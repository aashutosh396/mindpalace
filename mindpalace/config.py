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

USER_FILE   = lambda: identity_dir() / "USER.md"        # the person's soul (long-term, on-demand)
AGENT_FILE  = lambda: identity_dir() / "AGENT.md"       # the agent's persona
MEMORY_FILE = lambda: memory_dir() / "MEMORY.md"        # durable facts (long-term, on-demand)
CORE_FILE   = lambda: identity_dir() / "CORE.md"        # WORKING memory: essence + map (always loaded)


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


def heartbeat_webhook() -> str:
    """Webhook the heartbeat posts its FULL report to (the bot's home channel gets only a short
    note, so long reports don't pile up there). Default 'home' — the channel webhook configured
    first during setup (the updates channel)."""
    return load_config().get("heartbeat_webhook", "home")


def heartbeat_channel_label() -> str:
    """Friendly channel name shown in the short home note ('full report in the … channel')."""
    return load_config().get("heartbeat_channel_label", "updates")


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


def core_budget() -> int:
    """Soft char budget for CORE.md — the tiny WORKING memory loaded on every prompt."""
    try:
        return max(500, int(load_config().get("core_budget", 2000)))
    except (TypeError, ValueError):
        return 2000


def background_model() -> str:
    """Cheaper model for background work (reflect/compact/review/curate). Filing facts and
    distilling memory doesn't need Opus — and Opus is where Max limits bite. '' = default model."""
    return load_config().get("background_model", "claude-sonnet-4-6")


def main_model() -> str:
    """Model for normal replies. Sonnet by default — Opus burns the Max limit ~5x faster and,
    per Anthropic/Microsoft data, doesn't improve routine coding. '' = honor the CLI default."""
    return load_config().get("main_model", "sonnet")


MODEL_ALIASES = {
    "sonnet": "sonnet", "opus": "opus", "haiku": "haiku",
    "default": "", "auto": "", "cli": "",
    "claude-sonnet": "sonnet", "claude-opus": "opus", "claude-haiku": "haiku",
}


def set_main_model(name: str):
    """Switch the model used for normal replies. Accepts sonnet/opus/haiku, a full claude-* id,
    or default/auto (honor the CLI default). Persists immediately (effective next reply — no
    restart). Returns the stored value (or '(CLI default)' for empty), or None if invalid."""
    n = (name or "").strip().lower()
    val = MODEL_ALIASES.get(n)
    if val is None:
        val = n if n.startswith("claude") else None
    if val is None:
        return None
    cfg = load_config()
    cfg["main_model"] = val
    save_config(cfg)
    return val or "(CLI default)"


def power_model() -> str:
    """Model for genuinely hard reasoning (architecture, stubborn bugs) — used only when the owner
    signals it (e.g. 'think hard', 'use opus'). Opus by default. 'Sonnet by default, Opus on purpose.'"""
    return load_config().get("power_model", "opus")


def reflect_every() -> int:
    """Run background reflection (file facts + skillify) every N exchanges, not every message.
    0 = off. Big Max-budget saver — reflection was a 2nd full call on every single message."""
    try:
        return int(load_config().get("reflect_every", 4))
    except (TypeError, ValueError):
        return 4


def turn_idle_seconds() -> int:
    """Streaming turns are killed only after this many seconds of NO progress (no prose/tool
    events) — an INACTIVITY watchdog, not a total cap. A task that keeps emitting steps runs as
    long as it stays productive; only a genuinely stuck turn is reaped. Default 600."""
    try:
        return max(60, int(load_config().get("turn_idle_seconds", 600)))
    except (TypeError, ValueError):
        return 600


def turn_max_seconds() -> int:
    """Hard backstop on total turn wall-clock, regardless of activity — stops a runaway from
    holding the session lock forever. 0 = no hard cap (rely on the idle watchdog alone).
    Default 3600 (1h)."""
    try:
        return max(0, int(load_config().get("turn_max_seconds", 3600)))
    except (TypeError, ValueError):
        return 3600


def session_continuity() -> bool:
    """Reuse ONE claude CLI session per day per identity (--session-id / --resume) instead of
    rebuilding the full prompt each turn. Gives full in-session history + prompt-cache hits.
    ON by default; set "session_continuity": false in config.json to fall back to the legacy
    full-prompt path."""
    return bool(load_config().get("session_continuity", True))


def lean_voice() -> bool:
    """Lean, more-to-the-point replies: short answers, no filler, ONE opener instead of running
    narration (chips still show progress) — while staying warm/human. ON by default; set
    "lean_voice": false to restore the chattier high-personality voice for an A/B."""
    return bool(load_config().get("lean_voice", True))


def session_rotate_turns() -> int:
    """With session continuity on, start a FRESH (leaner) claude session segment after this many
    turns, so a chatty day doesn't grow one giant session. The new segment is seeded with the
    persona + current CORE.md working memory, so distilled knowledge carries over. 0 = never
    rotate (one session per day). Default 60."""
    try:
        return int(load_config().get("session_rotate_turns", 60))
    except (TypeError, ValueError):
        return 60


def curator_idle_minutes() -> int:
    """Skip background skill-curation unless the owner's been idle at least this long, so the
    curator never rewrites skills mid-conversation (mirrors Hermes's 2h idle gate). Default 120."""
    try:
        return int(load_config().get("curator_idle_minutes", 120))
    except (TypeError, ValueError):
        return 120


def touch_activity() -> None:
    """Stamp the owner's last interaction — gates idle-only background work (e.g. skill curation)."""
    import time
    try:
        state_dir().mkdir(parents=True, exist_ok=True)
        (state_dir() / "last_activity.txt").write_text(str(time.time()))
    except OSError:
        pass


def idle_seconds() -> float:
    """Seconds since the owner last interacted (huge sentinel if never recorded)."""
    import time
    try:
        return time.time() - float((state_dir() / "last_activity.txt").read_text().strip())
    except (FileNotFoundError, ValueError):
        return 1e9


# ---- curator state (skill-curation cadence + pause + telemetry) ----
def curator_state() -> dict:
    """Persistent curator state: last_run (epoch), run_count, paused, last_summary."""
    try:
        st = json.loads((state_dir() / "curator_state.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        st = {}
    return {"last_run": float(st.get("last_run", 0.0)),
            "run_count": int(st.get("run_count", 0)),
            "paused": bool(st.get("paused", False)),
            "last_summary": str(st.get("last_summary", ""))}


def save_curator_state(st: dict) -> None:
    try:
        state_dir().mkdir(parents=True, exist_ok=True)
        (state_dir() / "curator_state.json").write_text(json.dumps(st, indent=2))
    except OSError:
        pass


def set_curator_paused(paused: bool) -> None:
    st = curator_state(); st["paused"] = bool(paused); save_curator_state(st)


def webhooks() -> dict:
    return load_config().get("webhooks", {})


def set_webhook(name: str, url: str) -> None:
    cfg = load_config()
    cfg.setdefault("webhooks", {})[name] = url.strip()
    save_config(cfg)
