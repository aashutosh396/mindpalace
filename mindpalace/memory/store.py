"""Durable text memory + identity files — read helpers for the briefing."""
from __future__ import annotations

import re
import time
from .. import config
from .session_store import SessionStore

_STOP = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be", "to", "of",
         "in", "on", "for", "with", "my", "me", "you", "it", "this", "that", "what", "how",
         "do", "does", "did", "can", "could", "would", "should", "please", "need", "want",
         "get", "got", "have", "has", "the", "your", "our", "we", "us", "from", "about"}

_store: SessionStore | None = None


def store() -> SessionStore:
    global _store
    if _store is None:
        _store = SessionStore()
    return _store


def session_id() -> str:
    return time.strftime("%Y-%m-%d")


def _read(path, cap):
    try:
        c = path.read_text().strip()
        return c[:cap] if c else ""
    except FileNotFoundError:
        return ""


def identity_block() -> str:
    """Brain-style WORKING memory — kept tiny so each prompt stays light. The owner's essence
    + a map of what's known live in CORE.md; the full USER.md / MEMORY.md / vault are long-term,
    recalled on demand. Before CORE.md exists, fall back to a trimmed USER.md so nothing's empty."""
    parts = []
    agent = _read(config.AGENT_FILE(), 4000)
    if agent:
        parts.append("WHO YOU ARE (your persona):\n" + agent)
    core = _read(config.CORE_FILE(), config.core_budget() + 500)
    if core:
        parts.append(
            "WORKING MEMORY — your live, distilled sense of the owner + a MAP of what you know. "
            "This is your PRESENT memory. Deeper detail is long-term in USER.md, MEMORY.md and the "
            "vault: when the owner references something not in front of you, RECALL it (grep/read "
            "those) before assuming you don't know:\n" + core)
    else:                                            # bootstrap until the first compaction builds CORE.md
        user = _read(config.USER_FILE(), 1800)
        if user:
            parts.append("WHO YOU SERVE (the owner):\n" + user)
    return "\n\n".join(parts)


def memory_block() -> str:
    # Once CORE.md exists it carries the working memory + map, so we DON'T bulk-load MEMORY.md
    # each turn (it's long-term — recalled on demand). Only a small head as bootstrap before then.
    if config.CORE_FILE().exists():
        return ""
    mem = _read(config.MEMORY_FILE(), 1800)
    return ("YOUR MEMORY (durable facts — bootstrap; moves to working memory on next compaction):\n"
            + mem) if mem else ""


def _keywords(q: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_.-]{3,}", (q or "").lower())
    return [w for w in dict.fromkeys(words) if w not in _STOP][:8]


def _recall_longterm(query: str, cap: int = 1200) -> str:
    """Keyword search over MEMORY.md + vault so relevant long-term facts surface AUTOMATICALLY
    on each prompt — no reliance on the model remembering to grep. Cheap, no LLM."""
    kws = _keywords(query)
    if not kws:
        return ""
    files = [config.MEMORY_FILE()]
    try:
        files += [p for p in sorted(config.vault_dir().rglob("*.md"))
                  if p.name.lower() != "log.md"]   # LOG is an append-only timeline, not reference
    except Exception:
        pass
    scored = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except OSError:
            continue
        low = txt.lower()
        score = sum(low.count(k) for k in kws)
        if not score:
            continue
        best = sorted((ln for ln in txt.splitlines()
                       if ln.strip() and any(k in ln.lower() for k in kws)),
                      key=lambda ln: -sum(k in ln.lower() for k in kws))[:3]
        if best:
            scored.append((score, f.name, best))
    if not scored:
        return ""
    scored.sort(key=lambda x: -x[0])
    out, used = [], 0
    for _score, name, lines in scored[:4]:
        for ln in lines:
            snip = f"  [{name}] {ln.strip()[:200]}"
            if used + len(snip) > cap:
                return "\n".join(out)
            out.append(snip)
            used += len(snip)
    return "\n".join(out)


def recall_block(query: str, limit: int = 3) -> str:
    parts = []
    hits = store().search(query, limit=limit)
    if hits:
        lines = ["RELEVANT PAST CONTEXT (recalled from chat history):"]
        for role, content, ts in hits:
            date = time.strftime("%Y-%m-%d", time.localtime(ts))
            lines.append(f"  [{date}] {role}: {content[:300].strip().replace(chr(10), ' ')}")
        parts.append("\n".join(lines))
    lt = _recall_longterm(query)
    if lt:
        parts.append("RECALLED FROM LONG-TERM MEMORY (auto-matched to this message — open the "
                     "named file for full detail):\n" + lt)
    return "\n\n".join(parts)


def save_exchange(owner_text: str, agent_text: str) -> None:
    s, sid = store(), session_id()
    s.save_turn(sid, "Owner", owner_text)
    s.save_turn(sid, "Assistant", agent_text)
    config.touch_activity()   # gate idle-only background work (e.g. skill curation)
