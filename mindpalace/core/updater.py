"""
Git update watcher — the agent keeps an eye on its own source repo. When new commits
land on the remote, it tells the owner in plain English that an update is ready. If the
owner says "yes", it pulls the changes and restarts itself so the new code goes live.

Config:
  "update_check_minutes"  how often to check (default 30; 0 = off)
  "repo_dir"              override the repo path (default: the checkout this runs from)

Flow:
  loop() every N min → `git fetch` → if the remote is ahead, post a friendly notice and
  drop a marker at state/pending_update.json. When the owner replies "yes"/"pull"/"update",
  the gateway calls accept() → `git pull --ff-only` → detached self-restart.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from .. import config

_AFFIRM = {"yes", "y", "yeah", "yep", "yup", "sure", "ok", "okay", "do it", "go",
           "go ahead", "pull", "update", "pull it", "yes pull", "update it",
           "pull the changes", "pull changes", "do it now", "please do"}


def repo_dir() -> Path:
    """The git checkout this package runs from (…/v2), or a config override."""
    override = config.load_config().get("repo_dir")
    if override:
        return Path(override).expanduser()
    return Path(__file__).resolve().parents[2]


def interval_minutes() -> int:
    try:
        return int(config.load_config().get("update_check_minutes", 30))   # 0 = off
    except (TypeError, ValueError):
        return 0


def _git(*args, timeout=60) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=str(repo_dir()),
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:                       # noqa: BLE001
        return 1, str(e)


def _pending_path() -> Path:
    return config.state_dir() / "pending_update.json"


def read_pending() -> dict | None:
    try:
        return json.loads(_pending_path().read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_pending(info: dict) -> None:
    config.state_dir().mkdir(parents=True, exist_ok=True)
    _pending_path().write_text(json.dumps(info, indent=2))


def clear_pending() -> None:
    _pending_path().unlink(missing_ok=True)


def is_affirmative(text: str) -> bool:
    return text.strip().lower().strip("!.?") in _AFFIRM


def check() -> dict | None:
    """Fetch the remote and report how far behind we are. None = up to date / can't tell."""
    if not (repo_dir() / ".git").exists():
        return None
    rc, _ = _git("fetch", "--quiet")
    if rc != 0:
        return None
    rc, upstream = _git("rev-parse", "--abbrev-ref", "@{u}")    # e.g. origin/main
    if rc != 0:
        return None
    rc, counts = _git("rev-list", "--left-right", "--count", f"HEAD...{upstream}")
    if rc != 0:
        return None
    try:
        behind = int(counts.split()[1])
    except (IndexError, ValueError):
        return None
    if behind <= 0:
        return None
    _, remote_sha = _git("rev-parse", upstream)
    _, log = _git("log", "--no-merges", "--pretty=%s", f"HEAD..{upstream}")
    subjects = [s for s in log.splitlines() if s.strip()][:5]
    return {"behind": behind, "remote_sha": remote_sha.strip(),
            "upstream": upstream, "log": subjects}


# conventional-commit type → plain-English label a non-technical owner gets
_TYPE_LABEL = {
    "feat": "New", "fix": "Fixed", "perf": "Faster", "refactor": "Improved",
    "docs": "Docs", "style": "Polish", "test": "Tests", "chore": "Maintenance",
    "build": "Build", "ci": "CI", "revert": "Reverted",
}
_PREFIX = re.compile(r"^(\w+)(?:\([^)]*\))?!?:\s*(.+)$")   # type(scope): rest


def _humanize(subject: str) -> str:
    """Turn a raw commit subject into a plain-English line — no type(scope): noise."""
    s = (subject or "").strip()
    m = _PREFIX.match(s)
    if m:
        typ, rest = m.group(1).lower(), m.group(2).strip()
        rest = rest[:1].upper() + rest[1:] if rest else rest
        label = _TYPE_LABEL.get(typ)
        return f"{label}: {rest}" if label else rest
    return s[:1].upper() + s[1:] if s else s


def summarize_changes(subjects: list[str]) -> list[str]:
    """High-level, deduped bullets describing what changed (max 4)."""
    seen, out = set(), []
    for s in subjects or []:
        h = _humanize(s)
        k = h.lower()
        if h and k not in seen:
            seen.add(k)
            out.append(h)
    return out[:4]


def notice_text(info: dict) -> str:
    # Rendered as a Discord ```ansi``` block (real colors — diff's @@ shows white in Discord):
    # bold-cyan header, green + feature lines, bold-yellow call-to-action, gaps for breathing room.
    E, R = "\033", "\033[0m"
    bullets = summarize_changes(info.get("log") or [])
    feats = [f"{E}[0;32m+ {b}{R}" for b in bullets] or [f"{E}[0;32m+ improvements and fixes{R}"]
    lines = ["```ansi", f"{E}[1;36m🔔  UPDATE AVAILABLE{R}", ""]
    lines += feats
    lines += ["", f'{E}[1;33mreply "yes"  →  I pull + restart 🔄{R}', "```"]
    return "\n".join(lines)


