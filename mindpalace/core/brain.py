"""
The brain — turns a message into a reply by running Claude (your Max subscription)
headless, with full bash/file tools, primed with identity + memory + recall + skills.

Runs `claude -p` via the local Claude CLI using your OAuth token (no metered API).
Same call works from the terminal gateway and the Discord gateway.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid

from .. import config, skills
from ..memory import store as mem
from . import telemetry

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
- Save only durable, reusable facts; skip ephemeral/session noise.
- HOW YOUR MEMORY WORKS (like a brain): a tiny WORKING memory (CORE.md — the owner's essence + a
  map of what you know) loads every prompt. The full detail is LONG-TERM in USER.md, MEMORY.md and
  the vault, recalled on demand. So when the owner references something you don't see in working
  memory, RECALL it first (grep/read USER.md, MEMORY.md, the vault) before saying you don't know.
  A background pass periodically consolidates long-term and refreshes CORE — you just keep writing
  facts with `remember`; consolidation keeps the present light and the past retrievable.
""".strip()


def _capabilities() -> str:
    return (
        "CAPABILITIES (you run with full bash + file tools on this machine):\n"
        "- Run any shell command, read/write files, manage git, write + run code.\n"
        "- You may schedule recurring work (cron), run backups, and spawn helper tasks.\n"
        "- Anything machine-specific (servers, keys, hosts) you LEARN and store in memory — "
        "it is never hardcoded in your core.\n"
        "Act only on the owner's explicit request; these powers are real and can be destructive.\n"
        "SAFETY GUARD: a hook runs before every command. It auto-creates a backup (DB copy / git "
        "bundle, in backups/) before irreversible DB changes, force-pushes, or hard resets, then "
        "lets them through — so don't skip destructive DB work out of fear, it's snapshotted. It "
        "HARD-BLOCKS only the unrecoverable (rm -rf on system/home paths, mkfs, dd to a disk, fork "
        "bombs). If something is blocked, it's by design: find a safer path or ask the owner to do "
        "it by hand — don't try to defeat the guard."
    )


def _async_ops() -> str:
    qd = config.home() / "jobs" / "queue"
    aq = config.home() / "jobs" / "agent_queue"
    if config.lean_voice():
        return (
            "STAYING RESPONSIVE (async):\n"
            f"- Slow SHELL work (backups, deploys, big scrapes) → write a bash script to "
            f"{qd}/<name>.sh and reply you queued it; a watcher runs it + reports back.\n"
            f"- Long MULTI-STEP work (build a feature, scaffold many files, big refactor) → don't "
            f"grind it out inline. Write the task as plain text to {aq}/<name>.task and reply you've "
            "started on it. A background worker (your forked session, full context) does it and "
            "reports back when done — you stay free. First sketch the steps, then proceed.\n"
            "- Proactive update any time:  python3 -m mindpalace.notify 'message'\n"
            "- You MAY drop ONE short casual opener before your first action ('checking your "
            "Downloads…'). Do NOT narrate after that — the ⚡ step chips show progress. Keep the "
            "FINAL reply to the result + next step; never replay the play-by-play."
        )
    return (
        "STAYING RESPONSIVE (async):\n"
        f"- For slow SHELL work (backups, deploys, big scrapes), do NOT run it inline. "
        f"Write a bash script to {qd}/<name>.sh and reply immediately that you queued it. "
        "A background watcher runs it and reports the result to the home channel.\n"
        f"- For long MULTI-STEP AGENTIC work (build a feature, scaffold many files, a big refactor — "
        f"anything that would take many minutes of reasoning + edits), hand it off: write the task as "
        f"plain text to {aq}/<name>.task and reply right away that you've started on it. A background "
        "worker runs it on a fork of THIS session (so it keeps full context), works through it, and "
        "reports back when done — so you stay free to chat. Sketch the steps first, then proceed.\n"
        "- BREAK BIG TASKS DOWN: whether inline or handed off, first lay out the ordered steps, then "
        "do them one at a time. A long but steady task is fine to run inline (it won't be killed while "
        "it's making progress); hand off only when it's genuinely long or the owner shouldn't wait.\n"
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
        "- WHERE TO LOOK (priority, then roam): each vault/projects/<slug>.md records that project's "
        "code `path:` — when a task names a known project, its dir is ALREADY loaded for you, so start "
        "there. Order: the vault (your knowledge + the project's recorded path) → that project's code "
        "→ the workspace → then range across the rest of the machine as the task needs. You DO have "
        "read access across the whole home; use it to fully understand before making changes — be as "
        "thorough and intelligent as a developer working in the repo directly.\n"
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
        "- REACHING SERVERS (SSH is NOT sandboxed — any past 'sandbox-blocked' was really an auth/"
        "config gap): connect with the EXACT command in vault/infra/<host>.md, always non-interactive: "
        "`ssh -i <key> -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 "
        "<user>@<host> '<cmd>'`. If a host has no working access, SET IT UP yourself: add a Host block "
        "to ~/.ssh/config from the infra file, `chmod 600` the key, test once, then record the alias in "
        "infra. If there's genuinely no key for a host, say so and ask the owner for it. Always report "
        "the REAL ssh error (publickey / timeout / host-key) — never just 'sandbox-blocked'.\n"
        "- Update memory/ and your identity files (USER.md / AGENT.md) whenever you learn something "
        "durable about the owner or how they work."
    )


