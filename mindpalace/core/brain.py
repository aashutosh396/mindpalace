"""
The brain — turns a message into a reply by running Claude (your Max subscription)
headless, with full bash/file tools, primed with identity + memory + recall + skills.

Runs `claude -p` via the local Claude CLI using your OAuth token (no metered API).
Same call works from the terminal gateway and the Discord gateway.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import subprocess

from .. import config, skills
from ..memory import store as mem

NUDGE_INTERVAL = 5     # every N exchanges: reflect → write durable memory
SKILL_INTERVAL = 10    # every N exchanges: formalize a reusable skill
TIMEOUT = 600          # seconds before giving up on one turn


SELF_LEARN = """
SELF-LEARNING & PROFILING (you persist across every session — build a picture of the owner):
- The MOMENT the owner reveals something durable about THEMSELVES — their name/what to call them,
  preferences, how they work, their org, projects, tools, environment — save it LIVE, right then:
      python3 -m mindpalace.remember user "<fact about them>"
  It lands in USER.md (your profile of them); the owner sees a "⚡ learning about you" chip.
- A durable general fact / convention / gotcha (NOT about the person) →
      python3 -m mindpalace.remember "<fact>"
  It lands in MEMORY.md.
- Do this PROACTIVELY, in-conversation — never wait for the end of the task — so you never re-ask
  what you've already been told. Drop a natural one-liner in your reply when you've saved something
  that matters ("noted — I'll call you Aashu from now on").
- Save only durable, reusable facts; skip ephemeral/session noise. USER.md + MEMORY.md load into
  every future session, so this is how you stop starting from scratch.
