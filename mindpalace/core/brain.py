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
        "- NARRATE as you work: before each step, say in one short, natural line what you're "
        "doing and why (e.g. \"saving the newly discovered creds into accounts/, linking them to "
        "the repairmate project\", \"recording the VPS in infra/ and logging it\"). The owner "
        "watches these live — keep them human and specific, not robotic.\n"
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
    elif os.geteuid() != 0:                      # full; claude blocks bypass as root
        args += ["--permission-mode", "bypassPermissions"]
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


def _summ_tool(blk: dict) -> str:
    """Natural-language narration of a tool step (what it's doing, in human terms)."""
    name = blk.get("name", "tool")
    inp = blk.get("input", {}) or {}
    fp = inp.get("file_path", "") or ""
    low = fp.lower()
    if name in ("Write", "Edit") and fp:
        if "/accounts/" in low:  return f"💾 saving credentials → {_short(fp)}"
        if "/infra/" in low:     return f"🗄 recording the server → {_short(fp)}"
        if "/projects/" in low:  return f"📁 updating the project → {_short(fp)}"
        if "/runbooks/" in low:  return f"📓 writing a runbook → {_short(fp)}"
        if low.endswith("log.md"): return "🧾 logging it to LOG.md"
        if "/skills/" in low:    return f"🧠 drafting a skill → {_short(fp)}"
        if "memory" in low:      return "🧠 noting it to memory"
        return f"📝 writing {_short(fp)}"
    if name == "Bash":
        c = (inp.get("command", "") or "").strip()
        if c.startswith("ssh"):  return f"🔌 connecting: `{c[:70]}`"
        return f"🔧 running: `{c[:70]}`"
    if name == "Read":          return f"📖 reading {_short(fp)}"
    if name in ("Grep", "Glob"): return f"🔎 searching `{inp.get('pattern') or inp.get('path') or ''}`"
    if name == "WebFetch":      return f"🌐 fetching {inp.get('url', '')[:60]}"
    return f"⚙️ {name}"


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
    sem = _semaphore()
    await sem.acquire()                          # cap concurrent claude procs
    try:
        proc = await asyncio.create_subprocess_exec(
            *args, cwd=str(config.home()), env=_env(),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    except Exception as e:
        sem.release()
        return f"(error: {str(e)[:160]})"

    async def _read():
        nonlocal final, steps
        async for raw in proc.stdout:
            line = raw.decode(errors="replace").strip()
            if not line:
                continue
            try:
                ev = _json.loads(line)
            except _json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "assistant":
                for blk in ev.get("message", {}).get("content", []):
                    if steps >= max_steps:
                        break
                    bt = blk.get("type")
                    if bt == "text":
                        txt = (blk.get("text") or "").strip()
                        if txt:                       # the model's own narration
                            steps += 1
                            try:
                                await on_progress("💭 " + txt[:240])
                            except Exception:
                                pass
                    elif bt == "tool_use":
                        steps += 1
                        try:
                            await on_progress(_summ_tool(blk))
                        except Exception:
                            pass
            elif t == "result":
                final = ev.get("result", "") or final

    try:
        await asyncio.wait_for(_read(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        proc.kill()
        sem.release()
        return final or f"(timed out after {TIMEOUT}s — break it into steps)"
    await proc.wait()
    sem.release()
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