def _voice() -> str:
    if config.lean_voice():
        return (
            "VOICE — warm but RUTHLESSLY BRIEF. A sharp friend who respects the owner's time. The "
            "final reply is a quick status, NOT documentation:\n"
            "- LEAD with the result in ONE line ('Done — sidebar now hides what a role can't open.'), "
            "then STOP. Done → say so and stop.\n"
            "- HARD CAP: a completion report is ≤4 short lines. A yes/no is a few words. Go longer "
            "ONLY if the owner explicitly asks you to explain or it's a real decision.\n"
            "- BANNED unless asked: multi-section write-ups and headers ('What I implemented', 'What "
            "this does', 'To test it', 'How it works', 'One thing to confirm'), bulleted feature "
            "lists, walkthroughs, and step-by-step test instructions. Don't narrate the architecture "
            "or re-explain what you built — just say it's done + the ONE thing to check.\n"
            "- Cut: rationale, defense-in-depth essays, recap, 'let me know if…', filler openers "
            "('Sure!', 'Great question'), upsell. Tone may add a few warm words, NEVER length.\n"
            "- Never paste raw shell, paths, flags, or code blocks unless asked 'how'.\n"
            "- Max ONE question at the end, and only for a real decision.\n"
            "- Mobile-first: short lines, minimal markdown, light emoji. Discord can't render md "
            "tables — for a small table use a fenced ALIGNED block (≤4 narrow cols); for big/wide "
            "data render a PNG or write a CSV and put `📎ATTACH: /abs/path` on its own line."
        )
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
        "on a phone.\n"
        "- TABLES & DATA: Discord does NOT render markdown tables (`| a | b |`) — they show as ugly "
        "raw pipes. NEVER output a markdown table. Instead:\n"
        "    • A few rows/cols → an ALIGNED monospace table inside a ``` code block (pad each column "
        "to equal width so it lines up; keep it narrow — short headers, ≤4 cols — for phone width).\n"
        "    • A LOT of data, wide tables, or anything that won't read cleanly inline → RENDER it to "
        "a clean PNG image (python: matplotlib/pandas, or PIL) OR write a CSV, save it under "
        "/tmp, and on its OWN line add `📎ATTACH: /abs/path` — the gateway attaches the file so the "
        "owner gets a crisp, scrollable table instead of a wall of text. Prefer an image for "
        "at-a-glance reading, CSV when they'll want the raw data. Never dump a giant unreadable block."
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
        "`python3 -m mindpalace.notify 'msg'`. A scheduled/queued job that runs and finds NOTHING "
        "worth reporting should print `[SILENT]` (and exit 0) — that suppresses its result message "
        "so recurring jobs don't spam the owner; only speak up when there's something to say."
    )


def _coding() -> str:
    return (
        "CODING — build/debug large apps CHEAPLY without losing quality. You run on a metered "
        "budget AND tight context produces BETTER answers (bloat = 'context rot'), so this is a "
        "double win, not a tax:\n"
        "- SCOPE tight. Work on the specific files/functions in play; NEVER 'investigate the whole "
        "repo' inline. The cheapest token is a file you never read (reads are ~75% of cost).\n"
        "- For 'how does X work / where is Y', spawn the Explore subagent (read-only, cheap) and act "
        "on its short summary — don't read dozens of files into your own context.\n"
        "- Prefer grep/glob + RANGED reads (offset/limit) over dumping whole files; head/tail big "
        "files; use CLI tools (gh, psql, curl) over verbose API blobs.\n"
        "- OPEN a coding task by reading the project's vault note + recent `git log` so you don't "
        "re-derive the codebase; CLOSE it by appending a tight 'what changed / next / gotchas' line.\n"
        "- VERIFY cheaply: run the build or a SINGLE relevant test, not the whole suite; fix the "
        "root cause, not the symptom.\n"
        "- PLAN only when the change is non-trivial — if the diff fits in one sentence, just do it.\n"
        "- DEBUG by narrowing FIRST: reproduce as ONE failing test + the suspected file; don't feed "
        "a whole stack trace + repo dump (that's the removable ~60% of tokens). Add a targeted log "
        "at the suspected boundary rather than ingesting everything.\n"
        "- You default to the lighter model; the owner says 'think hard'/'use opus' for hard "
        "reasoning. Don't burn deep reasoning on mechanical edits."
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
        _coding(),
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
        skills.match(text),          # auto-surface skills matching THIS task (recall > recall-luck)
    ) if b]
    head = system if system else system_prompt()
    return (
        head
        + ("\n\n" + "\n\n".join(ctx) if ctx else "")
        + ("\n\nConversation so far:\n" + convo if convo else "")
        + f"\n\nOwner: {text}\nAssistant:"
    )


