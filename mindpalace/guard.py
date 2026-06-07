"""
Safety guard — a Claude Code PreToolUse hook that runs before EVERY Bash command the agent
issues, even under --dangerously-skip-permissions (hooks fire regardless of permission mode).

Two jobs:
  • BACKUP-THEN-ALLOW recoverable-but-scary ops: snapshot a DB / a git restore point before
    irreversible DB changes, force-pushes, or `git reset --hard`, then let them proceed.
  • HARD-BLOCK the truly unrecoverable: `rm -rf` on system/home paths, mkfs, dd to a disk,
    fork bomb, `chmod -R`/`chown -R` on /. The model cannot bypass this.

Everything else passes instantly. The guard FAILS OPEN on its own errors — a bug here must
never brick the agent — but FAILS CLOSED on a matched catastrophic pattern.

Invoked by the hook as:  <python> -m mindpalace.guard --home <data-home>
Reads the tool-call JSON on stdin; exit 2 + JSON = block, exit 0 = allow.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ---- paths -----------------------------------------------------------------

def _home() -> Path:
    for i, a in enumerate(sys.argv):
        if a == "--home" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).expanduser()
    return Path(os.environ.get("MINDPALACE_HOME", Path.home() / ".mindpalace")).expanduser()


def _backup_dir() -> Path:
    d = _home() / "backups"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---- hook decisions --------------------------------------------------------

def _allow():
    sys.exit(0)


def _block(reason: str):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    sys.stderr.write("🛡️ SAFETY GATE blocked this command: " + reason +
                     "\nIt's irreversible and has no backup. If you truly need it, the owner "
                     "must run it by hand.\n")
    sys.exit(2)


# ---- catastrophic (block) patterns: only the genuinely unrecoverable -------
# scratch roots where rm -rf is always fine (throwaway space)
_SCRATCH = ("/tmp/", "/var/tmp/", "/private/tmp/")
# WHOLE-TREE wipe targets — block these, but ALLOW deep paths under them
# (e.g. block `rm -rf /var` and `rm -rf ~/*`, but allow `rm -rf /var/www` and `rm -rf ~/proj/x`).
_DANGER = re.compile(
    r'(^|\s)('
    r'/|/\*|'                                   # filesystem root
    r'~|~/|~/\*|'                               # whole home (shorthand)
    r'\$home(/\*)?|'                            # $HOME or $HOME/*
    r'/(etc|usr|bin|sbin|lib\w*|boot|root|home|var|opt|srv|sys|proc)(/\*)?'
    r')(\s|$)')


def _is_rm_rf(low: str) -> bool:
    return bool(re.search(r'\brm\s+(?:-\w+\s+)*-\w*r\w*f|\brm\s+(?:-\w+\s+)*-\w*f\w*r|'
                          r'\brm\s+-r\s+-f|\brm\s+-f\s+-r', low))


def _catastrophic(c: str) -> str | None:
    low = c.lower()
    if re.search(r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:', c):
        return "fork bomb"
    if re.search(r'\b(mkfs\S*|mke2fs|mkswap|fdisk|parted)\b', low):
        return "formatting / partitioning a disk"
    if re.search(r'\bdd\b[^|]*\bof=/dev/', low):
        return "writing raw bytes to a disk device (dd of=/dev/…)"
    if re.search(r'>\s*/dev/(sd|nvme|disk|mmcblk|hd)', low):
        return "overwriting a disk device"
    if re.search(r'\bchmod\s+-r\b[^/]*\s/(\s|$)|\bchown\s+-r\b[^/]*\s/(\s|$)', low):
        return "recursive chmod/chown on /"
    if _is_rm_rf(low):
        if any(s in low for s in _SCRATCH):
            return None                          # scratch dirs are fine
        if _DANGER.search(low):
            return "recursive force-delete of the filesystem root or a whole home/system tree"
    return None


# ---- backup-then-allow detection ------------------------------------------

_DB_DESTRUCTIVE = re.compile(r'\b(drop\s+(database|table)|truncate|delete\s+from|alter\s+table|'
                             r'\.migrate\b|manage\.py\s+migrate|alembic\s+upgrade)\b', re.I)
_SQLITE_FILE = re.compile(r"[^\s'\"]+\.(?:db|sqlite|sqlite3)\b")


def _stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def _backup_sqlite(c: str) -> list[str]:
    saved = []
    for m in _SQLITE_FILE.finditer(c):
        f = Path(m.group(0).strip("'\""))
        try:
            if f.exists() and f.is_file():
                dest = _backup_dir() / f"{f.name}.{_stamp()}.bak"
                shutil.copy2(f, dest)
                saved.append(dest.name)
        except OSError:
            pass
    return saved


def _backup_mysql(c: str) -> list[str]:
    """Best-effort logical dump using the same connection flags present in the command."""
    tool = "mysqldump" if re.search(r'\bmysql\b', c) else ("pg_dump" if re.search(r'\bpsql\b', c) else None)
    if not tool or not shutil.which(tool):
        return []
    flags = re.findall(r'(-[hu]\s*\S+|--host=\S+|--user=\S+|-p\S*|--password=\S+|--port=\S+)', c)
    dbs = re.findall(r'(?:--database=|\b-D\s*)(\S+)', c)
    dest = _backup_dir() / f"db-dump.{_stamp()}.sql"
    try:
        with open(dest, "w") as fh:
            subprocess.run([tool, *[f for fl in flags for f in fl.split(maxsplit=1)], *dbs],
                           stdout=fh, stderr=subprocess.DEVNULL, timeout=120)
        if dest.stat().st_size > 0:
            return [dest.name]
        dest.unlink(missing_ok=True)
    except Exception:
        try:
            dest.unlink(missing_ok=True)
        except OSError:
            pass
    return []


def _backup_git(c: str) -> list[str]:
    """Snapshot the current HEAD as a bundle before a force-push / hard reset."""
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        inside = subprocess.run(["git", "-C", cwd, "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True, timeout=10)
        if inside.returncode != 0:
            return []
        dest = _backup_dir() / f"git-{Path(cwd).name}.{_stamp()}.bundle"
        r = subprocess.run(["git", "-C", cwd, "bundle", "create", str(dest), "--all"],
                           capture_output=True, text=True, timeout=60)
        return [dest.name] if r.returncode == 0 else []
    except Exception:
        return []


def _maybe_backup(c: str) -> list[str]:
    low = c.lower()
    saved = []
    if _DB_DESTRUCTIVE.search(c) or (_SQLITE_FILE.search(c) and re.search(r'\brm\b', low)):
        saved += _backup_sqlite(c)
        if re.search(r'\bmysql\b|\bpsql\b', low) and _DB_DESTRUCTIVE.search(c):
            saved += _backup_mysql(c)
    if re.search(r'\bgit\s+push\b.*(--force|-f|\s\+)|\bgit\s+reset\s+--hard\b', low):
        saved += _backup_git(c)
    return saved


# ---- entry point -----------------------------------------------------------

def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        _allow()                                 # can't parse → fail open
    if data.get("tool_name") != "Bash":
        _allow()
    cmd = (data.get("tool_input", {}) or {}).get("command", "") or ""
    if not cmd.strip():
        _allow()
    try:
        reason = _catastrophic(cmd)
        if reason:
            _block(reason)                       # fail CLOSED on a matched catastrophe
        saved = _maybe_backup(cmd)
        if saved:
            print(f"🛟 safety backup saved before this: {', '.join(saved)} (in backups/)")
    except SystemExit:
        raise
    except Exception:
        pass                                     # any guard bug → fail OPEN, never brick the agent
    _allow()


# ---- installer: write the hook config the daemon points claude at ----------

def ensure_installed() -> None:
    """Write ~/.mindpalace/.claude/{settings.json,hooks/guard.sh} so `claude -p` (cwd=home)
    runs this guard before every Bash call. Idempotent; refreshes paths each daemon start."""
    home = _home()
    hooks = home / ".claude" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    sh = hooks / "guard.sh"
    sh.write_text(f'#!/bin/bash\nexec "{sys.executable}" -m mindpalace.guard --home "{home}"\n')
    try:
        sh.chmod(0o755)
    except OSError:
        pass
    settings = home / ".claude" / "settings.json"
    cfg = {"hooks": {"PreToolUse": [
        {"matcher": "Bash", "hooks": [
            {"type": "command", "command": str(sh), "timeout": 30}]}]}}
    settings.write_text(json.dumps(cfg, indent=2))


if __name__ == "__main__":
    main()