def pull() -> tuple[bool, str]:
    """Fast-forward pull. Won't touch local edits — reports if it can't auto-update."""
    rc, out = _git("pull", "--ff-only", timeout=180)
    if rc == 0:
        return True, out
    return False, out


def _running_from_repo() -> bool:
    """True if the live package IS the checkout (Mac dev). False = copy-install (pipx),
    where the venv holds a snapshot and a pull alone won't update the running code."""
    try:
        return Path(__file__).resolve().is_relative_to(repo_dir().resolve())
    except Exception:                            # noqa: BLE001
        return False


def sync_venv() -> tuple[bool, str]:
    """On copy-installs (pipx hosts like gimi) reinstall the freshly-pulled checkout into
    the running venv, else the new code never goes live. No-op on run-from-checkout hosts."""
    if _running_from_repo():
        return True, "run-from-checkout; no reinstall needed"
    try:
        p = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--force-reinstall",
             "--no-deps", str(repo_dir())],
            capture_output=True, text=True, timeout=300)
        return p.returncode == 0, (p.stdout + p.stderr).strip()[-600:]
    except Exception as e:                       # noqa: BLE001
        return False, str(e)


def restart_detached(delay: int = 3) -> None:
    """Spawn a detached helper that restarts the daemon after a short delay, so the
    confirmation message lands before we drop the connection."""
    code = (
        f"import time;time.sleep({delay});"
        "from mindpalace.core import service;"
        "service.stop();time.sleep(1);service.spawn()")
    subprocess.Popen(
        [sys.executable, "-c", code],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
        env={**os.environ, "MINDPALACE_HOME": str(config.home())})


CRITICAL_FILES = (
    "mindpalace/core/brain.py", "mindpalace/core/daemon.py", "mindpalace/core/updater.py",
    "mindpalace/core/service.py", "mindpalace/gateways/discord.py", "mindpalace/gateways/terminal.py",
    "mindpalace/config.py", "mindpalace/cli.py", "mindpalace/agents/analyst.py",
    "mindpalace/memory/store.py", "mindpalace/skills.py",
)


def _head_sha() -> str:
    rc, out = _git("rev-parse", "HEAD")
    return out.strip() if rc == 0 else ""


def _compile_critical() -> tuple[bool, str]:
    """Syntax-check the files the daemon needs to boot. A bad pull that won't parse must NOT
    go live — better to roll back and stay on the working version than brick the bot."""
    import py_compile
    errs = []
    for rel in CRITICAL_FILES:
        p = repo_dir() / rel
        if not p.exists():
            continue
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            errs.append(str(e))
    return (not errs, "\n".join(errs)[-800:])


def accept() -> str:
    """Owner said yes: pull + restart. Returns the message to post."""
    before = _head_sha()                          # for rollback if the pull won't parse
    ok, out = pull()
    if not ok:
        clear_pending()
        return ("⚠️ Couldn't auto-update — looks like there are local changes in the way. "
                "I've left things as they are; this one needs a hand.\n```\n" + out[-600:] + "\n```")
    cok, cerr = _compile_critical()              # safety gate BEFORE we reload into the new code
    if not cok:
        if before:
            _git("reset", "--hard", before)      # restore the working version
        clear_pending()
        return ("⚠️ An update came in but it failed my safety check (won't parse), so I rolled it "
                "back and stayed on the version that works. A human should look.\n```\n"
                + cerr + "\n```")
    synced, sout = sync_venv()
    if not synced:
        clear_pending()
        return ("⚠️ Pulled the update but couldn't load it into my runtime — needs a hand."
                "\n```\n" + sout + "\n```")
    clear_pending()
    restart_detached()
    return "✅ Update pulled. Restarting myself now — back in a few seconds. 🔄"


async def loop(report, interval_min: int):
    """Background watcher. Re-notifies each interval while an update stays unpulled."""
    if interval_min <= 0:
        return
    print(f"updater: checking for updates every {interval_min}m")
    while True:
        await asyncio.sleep(interval_min * 60)
        try:
            info = await asyncio.to_thread(check)
            if not info:
                clear_pending()
                continue
            write_pending({"remote_sha": info["remote_sha"], "behind": info["behind"]})
            await report(notice_text(info))
        except Exception as e:                   # noqa: BLE001
            print(f"updater error: {e}")