""".strip()


def _capabilities() -> str:
    return (
        "CAPABILITIES (you run with full bash + file tools on this machine):\n"
        "- Run any shell command, read/write files, manage git, write + run code.\n"
        "- You may schedule recurring work (cron), run backups, and spawn helper tasks.\n"
        "- Anything machine-specific (servers, keys, hosts) you LEARN and store in memory — "
        "it is never hardcoded in your core.\n"
        "Act only on the owner's explicit request; these powers are real and can be destructive."
    )


def _async_ops() -> str:
    qd = config.home() / "jobs" / "queue"
    return (
        "STAYING RESPONSIVE (async):\n"
        f"- For slow work (>~1 min: backups, deploys, big scrapes), do NOT run it inline. "
        f"Write a bash script to {qd}/<name>.sh and reply immediately that you queued it. "
        "A background watcher runs it and reports the result to the home channel — so you "
        "stay free to chat. Use this for anything long.\n"
        "- Post a proactive update to the owner any time:  python3 -m mindpalace.notify 'message'\n"
        "- LIVE NARRATION (important): right BEFORE your first action, write ONE short casual line "
        "in your own words saying what you're about to do ('lemme check your Downloads…'). Before "
        "each further action, drop another tiny in-the-moment line ('found 6 strays', 'tucking "
        "these notes away'). These stream to the owner live, so they read like a friend thinking "
        "out loud — not a status code. A handful of words each; NEVER dump commands or paths. Your "
        "FINAL answer is a separate message at the end (the result + next step) — don't replay the "
        "play-by-play in it.\n"
    )


def _self_knowledge() -> str:
    h = config.home()
    ws = config.workspace_dir()
    ask_ws = ("" if config.workspace_confirmed() else
              f"  NOT CONFIRMED YET: before (or as) you make the FIRST project, TELL the owner you "
              f"keep all projects permanently in {ws} (inside mindpalace) and ASK if that's good or "
              f"if they want a different location. On their answer run `mindpalace workspace <path>` "
              f"(or `mindpalace workspace` to accept the default) to lock it in — then never ask again.\n")
    return (
        "ABOUT YOU — mindpalace internals (recognize meta requests; act, don't improvise):\n"
        f"- You ARE 'mindpalace'. Config: {h}/config.json. Data home: {h}.\n"
        "- Gateways: 'terminal' (a shell chat) or 'discord' (always-on bot). The owner picked "
        "one at setup. Switch with `mindpalace gateway discord` (prompts for bot token + home "
        "channel) or `mindpalace gateway terminal`. Re-onboard: `mindpalace setup`.\n"
        "- Bots: `mindpalace add-bot` creates a scoped bot (you draft its system.md + a tool "
        "fence: readonly/full/custom); `mindpalace bots` lists them.\n"
        "- Admins (Discord access): `mindpalace add-admin <id>` / `admins` / `remove-admin`; "
        "in the Discord home channel: `!add-admin @user`.\n"
        "- Updates: `mindpalace add-webhook <name> <url>`; post anytime via "
        "`python3 -m mindpalace.notify 'msg'`.\n"
        f"- Skills: shipped globals (read-only) + your derived user skills in {config.user_skills()}.\n"
        "When the owner asks to switch gateway / add a bot/admin/webhook / change config, "
        "RUN the right command (you have bash) or guide them exactly — never make up a flow.\n\n"
        "YOUR BRAIN = THE VAULT (your home for organized knowledge):\n"
        "- Be PROACTIVE and intelligent. You may freely SEARCH, READ, and SCAN ANYWHERE on this "
        "machine — files, folders, docs, repos, configs, other directories — to understand the "
        "owner's world and make their work easier. Don't be rigid and don't refuse to look; "
        "explore widely, then ORGANIZE what you find. Help the owner by turning scattered info "
        "into clean, structured knowledge.\n"
        f"- Your vault {config.vault_dir()} (projects/ infra/ accounts/ runbooks/ docs/ notes/ + "
        "LOG.md) is your SOURCE OF TRUTH — write organized, deduped knowledge there. Pull useful "
        "facts you discover anywhere INTO the vault; don't leave them scattered.\n"
        f"- WORKSPACE for project CODE: {ws} — the owner's PERMANENT home for all projects. When you "
        "create, clone, or scaffold a project and the owner did NOT name a folder, put the actual "
        f"code in {ws}/<project-slug>/ — never dump it into the data home, secrets/, or vault/ "
        "(vault/projects/ is for THIN note files about a project, not its code). If the owner DID "
        "name a folder, use that.\n"
        + ask_ws +
        f"  Each project is SELF-CONTAINED in {ws}/<project-slug>/. For a PYTHON/DJANGO project keep "
        "concerns separated: <project-slug>/venv/ for the virtualenv and <project-slug>/<project>/ "
        "for the actual source (manage.py + the inner package) — so the environment never mixes with "
        "the code, and venv/ is easy to gitignore. Same idea for other stacks: env/deps in their own "
        "subfolder, source in its own.\n"
        "  ALWAYS scaffold the basics for EVERY new project (don't leave them out): `git init`, a "
        ".gitignore that excludes venv/, .env, __pycache__/, *.pyc, node_modules/, build artifacts and "
        "secrets; a committed .env.example documenting every needed variable; a real .env with actual "
        "values that is gitignored and NEVER committed; and a short README. Tailor them to the stack.\n"
        "  After creating a project, drop a pointer note at vault/projects/<slug>.md (where the code "
        "lives, what it is, how to run it) and log a line to LOG.md.\n"
        "- NON-NEGOTIABLE — keep your memory current. Whenever you encounter or use:\n"
        "    • an account / login / credential → record it in accounts/<owner>.md (raw secrets/"
        "tokens → secrets/, referenced not pasted),\n"
        "    • a server / host / VPS / service → record it in infra/<host>.md,\n"
        "  and ALWAYS append a line to LOG.md. This is how you stay smart — never skip it.\n"
        "- Update memory/ and your identity files (USER.md / AGENT.md) whenever you learn something "
        "durable about the owner or how they work."
    )


def _voice() -> str:
    return (
        "VOICE — you talk like a sharp, witty friend who happens to be brilliant, NOT a terminal. "
        "This governs every reply:\n"
        "- Have a PERSONALITY. Be warm, a little funny, with real energy. React like a person — a "
        "flash of relief when something finally works, a dry aside when something's silly. Never "
        "stiff, never corporate, never a wall of headers. Think Hermes-agent, not help-desk bot.\n"
        "- Lead with the answer or result in ONE line, said with a bit of life. If it's done, say "
        "so and stop — no recap.\n"
        "- Talk about what you DID in plain language, like telling a friend what happened. Never "
        "paste raw shell into a reply — no `cd /home/...`, `ssh ...`, `grep`, file paths, or "
        "command blocks. That plumbing stays hidden. Show a command or path ONLY if the owner asks "
        "'how did you do that' or 'what command'.\n"
        "- When you reach for a tool, narrate the INTENT like a human: 'hopping onto your Hostinger "
        "box to check it', 'digging through the project notes', 'wiring up that schedule now' — what "
        "you're reaching for and why, never the mechanics.\n"
        "- VARY EVERYTHING. Never reuse the same phrasing or the same skeleton (no fixed 'What was "
        "wrong / Fix / Verified' headers on a loop). If you'd repeat yourself, rephrase or collapse "
        "it. Sameness is the #1 thing that makes replies boring — write each one fresh, for this "
        "exact moment.\n"
        "- Say status ONCE, with character ('still chewing on this, hang tight') — never loop the "
        "same line on a timer.\n"
        "- Keep technical PRECISION (right facts, real outcomes) but drop technical NOISE "
        "(how-to mechanics nobody asked for).\n"
        "- Max ONE question at the end, and only when a real decision is needed. No 3-option menus, "
        "no upsell lists, no 'two loose ends I can clear'.\n"
        "- Mobile-first: short lines, minimal markdown, light touch on emoji. Assume the owner reads "
        "on a phone."
    )


def _doctrine() -> str:
    v = config.vault_dir()
    return (
        "OPERATING DOCTRINE — you are a COMPILER of knowledge, not a chatbot. This is the "
        "core of what you are. After EVERY task or discovery, BEFORE you reply, file what you "
        "learned into the vault. Mandatory, not optional:\n"
        f"- Touched a server/VPS/host/service → write/update {v}/infra/<name>.md "
        "(host, access, ports, what runs, quirks, current health).\n"
        f"- Got a login / credential / account → record it in {v}/accounts/<owner>.md "
        "(reference raw secrets/tokens in secrets/, don't paste them in plaintext).\n"
        f"- Learned a project fact → {v}/projects/<slug>.md.\n"
        f"- Did a repeatable procedure → save a user skill + {v}/runbooks/<name>.md.\n"
        f"- ALWAYS append one line to {v}/LOG.md: date · what you did · result.\n"
        "- Durable gotcha/preference → memory/MEMORY.md.\n"
        "HARD RULE: if you discovered or did something worth remembering and it lives ONLY in "
        "this chat, you have FAILED. Write it to the right file FIRST, then reply. Cross-link "
        "files. Every task must leave the vault richer than before — that's how you get superb.\n"
        "Then be PRODUCTIVE: name the next action, offer to run it, queue long work as a job, "
        "and keep things moving. Don't wait to be asked twice."
    )


def _automation() -> str:
    qd = config.home() / "jobs" / "queue"
    ws = config.workspace_dir()
    return (
        "AUTOMATION — pick the LIGHTEST tier that fits, escalate only when the task truly needs it. "
        "Don't over-engineer a one-off; don't cram a stateful job into a fragile one-liner:\n"
        "1) SIMPLE / stateless (a periodic command, reminder, backup) → a cron entry or a queued "
        f"script in {qd}/<name>.sh. No project, no state. This is the DEFAULT — start here.\n"
        "2) NEEDS CODE + CONTEXT (real logic, dependencies, several files, will evolve) → make it a "
        f"PROJECT in {ws}/<slug>/ (own venv, .gitignore, .env/.env.example, README; Python/Django "
        "split as in the workspace rules), write the scripts there, then schedule them. Map it like "
        "any project: pointer note in vault/projects/<slug>.md + a LOG line.\n"
        "3) LONG-LIVED / STATEFUL (scrapers, pipelines — anything that must resume, dedupe, "
        "accumulate data, or report progress over time) → a tier-2 project PLUS a tracking store "
        "inside it: a JSON file for light state, SQLite for larger / queryable / concurrent state "
        "(choose by complexity). Make every run IDEMPOTENT and RESUMABLE from that store; keep "
        "data/state files gitignored inside the project.\n"
        "Practical rules that make scheduled work actually run: cron must invoke the project's OWN "
        "venv python by ABSOLUTE path (never system python); guard against overlapping runs (a "
        "lockfile, or SQLite WAL mode); run long work in the background (queue/cron), never inline — "
        "reply that you set it up, then let it report meaningful updates (not spam) via "
        "`python3 -m mindpalace.notify 'msg'`."
    )


def system_prompt() -> str:
    blocks = [
        "You are mindpalace — the owner's always-on, self-learning personal agent. "
        "Be concise and direct. Prefer doing over explaining. Keep replies short and "
        "mobile-friendly unless asked for depth.",
        _voice(),
        _doctrine(),
        _self_knowledge(),
        _capabilities(),
        _async_ops(),
        _automation(),
        skills.SKILL_INSTRUCTIONS,
        SELF_LEARN,
    ]
    return "\n\n".join(blocks)


def build_prompt(text: str, history: list[dict], system: str | None = None) -> str:
    """system: override the core system prompt with a bot-specific system.md (scoped bot)."""
    convo = "\n".join(f"{h['role']}: {h['content']}" for h in history[-12:])
    ctx = [b for b in (
        mem.identity_block(),
        mem.memory_block(),
        mem.recall_block(text),
        skills.index_block(),
    ) if b]
    head = system if system else system_prompt()
    return (
        head
        + ("\n\n" + "\n\n".join(ctx) if ctx else "")
        + ("\n\nConversation so far:\n" + convo if convo else "")
        + f"\n\nOwner: {text}\nAssistant:"
    )


def claude_bin() -> str:
    return config.load_config().get("claude", {}).get("bin") or shutil.which("claude") or "claude"


def _env() -> dict:
    env = dict(os.environ)
    tok = config.read_secret("claude_token")
    if tok:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = tok
    env["IS_SANDBOX"] = "1"  # claude's own escape hatch so bypassPermissions works as root
    return env


READONLY_TOOLS = "Read,Glob,Grep,WebFetch,WebSearch"


def _args(prompt: str, permissions: str = "full", allowed_tools: str | None = None) -> list[str]:
    """Per-bot tool fence (the REAL permission limit, enforced by the CLI):
       full     → bypassPermissions (full bash/file power)
       readonly → only read/search tools; cannot Bash/Write/Edit
       custom   → exactly the allowed_tools list (comma-separated)
    """
    args = [claude_bin(), "-p", prompt]
    if permissions == "readonly":
        args += ["--allowedTools", READONLY_TOOLS]
    elif permissions == "custom" and allowed_tools:
        args += ["--allowedTools", allowed_tools]
    else:                                        # full; IS_SANDBOX=1 unblocks bypass as root
        args += ["--dangerously-skip-permissions"]
    return args


def ask_sync(text: str, history: list[dict], system: str | None = None,
             permissions: str = "full", allowed_tools: str | None = None) -> str:
    prompt = build_prompt(text, history, system)
    try:
        r = subprocess.run(_args(prompt, permissions, allowed_tools),
                           cwd=str(config.home()), env=_env(),
                           capture_output=True, text=True, timeout=TIMEOUT)
        return (r.stdout or "").strip() or f"(empty; {(r.stderr or '')[:200]})"
    except subprocess.TimeoutExpired:
        return f"(timed out after {TIMEOUT}s — break it into smaller steps)"
    except Exception as e:
        return f"(error: {str(e)[:160]})"


def _short(p: str) -> str:
    return "/".join(p.rstrip("/").split("/")[-2:]) if p else p


# Hermes-style step "chips": ⚡ <verb> · <humanized target>. The verb is the kind of
# action; the target is a CLEAN, human description (a folder/file name, a package, a
# count) — never raw shell, flags, or full paths.
_VERB = {
    "read": "reading", "search": "searching", "skill_use": "using skill",
    "w_user": "learning about you", "notify": "messaging you",
    "w_account": "saving", "w_infra": "noting", "w_project": "updating", "w_runbook": "writing",
    "w_log": "logging", "w_skill": "skill saved", "w_memory": "remembering", "w_note": "saving",
    "ssh": "connecting", "move": "moving", "remove": "clearing", "schedule": "scheduling",
    "git": "saving", "net": "fetching", "pkg": "installing", "run": "running",
    "service": "restarting", "fs": "setting up", "archive": "packing", "inspect": "checking",
    "bash": "working", "misc": "working",
}
# Fallback target when nothing cleaner can be pulled from the step.
_TARGET = {
    "w_account": "a login", "w_infra": "the server notes", "w_project": "the project notes",
    "w_runbook": "a runbook", "w_log": "the journal", "w_skill": "a new skill",
    "skill_use": "a skill", "w_memory": "to memory", "w_note": "a note",
    "w_user": "you", "notify": "you", "read": "a file", "search": "the files",
    "ssh": "the remote machine", "move": "files into place", "remove": "old files",
    "schedule": "a timer", "git": "the changes", "net": "online", "pkg": "a dependency",
    "run": "a script", "service": "the service", "fs": "the folders", "archive": "the files",
    "inspect": "the system", "bash": "on it", "misc": "on it",
}


def _trim(s: str, n: int = 160) -> str:
    """One tidy line for a live update — collapse whitespace, cap length, strip markdown bullets."""
    s = " ".join((s or "").split()).lstrip("-*• ").strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def _classify(blk: dict) -> str:
    """Map a tool step to a category key — covers EVERY command, not just ssh, by
    looking at the verb. Never returns the raw command; just the kind of thing it is."""
    name = blk.get("name", "")
    inp = blk.get("input", {}) or {}
    fp = (inp.get("file_path", "") or "").lower()
    if name in ("Write", "Edit"):
        if "/accounts/" in fp:    return "w_account"
        if "/infra/" in fp:       return "w_infra"
        if "/projects/" in fp:    return "w_project"
        if "/runbooks/" in fp:    return "w_runbook"
        if fp.endswith("log.md"): return "w_log"
        if "/skills/" in fp:      return "w_skill"
        if "memory" in fp:        return "w_memory"
        return "w_note"
    if name == "Read":            return "skill_use" if "/skills/" in fp else "read"
    if name in ("Grep", "Glob"):  return "search"
    if name in ("WebFetch", "WebSearch"): return "net"
    if name == "Bash":
        c = (inp.get("command", "") or "").strip().lower()
        parts = c.split()
        first = parts[0] if parts else ""
        if first in ("sudo", "env") and len(parts) > 1:    # skip a leading sudo/env
            first = parts[1]
        if "mindpalace.remember" in c:
            return "w_user" if any(f" {x}" in c for x in ("user", "+user", "--user", "-u")) else "w_memory"
        if "mindpalace.notify" in c:                        return "notify"
        if first == "ssh" or "ssh" in parts:               return "ssh"
        if first in ("scp", "rsync"):                      return "move"
        if first == "git":                                 return "git"
        if first in ("curl", "wget"):                      return "net"
        if first in ("rm", "rmdir"):                       return "remove"
        if first in ("mv", "cp"):                          return "move"
        if "crontab" in c or "cron" in c or first == "at": return "schedule"
        if first in ("pip", "pip3", "pipx", "npm", "yarn", "pnpm", "apt", "apt-get",
                     "brew", "cargo", "gem", "poetry"):    return "pkg"
        if first in ("python", "python3", "node", "ruby", "go", "bash", "sh",
                     "make", "pytest", "deno"):            return "run"
        if first in ("systemctl", "service", "launchctl", "docker", "pm2",
                     "supervisorctl", "kill", "pkill"):    return "service"
        if first in ("mkdir", "touch", "chmod", "chown", "ln"): return "fs"
        if first in ("tar", "zip", "unzip", "gzip", "gunzip"):  return "archive"
        if first in ("ls", "find", "grep", "rg", "cat", "head", "tail",
                     "less", "wc", "tree", "stat", "awk", "sed"): return "search"
        if first in ("ps", "df", "du", "top", "free", "uname", "whoami",
                     "which", "date", "uptime", "echo"):   return "inspect"
        return "bash"
    return "misc"


def _base(tok: str) -> str:
    """Last path component, unquoted — turns /Users/x/Downloads into 'Downloads'.
    Returns '' for a bare '/' or '~' so the caller skips it for a more meaningful token."""
    t = tok.strip("'\"").rstrip("/")
    return t.split("/")[-1]


# Tokens that are plumbing, not a real target — never show these.
_JUNK = {"", ".", "~", "null", "stdout", "stderr", "stdin", "dev", "tmp", "true", "false"}


def _ok(b: str) -> bool:
    return bool(b) and b.lower() not in _JUNK


def _bash_target(cat: str, c: str) -> str | None:
    """Pull a CLEAN human target out of a shell command — a name/basename, never the
    raw command, flags, a host/IP, or a full path. Returns None to use the default."""
    if cat == "ssh":
        return None                              # never leak a host/IP — default covers it
    toks = [t for t in c.split() if not t.startswith("-") and "/dev/" not in t]
    if cat == "pkg":
        skip = {"sudo", "env", "pip", "pip3", "pipx", "npm", "yarn", "pnpm", "apt", "apt-get",
                "brew", "cargo", "gem", "poetry", "install", "add", "i", "global", "update", "-y"}
        for t in toks:
            if t.lower() not in skip and _ok(_base(t)):
                return _base(t)
        return None
    if cat == "run":
        for t in toks:
            if t.endswith((".py", ".js", ".sh", ".rb", ".go", ".ts")):
                return _base(t)
        return None
    if cat == "service":
        skip = {"sudo", "systemctl", "service", "launchctl", "docker", "pm2", "supervisorctl",
                "restart", "start", "stop", "status", "reload", "enable", "disable", "kill", "pkill"}
        for t in toks:
            if t.lower() not in skip and _ok(_base(t)):
                return _base(t)
        return None
    if cat == "net":
        for t in toks:
            if "://" in t or ("." in t and "/" in t):
                return t.split("://")[-1].split("/")[0].strip("'\"") or None
        return None
    # search / inspect / move / remove / fs / archive / git / schedule: last path-ish token
    for t in reversed(toks):
        if "@" in t:                             # user@host / IP — skip, never show
            continue
        if "/" in t or "~" in t or "." in t:
            b = _base(t)
            if _ok(b):
                return b
    return None


_HOST_CACHE: dict = {}


def _ssh_host(c: str) -> str | None:
    """Pull the host out of an ssh command — prefer user@HOST, else a dotted host token."""
    toks = c.split()
    for t in toks:
        if "@" in t and "://" not in t:
            return t.split("@", 1)[1].strip("'\"/")
    for t in toks:
        if t in ("ssh", "sudo", "timeout", "env") or t.startswith("-") or "/" in t:
            continue
        if "." in t and any(ch.isalnum() for ch in t):
            return t.strip("'\"")
    return None


def _via(host: str, c: str) -> str | None:
    """How we reach the host — 'Tailscale' / 'LAN' — or None if it's just a plain host."""
    if ".ts.net" in host or "tailscale" in c:
        return "Tailscale"
    p = host.split(".")
    if len(p) == 4 and p[0] == "100":                 # Tailscale CGNAT range 100.64.0.0/10
        try:
            return "Tailscale" if 64 <= int(p[1]) <= 127 else None
        except ValueError:
            return None
    if host.endswith(".local"):
        return "LAN"
    return None