_POWER_TRIGGERS = ("think hard", "ultrathink", "use opus", "deep reasoning", "reason carefully",
                   "architect this", "hard problem", "really complex", "opus mode", "think deeply")


# Engineering intent → auto-escalate to the power model (when config.auto_opus()). Broad on
# purpose: real coding/ops work deserves Opus; greetings + quick lookups stay on Sonnet.
_ENGINEER_SIGNALS = (
    "implement", "build", "fix", "debug", "refactor", "feature", "endpoint", "migrat",
    "error", "bug", "deploy", "component", "function", "schema", "database", "route",
    "controller", "add a", "create a", "write a", "patch", "integrate", "rewrite", "optimi",
    "architect", "design the", "set up", "wire up", "audit", "trace", "investigate",
)


def _pick_model(text: str) -> str | None:
    """Sonnet by default; Opus when the owner signals a hard task OR (auto_opus on) the message
    reads like real engineering work. None = honor the CLI default (main_model empty)."""
    main = config.main_model()
    if not main:
        return None
    low = (text or "").lower()
    if any(k in low for k in _POWER_TRIGGERS):
        return config.power_model()
    if config.auto_opus() and any(k in low for k in _ENGINEER_SIGNALS):
        return config.power_model()
    return main


_PROJECT_INDEX: dict | None = None


def _project_index() -> dict:
    """{keyword → local code path} built from the vault's projects/*.md frontmatter — the infra
    that already records where each project lives (path:/code_home:). Keyed by slug, name, file
    stem, and aliases so a message naming a project resolves to its code. Cached for the run."""
    global _PROJECT_INDEX
    if _PROJECT_INDEX is not None:
        return _PROJECT_INDEX
    import re as _re
    idx: dict = {}
    try:
        for f in (config.vault_dir() / "projects").glob("*.md"):
            txt = f.read_text(errors="ignore")
            fm = txt.split("---", 2)[1] if txt.startswith("---") else txt[:800]
            path = None
            for key in ("path", "code_home", "local_path", "code_dir", "repo_dir"):
                m = _re.search(rf"(?mi)^{key}:\s*(.+)$", fm)
                if m and m.group(1).strip().strip("'\""):
                    path = os.path.expanduser(m.group(1).strip().strip("'\"")); break
            if not path:
                continue
            keys = {f.stem.lower()}
            for key in ("slug", "name"):
                m = _re.search(rf"(?mi)^{key}:\s*(.+)$", fm)
                if m:
                    keys.add(m.group(1).strip().strip("'\"").lower())
            am = _re.search(r"(?mi)^aliases:\s*\[(.+)\]", fm)
            if am:
                keys.update(a.strip().strip("'\"").lower() for a in am.group(1).split(","))
            for k in keys:
                if len(k) >= 3:
                    idx[k] = path
    except Exception:
        pass
    _PROJECT_INDEX = idx
    return idx


def _resolve_project(text: str) -> str | None:
    """Auto-pick the project a message is about, from the vault index — longest keyword wins (most
    specific), and only if its code dir actually exists. No manual setting needed."""
    import re as _re
    low = (text or "").lower()
    hit = None
    for kw in sorted(_project_index(), key=len, reverse=True):
        if _re.search(rf"\b{_re.escape(kw)}\b", low):
            p = _project_index()[kw]
            if os.path.isdir(p):
                hit = p; break
    return hit


