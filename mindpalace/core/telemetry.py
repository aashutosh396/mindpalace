"""
Lightweight per-turn telemetry — so you can SEE the engine working during a soak.

Each streamed turn appends ONE JSONL line to state/turn_stats.jsonl recording how the turn ran:
session mode (create / resume / legacy), model, token usage (fresh input vs prompt-cache reads),
tool steps, and whether the stream fell back to the legacy path. `mindpalace usage` summarizes it.

Strictly best-effort: every call is wrapped so telemetry can NEVER break or slow a real turn.
"""
from __future__ import annotations

import json
import time

from .. import config

MAX_LINES = 2000            # keep the JSONL bounded
_TRIM_AT_BYTES = 1_000_000  # ~1 MB → trim to the last MAX_LINES


def _path():
    return config.state_dir() / "turn_stats.jsonl"


def log_turn(mode: str, model: str | None, usage: dict | None,
             steps: int, fallback: bool) -> None:
    """Append one turn's stats. usage is the claude `result` event's usage dict (or None)."""
    try:
        u = usage or {}
        row = {
            "ts": round(time.time(), 1),
            "mode": mode,                                   # create | resume | legacy
            "model": model or "default",
            "input": int(u.get("input_tokens", 0) or 0),               # FRESH input tokens
            "cache_read": int(u.get("cache_read_input_tokens", 0) or 0),
            "cache_create": int(u.get("cache_creation_input_tokens", 0) or 0),
            "output": int(u.get("output_tokens", 0) or 0),
            "steps": int(steps),
            "fallback": bool(fallback),
        }
        config.state_dir().mkdir(parents=True, exist_ok=True)
        p = _path()
        with p.open("a") as f:
            f.write(json.dumps(row) + "\n")
        if p.stat().st_size > _TRIM_AT_BYTES:               # trim occasionally, not every write
            tail = p.read_text().splitlines()[-MAX_LINES:]
            p.write_text("\n".join(tail) + "\n")
    except Exception:
        pass


def _rows(n: int):
    try:
        lines = _path().read_text().splitlines()[-n:]
    except (FileNotFoundError, OSError):
        return []
    out = []
    for ln in lines:
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def summarize(n: int = 50) -> str:
    """Human-readable rollup of the last n turns — the soak dashboard for session continuity."""
    rows = _rows(n)
    if not rows:
        return ("no turns recorded yet — chat with the bot a few times, then run "
                "`mindpalace usage` again.")
    modes: dict[str, int] = {}
    for r in rows:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    fresh = [r["input"] for r in rows]
    cread = [r["cache_read"] for r in rows]
    fallbacks = sum(1 for r in rows if r["fallback"])
    resumes = modes.get("resume", 0)
    avg_fresh = sum(fresh) / len(fresh)
    avg_cread = sum(cread) / len(cread)
    total_ctx = avg_fresh + avg_cread
    cache_pct = (avg_cread / total_ctx * 100) if total_ctx else 0.0
    # fresh-input on resume turns only — the headline continuity win
    resume_fresh = [r["input"] for r in rows if r["mode"] == "resume"]
    create_fresh = [r["input"] for r in rows if r["mode"] == "create"]

    def avg(xs):
        return (sum(xs) / len(xs)) if xs else 0.0

    lines = [
        f"📊 last {len(rows)} turns",
        f"  modes      : " + " · ".join(f"{k} {v}" for k, v in sorted(modes.items())),
        f"  fresh input: {avg_fresh:,.0f} tok/turn avg  (cache served {cache_pct:.0f}% of context)",
    ]
    if create_fresh and resume_fresh:
        lines.append(
            f"  continuity : create {avg(create_fresh):,.0f} tok → resume {avg(resume_fresh):,.0f} tok "
            f"fresh ({(1 - avg(resume_fresh) / avg(create_fresh)) * 100:.0f}% cheaper on resume)")
    if fallbacks:
        lines.append(f"  ⚠️ fallbacks: {fallbacks}/{len(rows)} turns fell back to the legacy path "
                     f"(continuity not taking — investigate)")
    else:
        lines.append("  fallbacks  : 0 ✅ (continuity holding)")
    return "\n".join(lines)
