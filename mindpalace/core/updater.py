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


def notice_text(info: dict) -> str:
    return "👋 Hey, there's a new update available. Want me to install it? Just say **yes**."


def pull() -> tuple[bool, str]:
    """Fast-forward pull. Won't touch local edits — reports if it can't auto-update."""
    rc, out = _git("pull", "--ff-only", timeout=180)
    if rc == 0:
        return True, out
    return False, out


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


def accept() -> str:
    """Owner said yes: pull + restart. Returns the message to post."""
    ok, out = pull()
    if not ok:
        clear_pending()
        return ("⚠️ Couldn't auto-update — looks like there are local changes in the way. "
                "I've left things as they are; this one needs a hand.\n```\n" + out[-600:] + "\n```")
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