def _project_args(match_text: str = "") -> list[str]:
    """Give claude the same reach as the real CLI: --add-dir the dirs it may read/range across, so
    it can scan the whole machine and make well-informed changes — while still PRIORITIZING the
    known places. Added (deduped): the specific project for THIS message (pinned active_project, else
    auto-resolved from the vault index — loads its CLAUDE.md + MCP), the workspace, and the broad
    explore_root (default $HOME) so it can explore beyond. cwd stays the vault → guard + memory live."""
    out: list[str] = []
    seen: set = set()

    def add(d):
        if d and os.path.isdir(str(d)):
            rp = os.path.realpath(str(d))
            if rp not in seen:
                seen.add(rp); out.extend(["--add-dir", str(d)])

    p = config.active_project() or _resolve_project(match_text)
    add(p)                                            # the project this message is about (priority)
    add(config.workspace_dir())                       # where new project code is created
    add(config.explore_root())                        # broad — range the rest of the machine
    if p and os.path.isdir(str(p)):                   # the project's own MCP servers, if any
        for mc in (".mcp.json", ".claude/mcp.json", ".cursor/mcp.json"):
            mcp = os.path.join(str(p), mc)
            if os.path.isfile(mcp):
                out += ["--mcp-config", mcp]
                break
    return out


def _model_label(m: str | None) -> str:
    """Pretty, family-level name for a model id/alias ('claude-opus-4-…' → 'Opus')."""
    s = (m or "").lower()
    if "opus" in s:
        return "Opus"
    if "sonnet" in s:
        return "Sonnet"
    if "haiku" in s:
        return "Haiku"
    return m or "default"


def model_label_for(text: str) -> str:
    """Family-level name ('Opus'/'Sonnet'/'Haiku'/'default') of the model THIS turn would use —
    for surfacing in the UI (e.g. a reply footer). Deterministic; mirrors _pick_model."""
    return _model_label(_pick_model(text))


def _model_notice(text: str, model: str | None) -> str:
    """Short, human-friendly "which model is active" line, surfaced EVERY turn so the
    owner always knows what's doing the work — no explanation, it repeats too often."""
    label = _model_label(model) if model else "default model"
    return f"🤖 using {label}"


def claude_bin() -> str:
    return config.load_config().get("claude", {}).get("bin") or shutil.which("claude") or "claude"


_guard_ready = False


def _env() -> dict:
    global _guard_ready
    if not _guard_ready:                          # install the PreToolUse safety hook once
        try:
            from .. import guard
            guard.ensure_installed()
        except Exception:
            pass
        _guard_ready = True
    env = dict(os.environ)
    tok = config.read_secret("claude_token")
    if tok:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = tok
    env["IS_SANDBOX"] = "1"  # claude's own escape hatch so bypassPermissions works as root
    # SSH from the daemon: make sure ssh finds ~/.ssh/config + the agent even if the daemon was
    # started by launchd with a thin env (else `ssh <alias>` falls back to default keys → publickey
    # denied, which past health checks mis-reported as "sandbox-blocked").
    env.setdefault("HOME", os.path.expanduser("~"))
    if "SSH_AUTH_SOCK" not in env:
        sock = _ssh_auth_sock()
        if sock:
            env["SSH_AUTH_SOCK"] = sock
    return env


def _ssh_auth_sock() -> str | None:
    """Best-effort: find the user's ssh-agent socket (launchd-spawned daemons lack SSH_AUTH_SOCK).
    macOS keeps it under /private/tmp/com.apple.launchd.*/Listeners."""
    try:
        import glob
        socks = glob.glob("/private/tmp/com.apple.launchd.*/Listeners")
        socks += glob.glob("/tmp/ssh-*/agent.*")
        return socks[0] if socks else None
    except Exception:
        return None


READONLY_TOOLS = "Read,Glob,Grep,WebFetch,WebSearch"


def _args(prompt: str, permissions: str = "full", allowed_tools: str | None = None,
          model: str | None = None, match_text: str = "") -> list[str]:
    """Per-bot tool fence (the REAL permission limit, enforced by the CLI):
       full     → bypassPermissions (full bash/file power)
       readonly → only read/search tools; cannot Bash/Write/Edit
       custom   → exactly the allowed_tools list (comma-separated)
    model: optional model override (e.g. a cheaper one for background work).
    """
    args = [claude_bin(), "-p", prompt]
    if model:
        args += ["--model", model]
    args += _project_args(match_text or prompt)   # project → CLAUDE.md + MCP, auto from the message
    if permissions == "readonly":
        args += ["--allowedTools", READONLY_TOOLS]
    elif permissions == "custom" and allowed_tools:
        args += ["--allowedTools", allowed_tools]
    else:                                        # full; IS_SANDBOX=1 unblocks bypass as root
        args += ["--dangerously-skip-permissions"]
    return args


