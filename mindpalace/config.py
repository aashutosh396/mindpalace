"""
Config + path resolution — the CORE↔USER-DATA bridge.

The CORE (this repo) is stateless about any person. Everything instance-specific
lives in the USER-DATA home, resolved here. Set MINDPALACE_HOME to relocate it;
default is ~/.mindpalace. Update the core (git pull) → user data untouched.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# ---- core (this repo) ----
PKG_ROOT = Path(__file__).resolve().parent            # .../mindpalace (package)
REPO_ROOT = PKG_ROOT.parent                           # repo root
GLOBAL_SKILLS = PKG_ROOT / "skills" / "global"        # shipped reference skills (bundled, pristine)


# ---- user-data home ----
def home() -> Path:
    return Path(os.environ.get("MINDPALACE_HOME", Path.home() / ".mindpalace")).expanduser()


def config_path() -> Path:
    return home() / "config.json"


# data subdirs (instance-private)
def secrets_dir() -> Path:  return home() / "secrets"
def identity_dir() -> Path: return home() / "identity"
def memory_dir() -> Path:   return home() / "memory"
def user_skills() -> Path:  return home() / "skills"     # derived, per-user
def state_dir() -> Path:    return home() / "state"
def logs_dir() -> Path:     return home() / "logs"
def vault_dir() -> Path:    return home() / "vault"      # structured knowledge (resource-first)


def workspace_dir() -> Path:
    """Where project CODE lives. Owner can relocate it; default ~/.mindpalace/workspace."""
    p = load_config().get("workspace")
    return Path(p).expanduser() if p else home() / "workspace"


def workspace_confirmed() -> bool:
    """True once the owner has explicitly accepted/set their permanent workspace."""
    return bool(load_config().get("workspace_confirmed"))


def set_workspace(path: str | None = None) -> Path:
    """Set (and mark confirmed) the permanent project workspace. None confirms the default."""
    cfg = load_config()
    if path:
        cfg["workspace"] = str(Path(path).expanduser())
    cfg["workspace_confirmed"] = True
    save_config(cfg)
    d = workspace_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d

VAULT_SUBDIRS = ("projects", "infra", "accounts", "runbooks", "docs", "notes")

USER_FILE   = lambda: identity_dir() / "USER.md"        # the person's soul
AGENT_FILE  = lambda: identity_dir() / "AGENT.md"       # the agent's persona
MEMORY_FILE = lambda: memory_dir() / "MEMORY.md"        # durable facts


def is_initialized() -> bool:
    return config_path().exists()


def ensure_dirs() -> None:
    for d in (home(), secrets_dir(), identity_dir(), memory_dir(),
              user_skills(), state_dir(), logs_dir(), vault_dir(), workspace_dir()):
        d.mkdir(parents=True, exist_ok=True)
    for sub in VAULT_SUBDIRS:
        (vault_dir() / sub).mkdir(parents=True, exist_ok=True)
    log = vault_dir() / "LOG.md"
    if not log.exists():
        log.write_text("# LOG\n\nAppend-only timeline. The agent records what it does here.\n")
    readme = vault_dir() / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Vault — your structured knowledge\n\n"
            "Resource-first knowledge base the agent reads + writes:\n"
            "- `projects/` — one file per project (thin pointers to infra/accounts)\n"
            "- `infra/` — one per server/host/service\n"
            "- `accounts/` — one per platform/client (logins; encrypt secrets)\n"
            "- `runbooks/` — repeatable procedures\n"
            "- `docs/` , `notes/` — artifacts + freeform notes\n"
            "- `LOG.md` — append-only timeline\n")
    # secrets must never be world-readable
    try:
        os.chmod(secrets_dir(), 0o700)
    except OSError:
        pass


def load_config() -> dict:
    try:
        return json.loads(config_path().read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(cfg: dict) -> None:
    ensure_dirs()
    config_path().write_text(json.dumps(cfg, indent=2))


def read_secret(name: str) -> str | None:
    f = secrets_dir() / name
    return f.read_text().strip() if f.exists() else None


def write_secret(name: str, value: str) -> None:
    ensure_dirs()
    f = secrets_dir() / name
    f.write_text(value.strip())
    try:
        os.chmod(f, 0o600)
    except OSError:
        pass


# ---- admins (Discord access control) ----
# Only admins may drive the agent + run admin tasks (add bots/admins/webhooks, config).
# The local terminal is inherently trusted (machine access) — admin list gates REMOTE use.
def admins() -> list:
    return load_config().get("discord", {}).get("admins", [])


def is_admin(uid) -> bool:
    a = admins()
    return (not a) or int(uid) in a        # empty list (pre-setup) = allow


def add_admin(uid) -> bool:
    cfg = load_config()
    a = cfg.setdefault("discord", {}).setdefault("admins", [])
    if int(uid) in a:
        return False
    a.append(int(uid)); save_config(cfg); return True


def remove_admin(uid) -> bool:
    cfg = load_config()
    a = cfg.get("discord", {}).get("admins", [])
    if int(uid) not in a:
        return False
    a.remove(int(uid)); save_config(cfg); return True


# ---- webhooks (post updates to channels from anywhere, incl. cron out-of-process) ----
def concurrency() -> int:
    """Max simultaneous claude reasoning processes (parallel agents). Default 8."""
    try:
        return max(1, int(load_config().get("concurrency", 8)))
    except (TypeError, ValueError):
        return 8


def heartbeat_minutes() -> int:
    try:
        return int(load_config().get("heartbeat_minutes", 30))   # 0 = off
    except (TypeError, ValueError):
        return 0


def user_budget() -> int:
    """Soft char budget for USER.md — compaction distills the owner's profile to fit."""
    try:
        return max(1000, int(load_config().get("user_budget", 6000)))
    except (TypeError, ValueError):
        return 6000


def memory_budget() -> int:
    """Soft char budget for MEMORY.md — compaction distills durable facts to fit."""
    try:
        return max(1000, int(load_config().get("memory_budget", 9000)))
    except (TypeError, ValueError):
        return 9000


def compact_every() -> int:
    """Run a background memory-compaction pass every N exchanges. 0 = off."""
    try:
        return int(load_config().get("compact_every", 10))
    except (TypeError, ValueError):
        return 10


def webhooks() -> dict:
    return load_config().get("webhooks", {})


def set_webhook(name: str, url: str) -> None:
    cfg = load_config()
    cfg.setdefault("webhooks", {})[name] = url.strip()
    save_config(cfg)