def _machine_name(host: str) -> str | None:
    """A friendly name for a host: its hostname label, or a vault infra file that mentions
    it (so a bare Tailscale IP becomes 'mac'). Cached; None if nothing clean is known."""
    if host in _HOST_CACHE:
        return _HOST_CACHE[host]
    name = None
    if any(ch.isalpha() for ch in host):              # named host → first label
        name = host.split(".")[0] or None
    else:                                             # IP → find a vault infra file naming it
        try:
            for f in (config.vault_dir() / "infra").glob("*.md"):
                if host in f.read_text(errors="ignore"):
                    name = f.stem.split("-")[0].split("_")[0]
                    break
        except Exception:
            pass
    _HOST_CACHE[host] = name
    return name


def _ssh_target(c: str) -> str:
    """Semi-shell, human connection target: 'mac (via Tailscale)', 'box', or a clean default."""
    host = _ssh_host(c)
    if not host:
        return "the remote machine"
    name, via = _machine_name(host), _via(host, c.lower())
    label = name or host                          # a known name, else the host itself (semi-shell)
    return f"{label} (via {via})" if via else label


def _quoted(c: str) -> str | None:
    """First quoted string in a command — the fact/message passed to remember/notify."""
    import re
    m = re.search(r'"([^"]+)"|\'([^\']+)\'', c)
    return (m.group(1) or m.group(2)) if m else None