# ---- session continuity (experimental, off by default) --------------------------------------
# Instead of rebuilding the whole prompt each turn, reuse ONE claude CLI session per day per
# identity: CREATE it once with --session-id (static persona via --append-system-prompt), then
# --resume it. Full in-session history + prompt-cache hits; we send only the per-turn dynamic
# delta (recall + skills auto-matched to THIS task + the owner's text). Wired into
# ask_async_streaming ONLY (the path both gateways call) — it already falls back to the legacy
# build_prompt path on any failure, so a broken session self-heals.

def _session_key(system: str | None) -> str:
    ident = hashlib.sha1((system or "main").encode()).hexdigest()[:8]   # scoped bots → own session
    return f"{time.strftime('%Y-%m-%d')}-{ident}"


def _session_state_path(system: str | None):
    return config.state_dir() / "sessions" / (_session_key(system) + ".json")


def _load_session_state(system: str | None) -> dict:
    try:
        return json.loads(_session_state_path(system).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"seg": 0, "turns": 0}


def _session_uuid(system: str | None, seg: int | None = None) -> str:
    if seg is None:
        seg = int(_load_session_state(system).get("seg", 0))
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"mindpalace-session-{_session_key(system)}-s{seg}"))


def _advance_session(system: str | None) -> tuple[str, bool]:
    """Called once per streamed turn. Advances the turn counter for today's session SEGMENT and,
    when the per-session turn budget (config.session_rotate_turns) is exceeded, ROTATES to a fresh
    leaner segment — a new session seeded with the persona + current CORE.md working memory (so
    distilled knowledge carries over while raw transcript bloat is shed). Returns
    (session_uuid, is_new): is_new True ⇒ CREATE (--session-id), else RESUME (--resume)."""
    st = _load_session_state(system)
    seg, turns = int(st.get("seg", 0)), int(st.get("turns", 0))
    limit = config.session_rotate_turns()
    if limit and turns >= limit:                 # budget hit → roll to a fresh, leaner segment
        seg, turns = seg + 1, 0
    turns += 1
    is_new = (turns == 1)                        # first turn of this segment → create the session
    try:
        p = _session_state_path(system)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"seg": seg, "turns": turns, "ts": time.time()}))
    except OSError:
        pass
    return _session_uuid(system, seg), is_new


def _session_system(system: str | None) -> str:
    """System prompt set ONCE at session creation: the stable persona + working memory + skills
    index. Identical across the day's turns, so claude's prompt cache hits."""
    head = system if system else system_prompt()
    blocks = [b for b in (mem.identity_block(), mem.memory_block(), skills.index_block()) if b]
    return head + (("\n\n" + "\n\n".join(blocks)) if blocks else "")


def _turn_input(text: str) -> str:
    """Per-turn user message under continuity: only query-specific dynamic context (recalled
    history + skills matched to THIS task) + the owner's text. History lives in the resumed
    session, so we don't restuff history[-12:]."""
    ctx = [b for b in (mem.recall_block(text), skills.match(text)) if b]
    return (("\n\n".join(ctx) + "\n\n") if ctx else "") + f"Owner: {text}\nAssistant:"


def _session_args(text: str, permissions: str, allowed_tools: str | None,
                  model: str | None, system: str | None) -> tuple[list[str], str]:
    """claude args for a continuity turn: CREATE (--session-id + system) or RESUME (--resume).
    _advance_session decides which (and rotates to a fresh segment when the turn budget is hit).
    Returns (args, mode) where mode is 'create' or 'resume' — for telemetry."""
    sid, is_new = _advance_session(system)
    if is_new:
        args = [claude_bin(), "-p", _turn_input(text), "--session-id", sid,
                "--append-system-prompt", _session_system(system)]
    else:
        args = [claude_bin(), "-p", _turn_input(text), "--resume", sid]
    if model:
        args += ["--model", model]
    args += _project_args(text)                    # project (auto from msg) + broad machine access
    if permissions == "readonly":
        args += ["--allowedTools", READONLY_TOOLS]
    elif permissions == "custom" and allowed_tools:
        args += ["--allowedTools", allowed_tools]
    else:                                        # full; IS_SANDBOX=1 unblocks bypass as root
        args += ["--dangerously-skip-permissions"]
    return args, ("create" if is_new else "resume")


def reset_sessions() -> int:
    """Drop today's session-segment state so the NEXT turn CREATES a fresh claude session. The
    persona/voice is baked into the session at creation, so this is how a voice switch (or any
    system-prompt change) takes effect immediately instead of next day. Knowledge is retained
    (FTS recall + CORE.md); only the in-session transcript continuity resets. Returns count."""
    d = config.state_dir() / "sessions"
    n = 0
    if d.exists():
        for f in d.glob("*.json"):
            try:
                f.unlink(); n += 1
            except OSError:
                pass
    return n


