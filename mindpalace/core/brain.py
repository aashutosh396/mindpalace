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


SELF_LEARN = f"""
SELF-LEARNING (you persist across every session — use your bash tools):
  {config.MEMORY_FILE()}   — durable facts, conventions, infra, gotchas
  {config.USER_FILE()}     — owner preferences, communication style, habits
Append a fact:  printf '\\n- %s: <fact>\\n' "$(date +%F)" >> {config.MEMORY_FILE()}
Save only durable, reusable facts — skip ephemeral/session-specific noise.
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
        "- As you work, drop SHORT, casual updates in your OWN words — a handful of words each, "
        "in the moment ('lemme ping it…', 'reachable ✅', 'noting it in your vault'). These stream "
        "to the owner live, so they read like a friend thinking out loud, not a status code. Keep "
        "them tiny and human; NEVER dump commands or paths. Your final answer is separate — give "
        "the result + next step there, and don't replay the play-by-play in it.\n"
    )


def _self_knowledge() -> str:
    h = config.home()
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


# Every kind of step gets a POOL of human phrasings, not one canned line — so even when
# the agent does the same kind of thing twice, you don't read the same words twice.
_PHRASES = {
    "w_account": ["💾 stashing that login somewhere safe", "🔐 filing those credentials away",
                  "💾 saving the account details for later"],
    "w_infra":   ["🗄 jotting down the server details", "🗄 noting how this box is set up",
                  "🖥 saving what I learned about the machine"],
    "w_project": ["📁 updating my notes on this project", "📁 keeping the project file current",
                  "🗂 tidying up the project notes"],
    "w_runbook": ["📓 writing down the steps so I remember", "📓 saving this as a runbook",
                  "📝 capturing the how-to for next time"],
    "w_log":     ["🧾 jotting this in the journal", "🧾 logging it for the record",
                  "📒 adding a line to the log"],
    "w_skill":   ["🧠 picking up a new trick", "✨ turning this into a reusable skill",
                  "🧠 learning how to do this for next time"],
    "w_memory":  ["🧠 committing this to memory", "🧠 making a mental note",
                  "🧠 remembering this for next time"],
    "w_note":    ["📝 scribbling a note", "✍️ writing that down", "📝 saving this"],
    "read":      ["📖 having a read through", "👀 taking a look at this",
                  "📖 catching up on what's in here"],
    "search":    ["🔎 digging through the files", "🔎 hunting for what I need",
                  "👀 poking around to find it", "🔍 scanning for the right bit"],
    "ssh":       ["🔌 hopping onto the server", "🔌 jumping on the box now",
                  "🛰 connecting to the remote machine"],
    "move":      ["📦 shuffling things into place", "📦 moving stuff around",
                  "🚚 putting things where they belong"],
    "remove":    ["🧹 clearing out the old stuff", "🗑 tidying up some clutter", "🧹 cleaning house"],
    "schedule":  ["⏰ wiring up a schedule", "⏰ setting it to run on its own", "🗓 putting it on a timer"],
    "git":       ["🌳 saving the changes", "🌳 committing the work", "💾 locking in the changes"],
    "net":       ["🌐 fetching something online", "🌐 pulling this off the web",
                  "📡 grabbing it from the internet", "🔗 looking it up online"],
    "pkg":       ["📦 grabbing the tools I need", "⬇️ installing a dependency",
                  "🧰 setting up what's needed"],
    "run":       ["⚙️ running the code", "🚀 firing this off", "⚙️ putting it to work"],
    "service":   ["🔄 nudging the service", "🔁 giving it a restart", "🩺 checking on the service"],
    "fs":        ["🗂 setting up the folders", "📂 getting the place ready", "🛠 laying the groundwork"],
    "archive":   ["📦 zipping things up", "🗜 packing it all together", "📦 bundling the files"],
    "inspect":   ["🩺 checking how things look", "📊 sizing up the situation",
                  "🔬 taking a quick measurement"],
    "bash":      ["🔧 working on it", "🛠 getting this done", "⚙️ handling it", "🔧 sorting this out"],
    "misc":      ["⚙️ working on it", "🛠 on it", "⚙️ handling this"],
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
    if name == "Read":            return "read"
    if name in ("Grep", "Glob"):  return "search"
    if name in ("WebFetch", "WebSearch"): return "net"
    if name == "Bash":
        c = (inp.get("command", "") or "").strip().lower()
        parts = c.split()
        first = parts[0] if parts else ""
        if first in ("sudo", "env") and len(parts) > 1:    # skip a leading sudo/env
            first = parts[1]
        if first == "ssh" or " ssh " in c:                 return "ssh"
        if first in ("scp", "rsync") or "rsync" in c:      return "move"
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


class _Narrator:
    """Turns the stream of tool steps into varied, human progress lines. Collapses a run
    of the same KIND of step (no '🔎 looking' five times), and rotates wording within each
    kind so the exact same line never lands twice — the cure for robotic, repetitive narration."""

    def __init__(self):
        self._rot: dict[str, int] = {}
        self._last_cat = None
        self._last_line = None

    def line(self, blk: dict):
        cat = _classify(blk)
        if cat == self._last_cat:
            return None                                   # collapse consecutive same-kind steps
        self._last_cat = cat
        pool = _PHRASES.get(cat) or _PHRASES["misc"]
        i = self._rot.get(cat, 0) % len(pool)
        out = pool[i]
        self._rot[cat] = i + 1
        if out == self._last_line and len(pool) > 1:      # never the exact same words twice running
            i = (i + 1) % len(pool)
            out = pool[i]
            self._rot[cat] = i + 1
        self._last_line = out
        return out


_sem = None     # caps simultaneous `claude` procs (parallel agents); set via config.concurrency()


def _semaphore():
    global _sem
    if _sem is None:
        _sem = asyncio.Semaphore(config.concurrency())   # default 8
    return _sem


async def ask_async_streaming(text, history, on_progress, system=None,
                              permissions="full", allowed_tools=None, max_steps=10) -> str:
    """Run the brain with streamed events; relay each tool step via on_progress(str).
    Returns the final reply. Falls back to non-streaming if the stream yields nothing."""
    import json as _json
    prompt = build_prompt(text, history, system)
    args = _args(prompt, permissions, allowed_tools) + ["--output-format", "stream-json", "--verbose"]
    final, steps = "", 0
    narrator = _Narrator()                       # varied, de-duped human progress lines
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
            nonlocal final, steps
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
                    content = ev.get("message", {}).get("content", [])
                    texts = [(b.get("text") or "").strip()
                             for b in content if b.get("type") == "text"]
                    texts = [x for x in texts if x]
                    tools = [b for b in content if b.get("type") == "tool_use"]
                    # Stream the model's OWN words as live commentary — but ONLY for messages
                    # that also fire a tool. A pure-text message is the final answer; it comes
                    # back via the `result` event, so streaming it would post it twice.
                    if tools:
                        emitted = False
                        for txt in texts:
                            if steps >= max_steps:
                                break
                            steps += 1
                            emitted = True
                            try:
                                await on_progress(_trim(txt))
                            except Exception:
                                pass
                        if not emitted and steps < max_steps:
                            # model acted without saying anything → one short human fallback
                            line = narrator.line(tools[0])
                            if line is not None:
                                steps += 1
                                try:
                                    await on_progress(line)
                                except Exception:
                                    pass
                elif t == "result":
                    final = ev.get("result", "") or final

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