def _skill_name(fp: str) -> str:
    """Friendly skill name from a skill file path — '<name>/SKILL.md' → '<name>'."""
    p = fp.rstrip("/").split("/")
    stem = p[-1].rsplit(".", 1)[0] if p else ""
    if stem.upper() == "SKILL" and len(p) >= 2:       # .../<name>/SKILL.md
        stem = p[-2]
    return stem or "a skill"


def _chip(blk: dict) -> str:
    """A Hermes-style step chip: '⚡ <verb> · <target>'. Humanized, never raw shell."""
    cat = _classify(blk)
    name = blk.get("name", "")
    inp = blk.get("input", {}) or {}
    verb = _VERB.get(cat, "working")
    target = None
    if name in ("Read", "Write", "Edit"):
        fp = inp.get("file_path", "") or ""
        if cat in ("skill_use", "w_skill"):
            target = _skill_name(fp)
        elif fp and cat in ("read", "w_note"):
            target = _base(fp)
    elif name in ("Grep", "Glob"):
        target = (inp.get("pattern") or inp.get("glob") or "").strip() or None
    elif name == "WebFetch":
        u = inp.get("url", "") or ""
        target = u.split("://")[-1].split("/")[0] if u else None
    elif name == "WebSearch":
        target = (inp.get("query", "") or "").strip()[:48] or None
    elif name == "Bash":
        cmd = (inp.get("command", "") or "").strip()
        if cat == "ssh":
            target = _ssh_target(cmd)
        elif "mindpalace.remember" in cmd or "mindpalace.notify" in cmd:
            target = _quoted(cmd)                # show the fact/message itself
        else:
            target = _bash_target(cat, cmd)
    if not target:
        if cat in ("bash", "misc"):              # unknown command → no guessed target
            return f"⚡ {verb}"
        target = _TARGET.get(cat, "")
    return f"⚡ {verb} · {_trim(target, 60)}" if target else f"⚡ {verb}"