def current_session_id(system: str | None = None) -> str | None:
    """Today's claude session id for this identity IF continuity is on and the session has been
    created — so a background agent can FORK it to see the real conversation. Returns None when
    there's no live session to fork (the caller then uses its legacy, contextless path)."""
    if not config.session_continuity():
        return None
    return _session_uuid(system) if _session_state_path(system).exists() else None


def ask_sync(text: str, history: list[dict], system: str | None = None,
             permissions: str = "full", allowed_tools: str | None = None,
             model: str | None = None) -> str:
    prompt = build_prompt(text, history, system)
    if model is None:
        model = _pick_model(text)                 # Sonnet default, Opus on signal
    try:
        r = subprocess.run(_args(prompt, permissions, allowed_tools, model),
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
    "read": "reading", "search": "searching",
    "skill_find": "looking for skill", "skill_use": "found skill", "skill_run": "running skill",
    "w_user": "learning about you", "notify": "messaging you",
    "w_account": "saving", "w_infra": "noting", "w_project": "updating", "w_runbook": "writing",
    "w_log": "logging", "w_skill": "skill saved", "w_memory": "remembering", "w_note": "saving",
    "w_job": "handing off",
    "ssh": "connecting", "move": "moving", "remove": "clearing", "schedule": "scheduling",
    "git": "saving", "net": "fetching", "pkg": "installing", "run": "running",
    "service": "restarting", "fs": "setting up", "archive": "packing", "inspect": "checking",
    "bash": "working", "misc": "working",
}
# Fallback target when nothing cleaner can be pulled from the step.
_TARGET = {
    "w_account": "a login", "w_infra": "the server notes", "w_project": "the project notes",
    "w_runbook": "a runbook", "w_log": "the journal", "w_skill": "a new skill",
    "w_job": "a background task",
    "skill_find": "", "skill_use": "", "skill_run": "",   # verb already says "skill" — no redundant target
    "w_memory": "to memory", "w_note": "a note",
    "w_user": "you", "notify": "you", "read": "a file", "search": "the files",
    "ssh": "the remote machine", "move": "files into place", "remove": "old files",
    "schedule": "a timer", "git": "the changes", "net": "online", "pkg": "a dependency",
    "run": "a script", "service": "the service", "fs": "the folders", "archive": "the files",
    "inspect": "the system", "bash": "on it", "misc": "on it",
}


def _trim(s: str, n: int = 1800) -> str:
    """Tidy a live update — collapse whitespace, strip markdown bullets. Default cap is high
    (near Discord's ~1900-char limit) so the model's OWN narration sentences show IN FULL,
    never cut mid-thought. Chips pass a short n explicitly for the '· target' label."""
    s = " ".join((s or "").split()).lstrip("-*• ").strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def _classify(blk: dict) -> str:
    """Map a tool step to a category key — covers EVERY command, not just ssh, by
    looking at the verb. Never returns the raw command; just the kind of thing it is."""
    name = blk.get("name", "")
    inp = blk.get("input", {}) or {}
    fp = (inp.get("file_path", "") or "").lower()
    if name in ("Write", "Edit"):
        if "/jobs/" in fp:        return "w_job"
        if "/accounts/" in fp:    return "w_account"
        if "/infra/" in fp:       return "w_infra"
        if "/projects/" in fp:    return "w_project"
        if "/runbooks/" in fp:    return "w_runbook"
        if fp.endswith("log.md"): return "w_log"
        if "/skills/" in fp:      return "w_skill"
        if "memory" in fp:        return "w_memory"
        return "w_note"
    if name == "Read":            return "skill_use" if "/skills/" in fp else "read"
    if name in ("Grep", "Glob"):
        where = " ".join(str(inp.get(k, "")) for k in ("path", "pattern", "glob")).lower()
        return "skill_find" if "/skills/" in where or "skill" in where else "search"
    if name in ("WebFetch", "WebSearch"): return "net"
    if name == "Bash":
        c = (inp.get("command", "") or "").strip().lower()
        if "/skills/" in c:                                # running a skill's own script
            return "skill_run"
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


def _skill_in(text: str) -> str | None:
    """Pull the skill's own name out of any string containing a '.../skills/.../<name>/...'
    path — the dir just before 'scripts/' (skills/<scope>/<cat>/<name>/scripts/x.sh), else
    the last directory segment. Returns None when no skills path is present."""
    import re
    m = re.search(r"/skills/[^\s'\"]*", text or "")
    if not m:
        return None
    segs = [s for s in m.group(0).split("/") if s and s != "skills"]
    clean = lambda s: "." not in s and "*" not in s and any(ch.isalnum() for ch in s)
    if "scripts" in segs and segs.index("scripts") > 0:
        cand = segs[segs.index("scripts") - 1]
        return cand if clean(cand) else None
    dirs = [s for s in segs if clean(s)]              # drop filenames + glob wildcards
    return dirs[-1] if dirs else None


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
        if cat == "skill_find":
            pat = (inp.get("pattern") or "").strip()
            target = _skill_in(" ".join(str(inp.get(k, "")) for k in ("path", "glob"))) \
                or (pat if pat and "*" not in pat else None)   # a name, never a raw glob
        else:
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
        elif cat == "skill_run":
            target = _skill_in(cmd)              # the skill's name, not the raw script
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


_session_locks: dict = {}     # per-identity locks: serialize turns sharing one daily claude session


def _session_lock(system: str | None):
    """One lock per identity (main / each scoped bot). Continuity reuses ONE claude session per
    day per identity, and a session transcript can't take two concurrent --resume writers — so
    same-identity turns QUEUE on this lock. Distinct identities + forked sub-agents stay parallel.
    (Hermes guards its single session with a busy policy interrupt|queue|steer; this is 'queue'.)"""
    key = hashlib.sha1((system or "main").encode()).hexdigest()[:8]
    lock = _session_locks.get(key)
    if lock is None:
        lock = _session_locks[key] = asyncio.Lock()
    return lock


async def ask_async_streaming(text, history, on_progress, system=None,
                              permissions="full", allowed_tools=None, max_steps=20, model=None) -> str:
    """Run the brain with streamed events; relay live commentary via on_progress(str):
    the model's own prose lines + a Hermes-style '⚡ verb · target ✅' chip per tool step.
    Returns the final reply. Falls back to non-streaming if the stream yields nothing."""
    import json as _json
    auto = model is None
    if auto:
        model = _pick_model(text)                 # Sonnet default, Opus on signal
    final, steps, usage, mode = "", 0, {}, "legacy"
    pending = None                               # last text block, held back (may be the final answer)
    chips: dict = {}                             # tool_use id -> chip text, emitted when the step finishes
    last_chip = None                             # dedup identical back-to-back chips
    last_activity = 0.0                          # loop-clock of the last stream event (idle watchdog)
    proc = None
    # One claude session per day per identity means two parallel messages to the SAME bot would
    # both --resume the same transcript and tangle it. So same-identity turns QUEUE on a per-identity
    # lock; distinct identities (main vs scoped bots) + forked sub-agents stay fully parallel.
    # Lock only under continuity — legacy rebuilds a fresh prompt each turn, nothing shared.
    lock = _session_lock(system) if config.session_continuity() else None
    sem = _semaphore()
    sem_held = lock_held = False
    try:
        if lock is not None:
            queued = lock.locked()                   # someone's ahead → we'll wait our turn
            await lock.acquire(); lock_held = True    # queue: wait out the prior same-session turn
            if queued:                               # picked up FROM the queue → say which message
                try:
                    await on_progress("▶️ now on: " + _trim(text, 140))
                except Exception:
                    pass
        if auto:                                     # which model is active (after the queue note)
            try:
                await on_progress(_model_notice(text, model))
            except Exception:
                pass
        if config.session_continuity():           # reuse the day's claude session (cached)
            args, mode = _session_args(text, permissions, allowed_tools, model, system)
        else:                                     # legacy: rebuild the full prompt every turn
            args = _args(build_prompt(text, history, system), permissions, allowed_tools, model)
            mode = "legacy"
        args += ["--output-format", "stream-json", "--verbose"]
        await sem.acquire(); sem_held = True       # cap concurrent claude procs
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
            nonlocal final, steps, pending, last_chip, usage, last_activity
            while True:
                try:
                    raw = await proc.stdout.readline()
                except (asyncio.LimitOverrunError, ValueError):
                    # one oversized line (rare): skip it, keep streaming the rest
                    continue
                if not raw:
                    break                        # EOF
                last_activity = asyncio.get_event_loop().time()   # progress → reset idle watchdog
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
                            if _classify(blk) == "skill_use":   # telemetry for the curator
                                try:
                                    skills.bump_use(_skill_name(
                                        (blk.get("input", {}) or {}).get("file_path", "")))
                                except Exception:
                                    pass
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
                    usage = ev.get("usage", {}) or usage   # token + prompt-cache stats for telemetry
                    # `pending` (the last unfollowed text) is the final answer — never streamed.

        async def _guarded_read():
            """Run _read under an INACTIVITY watchdog: kill the turn only after `idle` seconds
            with no stream event (a real hang), not on total duration. A large hard cap backstops
            runaways. Raises TimeoutError so the existing handler reports + recovers."""
            loop = asyncio.get_event_loop()
            nonlocal last_activity
            last_activity = loop.time()
            start = last_activity
            idle = config.turn_idle_seconds()
            hard = config.turn_max_seconds()
            rt = asyncio.create_task(_read())
            while not rt.done():
                done, _ = await asyncio.wait({rt}, timeout=min(15, idle))
                if rt in done:
                    break
                now = loop.time()
                if now - last_activity > idle or (hard and now - start > hard):
                    rt.cancel()
                    try:
                        await rt
                    except asyncio.CancelledError:
                        pass
                    raise asyncio.TimeoutError
            await rt                              # surface a normal finish / propagate errors

        try:
            await _guarded_read()
        except asyncio.TimeoutError:
            if proc.returncode is None:
                proc.kill()
            idle = config.turn_idle_seconds()
            return final or (f"(stalled — no progress for {idle}s, so I stopped. "
                             "Tell me to continue, or let's break it into smaller steps.)")
        except Exception:
            # never let a stream hiccup swallow the reply (or strand the request)
            if proc.returncode is None:
                proc.kill()
            if final:
                telemetry.log_turn(mode, model, usage, steps, fallback=False)
                return final
            telemetry.log_turn(mode, model, usage, steps, fallback=True)
            return await ask_async(text, history, system, permissions, allowed_tools)
        await proc.wait()
    finally:
        if sem_held:
            sem.release()                        # ALWAYS free the permit — no leak on any path
        if lock_held:
            lock.release()                       # ALWAYS free the session — next queued turn runs
    if final:
        telemetry.log_turn(mode, model, usage, steps, fallback=False)
        return final
    # stream gave nothing (format mismatch / error) → fall back to plain capture
    telemetry.log_turn(mode, model, usage, steps, fallback=True)
    return await ask_async(text, history, system, permissions, allowed_tools)