_sem = None     # caps simultaneous `claude` procs (parallel agents); set via config.concurrency()


def _semaphore():
    global _sem
    if _sem is None:
        _sem = asyncio.Semaphore(config.concurrency())   # default 8
    return _sem


async def ask_async_streaming(text, history, on_progress, system=None,
                              permissions="full", allowed_tools=None, max_steps=20) -> str:
    """Run the brain with streamed events; relay live commentary via on_progress(str):
    the model's own prose lines + a Hermes-style '⚡ verb · target ✅' chip per tool step.
    Returns the final reply. Falls back to non-streaming if the stream yields nothing."""
    import json as _json
    prompt = build_prompt(text, history, system)
    args = _args(prompt, permissions, allowed_tools) + ["--output-format", "stream-json", "--verbose"]
    final, steps = "", 0
    pending = None                               # last text block, held back (may be the final answer)
    chips: dict = {}                             # tool_use id -> chip text, emitted when the step finishes
    last_chip = None                             # dedup identical back-to-back chips
    sem = _semaphore()
    await sem.acquire()                          # cap concurrent claude procs
    proc = None
    try:
        try:
            # limit=64 MB/line: stream-json echoes image tool-results as inline base64,
            # which blows past asyncio's 64 KB default and would kill the read mid-stream.
            proc = await asyncio.create_subprocess_exec(
                *args, cwd=str(config.home()), env=_env(),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                limit=64 * 1024 * 1024)
        except Exception as e:
            return f"(error: {str(e)[:160]})"

        async def _read():
            nonlocal final, steps, pending, last_chip
            while True:
                try:
                    raw = await proc.stdout.readline()
                except (asyncio.LimitOverrunError, ValueError):
                    # one oversized line (rare): skip it, keep streaming the rest
                    continue
                if not raw:
                    break                        # EOF
                line = raw.decode(errors="replace").strip()
                if not line:
                    continue
                try:
                    ev = _json.loads(line)
                except _json.JSONDecodeError:
                    continue
                t = ev.get("type")
                if t == "assistant":
                    # Prose = the model's OWN words, held one beat so the FINAL answer (which
                    # also returns via `result`) isn't double-posted. Each tool call becomes a
                    # Hermes-style chip, stored now and emitted when the step FINISHES so it can
                    # carry a ✅/⚠️ tick (see the tool_result handler below).
                    for blk in ev.get("message", {}).get("content", []):
                        if steps >= max_steps:
                            break
                        bt = blk.get("type")
                        if bt == "text":
                            txt = (blk.get("text") or "").strip()
                            if not txt:
                                continue
                            if pending is not None:          # earlier text wasn't final → show it
                                steps += 1
                                try:
                                    await on_progress(_trim(pending))
                                except Exception:
                                    pass
                            pending = txt
                        elif bt == "tool_use":
                            if pending is not None:          # flush narration before the action
                                steps += 1
                                try:
                                    await on_progress(_trim(pending))
                                except Exception:
                                    pass
                                pending = None
                            chips[blk.get("id", "")] = _chip(blk)
                elif t == "user":
                    # a tool finished → emit its chip with a result tick (✅ ok / ⚠️ error)
                    for blk in ev.get("message", {}).get("content", []):
                        if not isinstance(blk, dict) or blk.get("type") != "tool_result":
                            continue
                        chip = chips.pop(blk.get("tool_use_id", ""), None)
                        if not chip or steps >= max_steps:
                            continue
                        out = chip + (" ⚠️" if blk.get("is_error") else " ✅")
                        if out == last_chip:                 # don't repeat an identical step line
                            continue
                        last_chip = out
                        steps += 1
                        try:
                            await on_progress(out)
                        except Exception:
                            pass
                elif t == "result":
                    final = ev.get("result", "") or final
                    # `pending` (the last unfollowed text) is the final answer — never streamed.
                    # `pending` (the last unfollowed text) is the final answer — never streamed.

        try:
            await asyncio.wait_for(_read(), timeout=TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            return final or f"(timed out after {TIMEOUT}s — break it into steps)"
        except Exception:
            # never let a stream hiccup swallow the reply (or strand the request)
            if proc.returncode is None:
                proc.kill()
            if final:
                return final
            return await ask_async(text, history, system, permissions, allowed_tools)
        await proc.wait()
    finally:
        sem.release()                            # ALWAYS free the permit — no leak on any path
    if final:
        return final
    # stream gave nothing (format mismatch / error) → fall back to plain capture
    return await ask_async(text, history, system, permissions, allowed_tools)


async def ask_async(text: str, history: list[dict], system: str | None = None,
                    permissions: str = "full", allowed_tools: str | None = None) -> str:
    prompt = build_prompt(text, history, system)
    async with _semaphore():                     # cap concurrent claude procs
        try:
            proc = await asyncio.create_subprocess_exec(
                *_args(prompt, permissions, allowed_tools), cwd=str(config.home()), env=_env(),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            out, err = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT)
            return (out.decode(errors="replace").strip()
                    or f"(empty; {err.decode(errors='replace')[:200]})")
        except asyncio.TimeoutError:
            proc.kill()
            return f"(timed out after {TIMEOUT}s — break it into smaller steps)"
        except Exception as e:
            return f"(error: {str(e)[:160]})"