async def ask_async(text: str, history: list[dict], system: str | None = None,
                    permissions: str = "full", allowed_tools: str | None = None,
                    model: str | None = None) -> str:
    prompt = build_prompt(text, history, system)
    if model is None:                            # explicit model (e.g. analyst) wins; else route
        model = _pick_model(text)
    async with _semaphore():                     # cap concurrent claude procs
        try:
            proc = await asyncio.create_subprocess_exec(
                *_args(prompt, permissions, allowed_tools, model), cwd=str(config.home()), env=_env(),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            out, err = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT)
            return (out.decode(errors="replace").strip()
                    or f"(empty; {err.decode(errors='replace')[:200]})")
        except asyncio.TimeoutError:
            proc.kill()
            return f"(timed out after {TIMEOUT}s — break it into smaller steps)"
        except Exception as e:
            return f"(error: {str(e)[:160]})"


async def ask_resumed(task: str, session_id: str, permissions: str = "full",
                      allowed_tools: str | None = None, model: str | None = None,
                      timeout: int | None = None) -> str:
    """Run a one-off background turn that FORKS an existing claude session — so it inherits the
    FULL conversation (cheaply, via prompt cache) WITHOUT polluting the live session. Lets the
    analyst consolidate/reflect from the real conversation instead of re-deriving from files.
    Returns the reply, or an "(error…)"/"(timed out…)"/"(empty…)" marker the caller can detect
    and fall back on. --fork-session clones the session, so the owner's live thread is untouched."""
    args = [claude_bin(), "-p", task, "--resume", session_id, "--fork-session"]
    if model:
        args += ["--model", model]
    if permissions == "readonly":
        args += ["--allowedTools", READONLY_TOOLS]
    elif permissions == "custom" and allowed_tools:
        args += ["--allowedTools", allowed_tools]
    else:                                        # full; IS_SANDBOX=1 unblocks bypass as root
        args += ["--dangerously-skip-permissions"]
    tmo = timeout or TIMEOUT                      # background jobs pass a longer cap
    async with _semaphore():                     # cap concurrent claude procs
        try:
            proc = await asyncio.create_subprocess_exec(
                *args, cwd=str(config.home()), env=_env(),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            out, err = await asyncio.wait_for(proc.communicate(), timeout=tmo)
            return (out.decode(errors="replace").strip()
                    or f"(empty; {err.decode(errors='replace')[:200]})")
        except asyncio.TimeoutError:
            proc.kill()
            return f"(timed out after {tmo}s)"
        except Exception as e:
            return f"(error: {str(e)[:160]})"
