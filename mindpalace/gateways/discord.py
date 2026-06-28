"""
Discord gateway — multi-bot with a supervising main bot.

Triggers
  MAIN bot:
    • home channel  → answers EVERY message (no mention needed) — UNLESS the message
      @mentions a scoped bot, in which case it stays quiet, MONITORS that bot, and posts
      a short report once the scoped bot finishes.
    • other channels → answers only when @mentioned.
  SCOPED bots:
    • answer only when @mentioned, in ANY channel.
    • when mentioned in the home channel, the main bot supervises + reports after.

All bots owner-locked. Each bot uses its own system.md + permission fence (the main bot
uses AGENT.md + full power). Per-bot history; shared memory. Needs mindpalace[discord].
"""
from __future__ import annotations

import asyncio
import json
import time

from ..core import brain, jobs, heartbeat, updater, notify
from .. import bots, config, scopes
from ..memory import store as mem

HEARTBEAT_AFTER = 60
KEEP = 24

# Channel-scoped personas, live. channel_id(int) -> {name, permissions, allowed_tools, system}.
# The ONE main bot answers AS this persona in this channel (own session, own history, own fence).
# Populated by run() at startup; mutated live by `!activate` / `!deactivate` (one gateway process).
_SCOPES: dict = {}


def _load(name):
    try:
        return json.loads((config.state_dir() / f"history_{name}.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(name, h):
    config.state_dir().mkdir(parents=True, exist_ok=True)
    (config.state_dir() / f"history_{name}.json").write_text(json.dumps(h[-KEEP:], indent=2))


def _chunks(s, n=1900):
    return [s[i:i + n] for i in range(0, len(s), n)] or ["(empty)"]


CORAL = 0xFF6B5C        # primary accent — the bot's embed bar, so its replies stand out from yours
YELLOW = 0xFFC861       # health-check card bar (distinct from coral replies)
_ACCENT_COLOR = {"cyan": YELLOW, "yellow": YELLOW, "green": 0x7BD88F, "red": 0xFF5370, "blue": 0x5FAFFF}


def _embed_chunks(s, n=4000):
    """Split a reply onto embed-description-sized pieces (cap 4096), breaking on line boundaries
    and BALANCING ``` fences so a code block split across cards stays valid on both sides."""
    out, cur = [], ""
    for line in (s or "").splitlines(keepends=True):
        if cur and len(cur) + len(line) > n:
            out.append(cur); cur = ""
        cur += line
    if cur:
        out.append(cur)
    fixed, carry = [], ""
    for ch in out:
        body = carry + ch
        carry = ""
        if body.count("```") % 2:            # left a fence open → close here, reopen next card
            body += "\n```"
            carry = "```\n"
        fixed.append(body[:4096])
    return fixed or ["(empty)"]


from ..theme import (fmt_dur as _fmt_dur, cook_verb as _cook_verb, cook_emoji as _cook_emoji,
                     cook_hint as _cook_hint, bar_fill as _bar, random_verb_offset as _verb_offset)

# Smart steering: classify a message that arrives WHILE the bot is mid-task.
_CORRECTION_KW = ("wait", "no,", "no ", "actually", "instead", "stop", "scratch that", "hold on",
                  "nvm", "never mind", "don't ", "do not ", "cancel that", "ignore that", "rather",
                  "not that", "change of plan", "forget that")
_FOLLOWUP_KW = ("also", "and also", "plus", "as well", "make sure", "oh and", "one more", "add ",
                "+ ", "btw", "by the way", "while you", "include", "and can you", "and please",
                "don't forget", "additionally")
_STEER_EARLY_SECS = 25       # "early" in the task → an addition is worth interrupting for


_BG_KW = ("in the background", "in the bg", "in parallel", "background this", "bg:", "on the side",
          "at the same time", "meanwhile", "in the meantime", "don't wait", "do not wait",
          "asynchronously", "as a side task", "run it in background", "while you")


def _wants_background(text: str) -> bool:
    """Owner explicitly wants this run in PARALLEL (not queued/blocking). Heuristic, no model call."""
    low = (text or "").lower()
    return any(k in low for k in _BG_KW)


# imperative "grind until done" phrases — only honored when the message is NOT a question
_GOAL_UNTIL = ("keep working until", "keep going until", "keep iterating until", "loop until",
               "iterate until", "don't stop until", "do not stop until", "until it's done",
               "until it is done", "until all tests pass", "until tests pass", "until it works")
_Q_STARTS = ("how", "what", "why", "did", "do", "does", "can", "could", "is", "are", "was",
             "were", "when", "where", "who", "which", "explain", "tell", "should", "would", "will")


def _wants_goal(text: str) -> tuple[bool, str]:
    """Detect an EXPLICIT ralph-wiggum GOAL-LOOP request — GATED so a casual mention ("how does the
    ralph loop work?", "explain the goal loop") never triggers it. Fires ONLY on:
      • a `goal:` / `ralph:` PREFIX,
      • an ALL-CAPS `GOAL` standalone token (the owner deliberately flags it),
      • a quoted "goal",
      • an unambiguous 'keep going until …' imperative that is NOT a question.
    Returns (yes, task). Heuristic, no model call."""
    import re
    t = (text or "").strip()
    low = t.lower()
    if low.startswith(("goal:", "ralph:")):                       # canonical explicit form
        return True, t.split(":", 1)[1].strip()
    if re.search(r"\bGOAL\b", t):                                 # ALL-CAPS GOAL marker
        return True, (re.sub(r"\bGOAL\b", "", t).strip(" :-—") or t)
    if re.search(r"""['"‘’“”]\s*goal\s*['"‘’“”]""", low):
        return True, t                                            # quoted "goal"
    first = low.split()[0] if low.split() else ""
    is_question = low.endswith("?") or first in _Q_STARTS
    if not is_question and any(k in low for k in _GOAL_UNTIL):    # imperative, not a question
        return True, t
    return False, ""


# Merged background-task panel, per channel: one live message listing ALL running bg tasks
# (label + timer + bar), kept at the bottom; completed ones drop off and post their own ✅ + summary.
_BG: dict = {}                # channel_id -> {channel, tasks:{tid:{label,t0}}, msg, ticker, done:[]}
_BG_SEQ = [0]


def _bg_state(channel):
    s = _BG.get(channel.id)
    if s is None:
        s = _BG[channel.id] = {"channel": channel, "tasks": {}, "msg": None, "ticker": None, "done": []}
    return s


def _bg_render(s):
    if not s["tasks"]:
        return None
    lines = [f"🛠️ **background** · {len(s['tasks'])} running"]
    for t in s["tasks"].values():
        el = time.monotonic() - t["t0"]
        lines.append(f"⏳ {t['label']} · {_fmt_dur(el)}  {_bar(el)}")
    return "\n".join(lines)


async def _bg_paint(s):
    """Post/refresh the merged panel; re-post at the bottom if buried; remove it when empty."""
    ch, body = s["channel"], _bg_render(s)
    try:
        if body is None:
            if s["msg"] is not None:
                try:
                    await s["msg"].delete()
                except Exception:
                    pass
                s["msg"] = None
            return
        if s["msg"] is None:
            s["msg"] = await ch.send(body)
        elif ch.last_message_id not in (None, s["msg"].id):   # buried → repost at bottom (no API for the check)
            old, s["msg"] = s["msg"], None
            s["msg"] = await ch.send(body)
            try:
                await old.delete()
            except Exception:
                pass
        else:
            await s["msg"].edit(content=body)
    except Exception:
        pass


async def _bg_ticker(s):
    while s["tasks"]:
        await asyncio.sleep(2.0)
        await _bg_paint(s)
    await _bg_paint(s)            # final pass → clears the panel when the last one finishes
    s["ticker"] = None


def _steer_kind(new: str) -> str:
    """Heuristic: a mid-task message is a 'correction' (steer/stop), an 'addition' (do this too),
    or a 'new' topic (queue separately). Fast + free; no model call."""
    low = " " + (new or "").strip().lower()
    if any(k in low for k in _CORRECTION_KW):
        return "correction"
    if any(k in low for k in _FOLLOWUP_KW):
        return "addition"
    return "new"


async def _post_health_card(channel, title, body, accent="yellow"):
    """Health/curation report as a CARD (same style as a reply; end-bar = the tally), colored per
    accent (yellow for health). Markdown renders in an embed, but md tables don't — align first."""
    from ..core import notify as _n
    import re as _re
    b = _n.prettify_tables((body or "").strip())
    m = _re.search(r"✓\s*(\d+)\s*⚠\s*(\d+)\s*✗\s*(\d+)", b)
    stats = f"{m.group(1)} ✓ · {m.group(2)} ⚠ · {m.group(3)} ✗" if m else "done"
    try:
        icon = channel.guild.me.display_avatar.url
    except Exception:
        icon = None
    await _send_reply(channel, title, b, icon, stats=stats,
                      color=_ACCENT_COLOR.get(accent, YELLOW), header=title)


async def _send_reply(channel, name, reply, icon_url=None, stats=None, color=CORAL, header=None):
    """Send a card-style reply: a left-bar embed with a header at the TOP and an 'end' bar at the
    BOTTOM (doubles as a summary: model · duration, or a health tally). `color` sets the bar (coral
    for replies, yellow for health). `header` overrides the '🤖 <name>' top line. Long replies →
    multiple cards; header on first, footer on last."""
    import discord
    head = header or f"🤖 {name}"
    chunks = _embed_chunks(reply)
    last = len(chunks) - 1
    for i, c in enumerate(chunks):
        em = discord.Embed(description=c, color=color)
        if i == 0:
            try:
                em.set_author(name=head, icon_url=icon_url) if icon_url \
                    else em.set_author(name=head)
            except Exception:
                em.set_author(name=head)
        if i == last:
            label = f"{name} · {stats}" if stats else f"end of {name}'s reply"
            bar = "━" * (12 if stats else 24)
            try:
                em.set_footer(text=f"{bar}  {label}  {bar}", icon_url=icon_url) if icon_url \
                    else em.set_footer(text=f"{bar}  {label}  {bar}")
            except Exception:
                em.set_footer(text=f"{bar}  {label}  {bar}")
        try:
            await channel.send(embed=em)
        except discord.Forbidden:
            # channel doesn't grant this bot "Embed Links" → plain-text fallback so the reply
            # still lands (common in a freshly-activated channel before perms are widened).
            prefix = f"**{head}**\n" if i == 0 else ""
            for part in _chunks(prefix + c):
                await channel.send(part)


import re as _re
from pathlib import Path as _Path
_ATTACH_RE = _re.compile(r'^[ \t]*(?:📎[ \t]*)?ATTACH:[ \t]*(.+?)[ \t]*$', _re.M)


def _extract_attachments(text):
    """Pull `📎ATTACH: /path` lines out of the reply → (clean_text, [existing file paths]).
    Lets the agent attach a rendered table image / CSV / file for data that's hard to read inline."""
    files = []
    for m in _ATTACH_RE.finditer(text or ""):
        p = m.group(1).strip().strip('`"\'')
        fp = _Path(p).expanduser()
        if p and fp.is_file():
            files.append(str(fp))
    clean = _ATTACH_RE.sub("", text or "").strip()
    return clean, files


_IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic")


async def _save_attachments(msg) -> list[dict]:
    """Download ALL attachments (images AND any other file — pem, pdf, csv, code, …) to
    state/incoming/ and return their local paths. The brain then reads them with its file
    tools: images via Read's viewer, everything else via Read/bash — so it can actually
    handle what the owner sent instead of saying the attachment didn't load."""
    out = []
    for a in getattr(msg, "attachments", []):
        ct = (a.content_type or "").lower()
        name = a.filename or "file"
        is_img = ct.startswith("image/") or name.lower().endswith(_IMG_EXT)
        dest = config.state_dir() / "incoming"
        dest.mkdir(parents=True, exist_ok=True)
        p = dest / f"{msg.id}_{name}"
        try:
            await a.save(str(p))
            out.append({"path": str(p), "name": name, "is_image": is_img})
        except Exception:
            pass
    return out


_REFLECT_KEYWORDS = ("ssh", "login", "log in", "password", "passwd", "cred", "secret", "token",
                     "api key", "apikey", "deploy", "server", "vps", "host", "port", "database",
                     " db ", "project", "webhook", "domain", "dns", "access", "setup", "set up",
                     "install", "configure", "connect", "backup", "restart", "migrate", "scrape",
                     "create", "build", "fix", "cron", "schedule")


def _worth_reflecting(text, reply):
    # substantial work, or anything that smells like a procedure/resource worth capturing
    blob = (text + " " + reply).lower()
    return len(reply) > 300 or any(k in blob for k in _REFLECT_KEYWORDS)


def _bump_counter(name) -> int:
    """Persisted per-bot exchange counter (survives restarts) — drives compaction cadence."""
    p = config.state_dir() / f"cmds_{name}.txt"
    try:
        n = int(p.read_text().strip()) + 1
    except (FileNotFoundError, ValueError):
        n = 1
    try:
        p.write_text(str(n))
    except OSError:
        pass
    return n


def _memory_heavy() -> bool:
    """Only bother compacting once a file is getting full (>60% of its budget)."""
    def size(path):
        try:
            return len(path.read_text())
        except OSError:
            return 0
    return (size(config.USER_FILE()) > 0.6 * config.user_budget()
            or size(config.MEMORY_FILE()) > 0.6 * config.memory_budget())


async def _compact(channel, system=None):
    """Background distillation of USER.md + MEMORY.md. Posts a short note when it tightened something.
    Forks the day's live session (when continuity is on) so it consolidates from the real chat."""
    from ..agents import analyst
    try:
        out = await analyst.compact(session_id=brain.current_session_id(system))
        if out and out.strip().upper() not in ("NOTHING", ""):
            await channel.send(f"_🧠 {out.strip()[:200]}_")
    except Exception:
        pass


async def _reflect(channel, text, reply):
    """SILENT background Analyst — reasons, files facts + skillifies. Never posts to chat
    (it works in the background, quietly making the agent smarter)."""
    from ..agents import analyst
    try:
        out = await analyst.reflect(text, reply)
        if out and out.strip().upper() not in ("NOTHING", ""):
            print(f"[analyst] {out.strip()[:200]}")     # to daemon log only
    except Exception:
        pass


def _ids_from(msg, parts):
    """User IDs from @mentions (preferred) or raw numeric args."""
    ids = [m.id for m in msg.mentions if not m.bot]
    ids += [int(p) for p in parts if p.isdigit()]
    return list(dict.fromkeys(ids))


def _extract_plan(raw: str, valid_names: set) -> list:
    """Pull the orchestrator's JSON plan out of its reply: a list of {room, task}, keeping only
    items that target a real room. Tolerant of prose around the JSON (claude often wraps it)."""
    if not raw:
        return []
    m = _re.search(r"\[.*\]", raw, _re.S)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except Exception:
        return []
    out = []
    for it in arr if isinstance(arr, list) else []:
        if isinstance(it, dict) and it.get("room") in valid_names and it.get("task"):
            out.append({"room": it["room"], "task": str(it["task"]).strip()})
    return out


def _extract_arch_plan(raw: str) -> list:
    """Parse the architect's plan: [{role, task, room?}]. room is optional (route to a real room
    if named, else run as an ephemeral agent). Tolerant of prose around the JSON."""
    if not raw:
        return []
    m = _re.search(r"\[.*\]", raw, _re.S)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except Exception:
        return []
    out = []
    for it in arr if isinstance(arr, list) else []:
        if isinstance(it, dict) and it.get("task"):
            out.append({"role": str(it.get("role") or "agent").strip()[:40],
                        "task": str(it["task"]).strip(),
                        "room": it["room"] if isinstance(it.get("room"), str) else None})
    return out


def _augment_with_attachments(text: str, atts: list) -> str:
    """Append a note pointing the brain at saved attachment paths. Attachments are saved to a
    LOCAL path on the box, so any turn (home OR another room) can Read them — the note carries
    the paths into whichever room handles the message (fixes images lost on cross-room dispatch)."""
    if not atts:
        return text
    imgs = [a for a in atts if a["is_image"]]
    files = [a for a in atts if not a["is_image"]]
    notes = []
    if imgs:
        notes.append("VIEW these image(s) with the Read tool: " + ", ".join(a["path"] for a in imgs))
    if files:
        notes.append("READ/process these file(s) with the Read tool or bash (they are saved "
                     "locally): " + ", ".join(f'{a["name"]} -> {a["path"]}' for a in files))
    return (text or "(no caption)") + (
        "\n\n[The owner attached files. " + " | ".join(notes)
        + ". Open them before replying — don't say the attachment didn't load.]")


async def _handle_command(msg, text) -> bool:
    """Admin commands (home channel). Returns True if it was a command."""
    parts = text[1:].split()
    if not parts:
        return False
    cmd, args = parts[0].lower(), parts[1:]
    if cmd == "help":
        await msg.channel.send(
            "**Commands** (admins only, here in the home channel):\n"
            "`!help` — show this list\n"
            "`!stop` — 🛑 EMERGENCY STOP: kill whatever I'm running right now (a runaway task / "
            "context blowup). I stay online — it just halts the current work.\n"
            "`!update check` — check GitHub for updates right now (just shows them)\n"
            "`!update` — pull the latest from GitHub + reload myself live\n"
            "`!bg` (or `!tasks`) — list running + recently-done background tasks in this channel\n"
            "`goal: <task>` (or `GOAL <task>`, or 'keep going until …') — I grind on it (ralph loop) in the "
            "background until done. Just *mentioning* 'goal'/'loop'/'ralph' in a question won't trigger it.\n"
            "`!project <path>` — PIN a project (otherwise I auto-detect it from your message via the vault); `!project none` to unpin\n"
            "`!mcp` — list MCP servers (✓=on); `!mcp enable <slug> KEY=val` / `!mcp disable <slug>` / `!mcp info <slug>`\n"
            "`!architect <goal>` — team on demand, ANY channel, no setup: I split the goal into "
            "parallel agents (routing to real rooms if they fit, else spawning ephemeral ones), run "
            "them at once, and merge into one answer. Simple goal = just answered.\n"
            "`#room <task>` — from here, send a task INTO an activated room; it runs there as that "
            "room's assistant and reports a one-liner back here (command the fleet from home).\n"
            "`!activate #channel <what it does>` — turn another channel into its OWN assistant "
            "(own session, own memory, persona drafted by me); add `readonly`/`full`/`custom` for its "
            "powers and `opus`/`sonnet`/`haiku` to pin its model (cheaper = run more in parallel). "
            "`!scopes` lists them · `!deactivate #channel` turns one off.\n"
            "`!activate #channel orchestrator <goal focus>` — make a room that SPLITS a goal across the "
            "other rooms, runs them in parallel, and MERGES the results. Then just talk to that room.\n"
            "`!bots` — list the bots I'm running\n"
            "`!admins` — who can talk to me\n"
            "`!add-admin @user` — let someone in\n"
            "`!remove-admin @user` — revoke access\n"
            "`!add-webhook <name> <url>` — add a notify webhook\n"
            "`!model opus` — switch my model (sonnet/opus/haiku); `!model` shows current\n"
            "`!heartbeat scan-now` — run a health check right now; `!heartbeat 30` — set the interval "
            "in minutes (0 = off); `!heartbeat` shows current\n"
            "`!curate now` — tidy my skill library now; `!curate pause`/`resume`; `!curate` shows status\n"
            "`!voice lean` / `!voice full` — switch my reply style (brief vs chatty); `!voice` shows current\n"
            "\nEverything else you say just goes straight to me — no command needed.")
    elif cmd in ("heartbeat", "hb"):
        sub = args[0].lower() if args else ""
        if sub in ("scan-now", "scan", "now", "run"):
            await msg.channel.send("🔍 running a health check right now — one sec…")
            async def _rep(m):
                await msg.channel.send(m)
            async def _scan_card(title, body, accent):
                await _post_health_card(msg.channel, title, body, accent)
            try:
                out = await heartbeat.run_once(_rep, card=_scan_card)   # yellow card → this channel
                if not out:
                    await msg.channel.send("💓 scan done — all quiet, nothing to flag.")
            except Exception as e:
                await msg.channel.send(f"⚠️ scan failed: {e}")
        elif args and args[0].lstrip("-").isdigit():
            n = max(0, int(args[0]))
            cfg = config.load_config(); cfg["heartbeat_minutes"] = n; config.save_config(cfg)
            await msg.channel.send(
                f"💓 heartbeat set to every **{n} min** — applies next cycle, no restart needed."
                if n else "💓 heartbeat turned **off**.")
        else:
            n = config.heartbeat_minutes()
            await msg.channel.send(
                f"💓 heartbeat: every **{n} min** (0 = off). Full report → **{config.heartbeat_webhook()}** "
                f"channel, short note here. `!heartbeat scan-now` to run one immediately · "
                f"`!heartbeat <minutes>` to change the interval.")
    elif cmd in ("voice", "tone"):
        sub = args[0].lower() if args else ""
        if sub in ("lean", "brief", "terse"):
            cfg = config.load_config(); cfg["lean_voice"] = True; config.save_config(cfg)
            brain.reset_sessions()
            await msg.channel.send("🪶 voice → **lean** (brief, to-the-point). Live from your next message.")
        elif sub in ("full", "chatty", "rich"):
            cfg = config.load_config(); cfg["lean_voice"] = False; config.save_config(cfg)
            brain.reset_sessions()
            await msg.channel.send("💬 voice → **full** (chatty, high-personality). Live from your next message.")
        else:
            await msg.channel.send(
                f"voice: **{'lean' if config.lean_voice() else 'full'}** · "
                "`!voice lean` (brief) / `!voice full` (chatty) — applies on your next message.")
    elif cmd == "mcp":
        from .. import mcp as reg
        sub = args[0].lower() if args else "list"
        en = reg.enabled()
        if sub in ("list", "ls"):
            lines = [f"**MCP servers** ({len(reg.catalog())}) — ✓ = wired in:"]
            for c in reg.catalog():
                m = "✓" if c["slug"] in en else "▫️"
                lines.append(f"{m} `{c['slug']}` — {c['description'][:46]}")
            lines.append("`!mcp enable <slug> KEY=val` · `!mcp disable <slug>` · `!mcp info <slug>`")
            buf = ""
            for ln in lines:
                if len(buf) + len(ln) > 1800:
                    await msg.channel.send(buf); buf = ""
                buf += ln + "\n"
            if buf:
                await msg.channel.send(buf)
        elif sub == "info":
            c = reg.get(args[1]) if len(args) > 1 else None
            if not c:
                await msg.channel.send("usage: `!mcp info <slug>`")
            else:
                import json as _j
                await msg.channel.send(
                    f"**{c['name']}** (`{c['slug']}`) · {c['category']}\n{c['description']}\n"
                    f"env: {', '.join(c['env']) or 'none'} · {c['homepage']}\n"
                    f"```json\n{_j.dumps(c['config'], indent=2)[:1200]}\n```")
        elif sub == "enable":
            if not args[1:]:
                await msg.channel.send("usage: `!mcp enable <slug> [KEY=val ...]`  (tip: set secrets via "
                                       "the terminal `mindpalace mcp enable` to keep keys out of chat)")
            else:
                slug = args[1].lower()
                kv = {t.split("=", 1)[0]: t.split("=", 1)[1] for t in args[2:] if "=" in t}
                if not reg.enable(slug, kv or None):
                    await msg.channel.send(f"no server `{slug}` — `!mcp list`")
                else:
                    miss = reg.missing_env(slug)
                    await msg.channel.send(f"✅ enabled `{slug}`." + (f" still needs: {', '.join(miss)}"
                        if miss else " ready.") + " (restart to wire it into running turns)")
        elif sub == "disable":
            if not args[1:]:
                await msg.channel.send("usage: `!mcp disable <slug>`")
            else:
                reg.disable(args[1].lower()); await msg.channel.send(f"disabled `{args[1].lower()}`.")
        else:
            await msg.channel.send("`!mcp` · `!mcp info <slug>` · `!mcp enable <slug> KEY=val` · `!mcp disable <slug>`")
    elif cmd in ("curate", "curator"):
        sub = args[0].lower() if args else "status"
        if sub in ("now", "run", "force"):
            await msg.channel.send("🧹 running skill curation now — one sec…")
            async def _rep(m):
                await msg.channel.send(m)
            async def _cur_card(title, body, accent):
                await _post_health_card(msg.channel, title, body, accent)
            try:
                out = await heartbeat.run_curation(_rep, force=True, card=_cur_card)
                if not out or out.strip().upper() in ("NOTHING", ""):
                    await msg.channel.send("🧹 curation done — library already tidy, nothing to change.")
            except Exception as e:
                await msg.channel.send(f"⚠️ curation failed: {e}")
        elif sub in ("pause", "off"):
            config.set_curator_paused(True)
            await msg.channel.send("⏸️ skill curation **paused** — no auto-tidy until you `!curate resume`.")
        elif sub in ("resume", "on"):
            config.set_curator_paused(False)
            await msg.channel.send("▶️ skill curation **resumed** — back on the idle + 7-day gate.")
        else:                                        # status
            import time
            st = config.curator_state()
            ago = "never" if not st["last_run"] else f"{(time.time() - st['last_run']) / 86400:.1f}d ago"
            idle_disp = "∞" if config.idle_seconds() > 1e8 else f"{config.idle_seconds() / 60:.0f}m"
            await msg.channel.send(
                "🧹 **Skill curation**\n"
                f"- state: {'⏸️ paused' if st['paused'] else '▶️ active'}\n"
                f"- runs: {st['run_count']} · last: {ago}\n"
                f"- gate: idle ≥ {config.curator_idle_minutes()}m (now {idle_disp} idle) · ≥7 days apart\n"
                + (f"- last note: _{st['last_summary']}_\n" if st["last_summary"] else "")
                + "`!curate now` to run now · `!curate pause` / `!curate resume`")
    elif cmd in ("stop", "halt", "abort", "kill"):
        import os
        from ..core import service
        n = service.kill_descendants(os.getpid())   # kill my worker procs; I (the bot) stay alive
        await msg.channel.send(f"🛑 halted {n} running process(es) — current work stopped. I'm still here."
                               if n else "🛑 nothing was running.")
    elif cmd in ("update", "upgrade") or (cmd == "mindpalace" and args[:1] == ["update"]):
        # `!update check` → just LOOK (no pull); `!update` → pull + reload live.
        sub = (args[1] if cmd == "mindpalace" and len(args) > 1 else args[0] if args else "").lower()
        if sub in ("check", "status", "?", "available"):
            await msg.channel.send("🔍 checking GitHub for updates right now…")
            info = await asyncio.to_thread(updater.check)
            if not info:
                await msg.channel.send("✅ up to date — you're on the latest. Nothing to pull.")
            else:                                    # arm the "yes" reply, then show the changelog
                updater.write_pending({"remote_sha": info["remote_sha"], "behind": info["behind"]})
                await msg.channel.send(updater.notice_text(info))
            return True
        await msg.channel.send("🔄 on it — grabbing the latest and reloading myself, back in a few secs…")
        result = await asyncio.to_thread(updater.accept)
        await msg.channel.send(result)
    elif cmd in ("bg", "tasks", "background"):
        s = _BG.get(msg.channel.id)
        running = list((s or {}).get("tasks", {}).values())
        done = (s or {}).get("done", [])
        lines = []
        if running:
            lines.append(f"🛠️ **running ({len(running)})**")
            for t in running:
                lines.append(f"• {t['label']} · {_fmt_dur(time.monotonic() - t['t0'])}")
        if done:
            lines.append(f"✅ **recently done ({len(done)})**")
            for lbl, dur in reversed(done[-5:]):
                lines.append(f"• {lbl} · {dur}")
        await msg.channel.send("\n".join(lines) if lines else "no background tasks here.")
    elif cmd in ("project", "proj"):
        if args:
            if args[0].lower() in ("none", "clear", "off"):
                config.set_active_project("")
                await msg.channel.send("📁 active project cleared — vault only.")
            else:
                import os as _os
                p = config.set_active_project(" ".join(args))
                ok = _os.path.isdir(p)
                await msg.channel.send(
                    f"📁 active project → `{p}`{'' if ok else '  ⚠️ path not found yet'}\n"
                    "I now read its CLAUDE.md + MCP from anywhere (cwd stays the vault, guard intact).")
        else:
            await msg.channel.send(
                f"📁 active project: `{config.active_project() or '(none — vault only)'}`\n"
                "set with `!project <path>` · clear with `!project none`")
    elif cmd == "admins":
        a = config.admins()
        await msg.channel.send("admins: " + (", ".join(f"<@{i}>" for i in a) or "none"))
    elif cmd == "add-admin":
        added = [i for i in _ids_from(msg, args) if config.add_admin(i)]
        await msg.channel.send("added " + ", ".join(f"<@{i}>" for i in added)
                               if added else "nothing added — @mention a user or give an ID")
    elif cmd == "remove-admin":
        gone = [i for i in _ids_from(msg, args) if config.remove_admin(i)]
        await msg.channel.send("removed " + ", ".join(f"<@{i}>" for i in gone)
                               if gone else "not an admin")
    elif cmd in ("activate", "scope", "add-scope"):
        # `!activate #channel [readonly|full|custom] <what it should do>`
        # Turn another channel into its own assistant — own session, own memory, own persona
        # (drafted live by Claude), all on THIS one bot. No new Discord app/token.
        target = msg.channel_mentions[0] if msg.channel_mentions else None
        rest = [a for a in args if not a.startswith("<#")]
        if not target:                                   # allow a raw numeric id too
            cid0 = scopes.resolve_channel(rest[0]) if rest else None
            if cid0:
                target = msg.guild.get_channel(cid0) if msg.guild else None
                rest = rest[1:]
        if not target:
            await msg.channel.send("usage: `!activate #channel [readonly|full|custom] <what it should do>` "
                                   "— mention the channel to turn into its own assistant.")
            return True
        if target.id == msg.channel.id:
            await msg.channel.send("that's the home channel — pick a *different* channel to activate.")
            return True
        tier, is_orch, model = "full", False, None
        while rest:                                  # consume leading keywords in any order
            t = rest[0].lower()
            if t == "orchestrator":
                is_orch = True; rest = rest[1:]      # a room that fans out + merges
            elif t in ("readonly", "full", "custom"):
                tier = t; rest = rest[1:]            # the tool fence
            elif t in ("opus", "sonnet", "haiku"):
                model = t; rest = rest[1:]           # pin this room's model (cost control)
            else:
                break
        intent = " ".join(rest).strip()
        if is_orch and not intent:
            intent = ("Coordinate the other activated rooms: take the owner's goal, split it across "
                      "the best-suited rooms, and merge their results into one clear answer.")
        if not intent:
            await msg.channel.send("tell me what that channel's assistant should do, e.g. "
                                   "`!activate #deploy handle deploys and read logs only`.")
            return True
        await msg.channel.send(f"🧬 activating <#{target.id}> — drafting its persona with Claude…")
        try:
            persona = await asyncio.to_thread(scopes.draft_persona, intent)
            name = (target.name or f"chan{target.id}").replace(" ", "-")
            allowed = ("Read" if tier == "custom" else None)
            scopes.add_scope(name, target.id, system=persona, permissions=tier,
                             allowed_tools=allowed, orchestrator=is_orch, model=model)
            spec = {"name": name, "permissions": tier, "allowed_tools": allowed, "system": persona}
            if is_orch:
                spec["orchestrator"] = True
            if model:
                spec["model"] = model
            _SCOPES[target.id] = spec
        except Exception as e:
            await msg.channel.send(f"⚠️ couldn't activate: {e}"); return True
        prev = persona.strip().replace("\n", " ")[:300]
        mtag = f" · {model}" if model else ""
        kind = ("🧭 ORCHESTRATOR room (fans out to the other rooms + merges)" if is_orch
                else f"its own assistant **{name}** ({tier})") + mtag
        await msg.channel.send(
            f"✅ <#{target.id}> is now {kind} — its own session, memory and persona. "
            f"Live now, no restart.\n> _{prev}…_\n"
            f"Edit its persona anytime: `scopes/{name}/system.md` · turn off: `!deactivate <#{target.id}>`")
    elif cmd in ("deactivate", "remove-scope", "unscope"):
        target = msg.channel_mentions[0] if msg.channel_mentions else None
        cid = target.id if target else (scopes.resolve_channel(args[0]) if args else None)
        if not cid:
            await msg.channel.send("usage: `!deactivate #channel` (or the channel id)"); return True
        scopes.remove(cid); _SCOPES.pop(cid, None)
        await msg.channel.send(f"🔌 turned off — <#{cid}> is no longer an assistant channel. "
                               "(its history is kept on disk.)")
    elif cmd in ("scopes", "channels"):
        if not _SCOPES:
            await msg.channel.send("no activated channels yet — `!activate #channel <what it does>`.")
        else:
            await msg.channel.send("**activated channels** (each its own assistant):\n" + "\n".join(
                f"• <#{cid}> → **{s['name']}** "
                + ("🧭 orchestrator" if s.get("orchestrator") else f"({s.get('permissions','?')}"
                   + (f", allow={s['allowed_tools']}" if s.get('allowed_tools') else "") + ")")
                + (f" · {s['model']}" if s.get("model") else "")
                for cid, s in _SCOPES.items()))
    elif cmd == "bots":
        reg = bots.registry()
        await msg.channel.send("\n".join(
            f"• {n}: {b.get('permissions','?')} / {b.get('trigger','?')}"
            for n, b in reg.items()) or "no bots")
    elif cmd == "add-webhook":
        if len(args) >= 2:
            config.set_webhook(args[0], args[1])
            await msg.channel.send(f"webhook `{args[0]}` saved")
        else:
            await msg.channel.send("usage: `!add-webhook <name> <url>`")
    elif cmd == "model":
        if args:
            val = config.set_main_model(args[0])
            if val is None:
                await msg.channel.send("usage: `!model sonnet|opus|haiku|<full-id>|default`")
            else:
                await msg.channel.send(
                    f"🧠 model → **{val}** (effective next reply). "
                    f"`think hard` / `use opus` still bumps to {config.power_model()} just for that turn.")
        else:
            await msg.channel.send(
                f"current: **{config.main_model() or '(CLI default)'}** · power: {config.power_model()} "
                f"· background: {config.background_model()}\nswitch with `!model sonnet|opus|haiku`")
    else:
        await msg.channel.send(f"unknown command `{cmd}` — try `!help`")
    return True


def run():
    try:
        import discord
    except ImportError:
        raise SystemExit('Discord gateway needs discord.py — run:  pip install "mindpalace[discord]"')

    cfg = config.load_config()
    dcfg = cfg.get("discord", {})
    home_channel = int(dcfg.get("home_channel", 0))
    registry = cfg.get("bots", {}) or {"main": {"permissions": "full", "trigger": "home"}}

    _SCOPES.clear()                              # load activated channels (own persona/session each)
    _SCOPES.update(scopes.active_map())
    if _SCOPES:
        print(f"[scopes] {len(_SCOPES)} activated channel(s): "
              + ", ".join(s["name"] for s in _SCOPES.values()))

    clients: dict[str, "discord.Client"] = {}   # name -> client
    scoped_ids: set[int] = set()                 # user-ids of non-main bots (for mention checks)
    turn_locks: dict = {}                        # per-bot: serialize a WHOLE turn (work + reply post)
    active: dict = {}                            # per-bot live turn state (for smart steering)

    async def _do_turn(channel, name, text, system, perms, allowed, model=None):
        """Drive one bot's brain; STREAM its steps live; reply; persist; file in background.
        model: per-room/per-agent model override (None → brain auto-picks Sonnet/Opus)."""
        history = _load(name)
        t0 = time.monotonic()

        # ONE live status message: ⚡ chips stack into it AND it shows a ticking timer ("⏳ 0m12s ·
        # thinking…") that a background ticker bumps every few seconds — so a long quiet stretch
        # reads as ALIVE, not stuck. Prose lines commit the current block, then post on their own.
        st = {"chips": [], "msg": None, "active": True}
        voff = _verb_offset()                    # this turn starts on a random verb

        def _body():
            el = time.monotonic() - t0
            emoji, verb, timer, hint = (_cook_emoji(el, offset=voff), _cook_verb(el, offset=voff),
                                        _fmt_dur(el), _cook_hint(el))
            head = f"{emoji} {verb} ({timer} · {hint})"   # the loader goes on its OWN line below
            bar = _bar(el)
            if st["chips"]:
                return "\n".join([f"> {c}" for c in st["chips"]] + [f"> {head}", f"> {bar}"])
            return f"{head}\n{bar}"

        async def _paint():
            try:
                if st["msg"] is None:
                    st["msg"] = await channel.send(_body())
                else:
                    await st["msg"].edit(content=_body())
            except Exception:
                pass

        async def _ticker():                            # heartbeat: move the pulse + bump timer
            while st["active"]:
                await asyncio.sleep(1.5)                 # lively but safe vs Discord edit limits
                if st["active"]:
                    await _paint()

        async def on_progress(line):
            try:
                if line[:1] in ("⚡", "📚"):       # step chip (⚡) or skill chip (📚) → stack
                    st["chips"].append(line)
                    await _paint()
                else:                                   # prose / 🤖 notice → freeze block, post on its own
                    if st["msg"] is not None and st["chips"]:
                        await st["msg"].edit(content="\n".join(f"> {c}" for c in st["chips"]))
                    st["chips"], st["msg"] = [], None
                    await channel.send(f"_{line}_")
            except Exception:
                pass

        ticker = asyncio.create_task(_ticker())
        try:
            async with channel.typing():               # instant + continuous typing
                reply = await brain.ask_async_streaming(
                    text, history, on_progress, system=system, permissions=perms,
                    allowed_tools=allowed, model=model)
        finally:
            st["active"] = False
            ticker.cancel()
            done = _fmt_dur(time.monotonic() - t0)
            try:                                        # finalize: swap timer → "✻ Baked for …"; KEEP it
                if st["msg"] is not None:
                    if st["chips"]:
                        body = "\n".join(f"> {c}" for c in st["chips"]) + f"\n> ✻ Baked for {done}"
                    else:
                        body = f"✻ Baked for {done}"
                    await st["msg"].edit(content=body)
            except Exception:
                pass
        dur = int(time.monotonic() - t0)
        reply, _files = _extract_attachments(reply)
        reply = notify.prettify_tables(reply)        # md tables → aligned, fenced (Discord can't render md tables)
        _fresh = brain.pop_fresh_session_note(system)   # first message of a new day → say so, once
        if _fresh:
            reply = f"{_fresh}\n\n{reply}" if reply else _fresh
        cl = clients.get(name)                       # bot's live display name + avatar for the card header
        disp = cl.user.display_name if cl and cl.user else name.replace("scope-", "", 1)
        icon = cl.user.display_avatar.url if cl and cl.user else None
        stats = f"{(model.capitalize() if model else brain.model_label_for(text))} · {_fmt_dur(dur)}"  # end-bar run summary
        await _send_reply(channel, disp, reply, icon, stats=stats)
        for _fp in _files:                       # attach rendered tables/images/CSVs for big data
            try:
                await channel.send(file=discord.File(_fp))
            except Exception:
                pass
        history += [{"role": "Owner", "content": text}, {"role": "Assistant", "content": reply}]
        _save(name, history)
        mem.save_exchange(text, reply)
        # Background work runs on the cheaper model AND on a cadence (not every message) to
        # protect the Max budget — reflection used to be a 2nd full Opus call per message.
        n = _bump_counter(name)
        if config.reflect_every() and n % config.reflect_every() == 0:
            asyncio.create_task(_reflect(channel, text, reply))
        if config.compact_every() and n % config.compact_every() == 0 and (
                _memory_heavy() or not config.CORE_FILE().exists()):
            asyncio.create_task(_compact(channel, system))
        return reply

    async def _run_brain(channel, name, text, system, perms, allowed, model=None):
        """Serialize a bot's turns END-TO-END (work + reply post). Holds the lock across a loop so a
        mid-task correction can INTERRUPT + re-run with the addition merged, and queued follow-ups
        run as a continuation — before any unrelated queued message. Order stays: prior answer →
        '▶️ now on: …' → this answer."""
        lock = turn_locks.setdefault(name, asyncio.Lock())
        queued = lock.locked()                    # someone's turn is still posting → we're in line
        async with lock:
            if queued:
                snippet = " ".join((text or "").split())[:140]
                try:
                    await channel.send(f"_▶️ now on: {snippet}_")
                except Exception:
                    pass
            cur_text, reply = text, None
            while True:
                t0 = time.monotonic()
                dt = asyncio.create_task(_do_turn(channel, name, cur_text, system, perms, allowed, model))
                active[name] = {"task": dt, "text": cur_text, "t0": t0, "additions": [], "merge": None}
                try:
                    reply = await dt
                except asyncio.CancelledError:
                    reply = None                  # interrupted to fold something in → loop re-runs
                info = active.get(name) or {}
                if info.get("merge"):             # correction/early-addition → re-run merged
                    cur_text = f"{cur_text}\n\n[Owner added mid-task — incorporate this]: {info['merge']}"
                    continue
                if info.get("additions"):         # later follow-ups → run as a continuation
                    cur_text = "Follow-up to what you just did:\n" + "\n".join(info["additions"])
                    continue
                break
            active.pop(name, None)
            return reply

    async def _background(channel, name, text, system, model=None):
        """Run a task in PARALLEL (the owner asked to background it): forks the session so it's
        lock-free — it runs ALONGSIDE live chat. Tracked in the merged per-channel background PANEL
        (one live message listing all running tasks); on finish it drops off the panel and posts a
        ✅ completion line with its summary attached right below it. No queue."""
        cl = clients.get(name)
        disp = cl.user.display_name if cl and cl.user else name
        icon = cl.user.display_avatar.url if cl and cl.user else None
        label = " ".join((text or "").split())[:48]
        s = _bg_state(channel)
        _BG_SEQ[0] += 1
        tid = _BG_SEQ[0]
        s["tasks"][tid] = {"label": label, "t0": time.monotonic()}
        if not s["ticker"] or s["ticker"].done():
            s["ticker"] = asyncio.create_task(_bg_ticker(s))
        await _bg_paint(s)

        async def _run():
            t0 = s["tasks"][tid]["t0"]
            wrapped = ("You're running this as a BACKGROUND task, in PARALLEL with the live chat. Do it "
                       "end to end autonomously (don't ask questions), then reply with a SHORT summary "
                       "of what you did.\n\n" + text)
            try:
                sid = brain.current_session_id(system)
                if sid:
                    reply = await brain.ask_resumed(wrapped, sid, timeout=config.agent_job_timeout(),
                                                    model=model)
                else:
                    reply = await brain.ask_async(wrapped, [], system=system, model=model)
            except Exception as e:
                reply = f"(background task hit an error: {e})"
            done = _fmt_dur(time.monotonic() - t0)
            s["tasks"].pop(tid, None)                # off the running panel
            s["done"].append((label, done)); s["done"][:] = s["done"][-10:]
            await _bg_paint(s)
            # completion UNIT — tick + summary attached right here (not a floating card at the end)
            await channel.send(f"✅ **background done** · {label} · {done}")
            reply, files = _extract_attachments(reply)
            reply = notify.prettify_tables(reply)
            await _send_reply(channel, disp, reply, icon, stats=f"background · {done}")
            for fp in files:
                try:
                    await channel.send(file=discord.File(fp))
                except Exception:
                    pass
        asyncio.create_task(_run())

    async def _goal_bg(channel, name, task, system):
        """Ralph-wiggum GOAL LOOP, run in the background: iterate the task until the agent emits
        the completion promise (or max iterations). Posts each iteration milestone + a final card.
        Lock-free (its own forked turns), so live chat keeps working."""
        from ..core import goal
        cl = clients.get(name)
        disp = cl.user.display_name if cl and cl.user else name
        icon = cl.user.display_avatar.url if cl and cl.user else None
        mx = config.goal_max_iter()
        await channel.send(f"🎯 **goal loop** started (up to {mx} iterations) — I'll grind on this "
                           f"and report back:\n> {task[:240]}")

        async def _run():
            t0 = time.monotonic()

            async def _prog(line):
                if line.startswith("🔁"):           # post iteration milestones only (skip step noise)
                    try:
                        await channel.send(f"_{line}_")
                    except Exception:
                        pass
            try:
                res = await goal.run_goal(task, _prog, max_iter=mx, system=system)
            except Exception as e:
                await channel.send(f"(goal loop error: {e})")
                return
            dur = _fmt_dur(time.monotonic() - t0)
            mark = "✅" if res["done"] else "⚠️"
            verb = "done" if res["done"] else f"stopped at the {mx}-iteration cap"
            await channel.send(f"{mark} **goal {verb}** · {res['iterations']} iterations · {dur}")
            body, files = _extract_attachments(res.get("result") or "(no result)")
            body = notify.prettify_tables(body)
            await _send_reply(channel, disp, body, icon,
                              stats=f"goal · {res['iterations']} iter · {dur}")
            for fp in files:
                try:
                    await channel.send(file=discord.File(fp))
                except Exception:
                    pass
        asyncio.create_task(_run())

    async def _dispatch(channel, name, text, system, perms, allowed, model=None):
        """Smart steering for a message that lands while the bot is busy:
          • correction ('wait/no/instead') OR an addition while the task JUST started → interrupt,
            merge it in, re-run.
          • addition later in the task → fold in as a continuation after the current turn finishes.
          • new topic → queue normally (serialized behind the current turn)."""
        is_goal, goal_task = _wants_goal(text)
        if is_goal:                               # 'goal: …' / 'keep going until …' → ralph loop
            await _goal_bg(channel, name, goal_task, system)
            return None
        if _wants_background(text):               # explicit 'in parallel / in the background' → fork it
            await _background(channel, name, text, system, model)
            return None
        cur = active.get(name)
        if cur and not cur["task"].done():
            kind = _steer_kind(text)
            if kind in ("correction", "addition"):
                early = (time.monotonic() - cur.get("t0", 0)) < _STEER_EARLY_SECS
                if kind == "correction" or early:
                    cur["merge"] = text
                    cur["task"].cancel()
                    await channel.send("↩️ got it — folding that into what I'm on, re-running with it.")
                else:
                    cur.setdefault("additions", []).append(text)
                    await channel.send("📎 noted — I'll fold that in right after this step.")
                return None
        return await _run_brain(channel, name, text, system, perms, allowed, model)

    async def _orchestrate(channel, task, sc):
        """An orchestrator room: PLAN (split the task across the other rooms) → FAN OUT in parallel
        (capped, to spare the box) → MERGE the results into one answer. Each sub-task runs in its
        target room as that room's persona (own session/memory/fence)."""
        workers = {cid: s for cid, s in _SCOPES.items()
                   if not s.get("orchestrator") and cid != channel.id}
        if not workers:
            await channel.send("no worker rooms yet — `!activate #room <intent>` a few first, then "
                               "give me a goal and I'll split it across them.")
            return
        name_to_cid = {s["name"]: cid for cid, s in workers.items()}
        roster = "\n".join(
            f"- {s['name']}: {((s.get('system') or '').strip().splitlines() or [''])[0][:120]}"
            for s in workers.values())
        await channel.send("🧭 planning the fan-out…")
        plan_prompt = (
            "You are an orchestrator. Split the owner's goal into independent sub-tasks and assign each "
            "to the ONE best-suited room from this roster:\n" + roster +
            f"\n\nGoal: {task}\n\nReturn ONLY a JSON array (1–5 items), no prose:\n"
            '[{"room":"<exact room name>","task":"<what that room should do>"}]\n'
            "Use only the room names listed.")
        try:
            raw = await brain.ask_async(plan_prompt, [], system=sc.get("system"))
        except Exception as e:
            await channel.send(f"⚠️ planning failed: {e}"); return
        plan = _extract_plan(raw, set(name_to_cid))
        if not plan:
            await channel.send("couldn't form a plan from the available rooms. My raw take:\n> "
                               + " ".join((raw or "").split())[:400]); return
        await channel.send("🧭 **plan**\n" + "\n".join(
            f"{i+1}. <#{name_to_cid[p['room']]}> (**{p['room']}**) → {p['task'][:140]}"
            for i, p in enumerate(plan)))

        sem = asyncio.Semaphore(3)                 # cap parallel heavy turns — the box is small
        async def _one(p):
            cid = name_to_cid[p["room"]]; w = workers[cid]
            ch = client.get_channel(cid)
            if ch is None:
                return {**p, "result": "(room channel not reachable)"}
            async with sem:
                try:
                    r = await _run_brain(ch, "scope-" + w["name"], p["task"], w.get("system"),
                                         w.get("permissions", "readonly"), w.get("allowed_tools"),
                                         w.get("model") or config.background_model())  # cheap fan-out
                except Exception as e:
                    r = f"(error: {e})"
            return {**p, "result": r or "(no reply)"}
        results = await asyncio.gather(*[_one(p) for p in plan])

        await channel.send("🪢 merging the results…")
        merge_prompt = (
            "You fanned this goal out to several rooms. Synthesize their results into ONE clear, "
            "complete answer for the owner — resolve overlaps, flag conflicts, keep it tight.\n\n"
            f"Goal: {task}\n\n" + "\n\n".join(
                f"### {r['room']} — did: {r['task'][:80]}\n{(r['result'] or '')[:2000]}" for r in results))
        try:
            final = await brain.ask_async(merge_prompt, [], system=sc.get("system"))
        except Exception as e:
            final = f"(merge failed: {e}) — but each room posted its own result above."
        await _send_reply(channel, sc["name"], final or "(merge produced nothing)",
                          None, stats=f"orchestrated · {len(results)} room(s)")

    async def _architect(channel, goal):
        """Team-on-demand, ANY channel, ZERO setup. PLAN the goal into role-tagged sub-tasks →
        run them in PARALLEL (route to a real room if one fits, else spawn an EPHEMERAL agent — a
        forked brain wearing that role) → MERGE. A simple goal returns one item = solo answer."""
        if not goal:
            await channel.send("usage: `!architect <goal>` — I split it into parallel agents, run "
                               "them, and merge. Works anywhere, no setup needed."); return
        workers = {cid: s for cid, s in _SCOPES.items() if not s.get("orchestrator")}
        roster = "\n".join(
            f"- {s['name']}: {((s.get('system') or '').strip().splitlines() or [''])[0][:100]}"
            for s in workers.values()) or "(none)"
        await channel.send("🧭 planning…")
        plan_prompt = (
            "Break the owner's goal into 1–5 INDEPENDENT sub-tasks that can run in parallel; give each "
            "a short role label. If a sub-task fits one of these existing rooms, put its exact name in "
            f'"room" (else null):\n{roster}\n\nGoal: {goal}\n\n'
            'Return ONLY JSON: [{"role":"<role>","task":"<sub-task>","room":<"name" or null>}]. '
            "If the goal is simple, return a single item.")
        try:
            raw = await brain.ask_async(plan_prompt, [], system=None)
        except Exception as e:
            await channel.send(f"⚠️ planning failed: {e}"); return
        plan = _extract_arch_plan(raw)
        if not plan:
            await channel.send("couldn't plan that — my take:\n> "
                               + " ".join((raw or "").split())[:600]); return
        n2c = {s["name"]: cid for cid, s in workers.items()}
        head = "solo" if len(plan) == 1 else f"{len(plan)} agents in parallel"
        await channel.send(f"🧭 **plan** ({head})\n" + "\n".join(
            f"{i+1}. **{p['role']}**" + (f" → <#{n2c[p['room']]}>" if p.get("room") in n2c else " · agent")
            + f" — {p['task'][:120]}" for i, p in enumerate(plan)))

        sem = asyncio.Semaphore(3)                  # cap parallel heavy turns — the box is small
        async def _one(p):
            async with sem:
                try:
                    if p.get("room") in n2c:        # a real room fits → use its persona + fence
                        cid = n2c[p["room"]]; w = workers[cid]
                        ch = client.get_channel(cid) or channel
                        r = await _run_brain(ch, "scope-" + w["name"], p["task"], w.get("system"),
                                             w.get("permissions", "readonly"), w.get("allowed_tools"),
                                             w.get("model") or config.background_model())  # cheap fan-out
                    else:                           # ephemeral agent — role hat, full brain, cheap model
                        r = await brain.ask_async(
                            f"You are acting as: {p['role']}. Do this sub-task autonomously, then "
                            f"report a concise result.\n\nSub-task: {p['task']}", [],
                            model=config.background_model())
                except Exception as e:
                    r = f"(error: {e})"
            return {**p, "result": r or "(no reply)"}
        results = await asyncio.gather(*[_one(p) for p in plan])

        for r in results:                           # show each agent's result
            await _send_reply(channel, r["role"], r["result"], None, stats="agent")
        if len(results) == 1:
            return                                  # solo — that single result IS the answer
        await channel.send("🪢 merging…")
        merge_prompt = ("Synthesize these parallel agent results into ONE clear, complete answer for "
                        f"the owner — resolve overlaps, flag conflicts, keep it tight.\n\nGoal: {goal}\n\n"
                        + "\n\n".join(f"### {r['role']}\n{(r['result'] or '')[:2000]}" for r in results))
        try:
            final = await brain.ask_async(merge_prompt, [], system=None)
        except Exception as e:
            final = f"(merge failed: {e}) — see the agent results above."
        await _send_reply(channel, "architect", final or "(nothing)", None,
                          stats=f"merged · {len(results)} agents")

    def make_client(name: str, spec: dict):
        is_main = spec.get("trigger", "mention") == "home"
        system = None if is_main else bots.load_system(name)
        perms = spec.get("permissions", "full")
        allowed = spec.get("allowed_tools")

        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        clients[name] = client

        @client.event
        async def on_ready():
            print(f"[{name}] connected as {client.user}")
            if not is_main:
                scoped_ids.add(client.user.id)
            elif home_channel:
                ch = client.get_channel(home_channel)
                if ch:
                    await ch.send(f"🟢 mindpalace online — main bot @ home channel "
                                  f"({len(registry)} bot(s)).")

        @client.event
        async def on_message(msg):
            if msg.author.bot:
                return
            in_home = msg.channel.id == home_channel
            # bootstrap: first human to talk in the home channel becomes the first admin
            if is_main and in_home and not config.admins():
                config.add_admin(msg.author.id)
                await msg.channel.send(f"👑 registered <@{msg.author.id}> as the first admin.")
            if not config.is_admin(msg.author.id):   # admins only
                return

            # admin commands (home channel) — handled here, not sent to the brain
            raw = (msg.content or "").strip()
            if is_main and raw[:10].lower() == "!architect":   # team-on-demand, works in ANY channel
                await _architect(msg.channel, raw[10:].strip())
                return
            if is_main and in_home and raw.startswith("!"):
                await _handle_command(msg, raw)
                return

            mentioned = client.user in msg.mentions
            scoped_mention = any(m.id in scoped_ids for m in msg.mentions)
            # effective identity for this turn — overridden below in an activated (scoped) channel
            eff_name, eff_system, eff_perms, eff_allowed, eff_model = name, system, perms, allowed, None

            if is_main:
                # home: handle everything EXCEPT messages aimed at a scoped bot (supervise instead)
                if in_home:
                    if scoped_mention:
                        return  # the scoped bot handles it; we report after (see scoped branch)
                    # cross-room dispatch: "#room <task>" in home → run it IN that activated room
                    # AS its persona (own session/memory/fence), then a one-line report back here.
                    routed = next((c for c in msg.channel_mentions if c.id in _SCOPES), None)
                    if routed:
                        sc = _SCOPES[routed.id]
                        task = (msg.content or "").replace(f"<#{routed.id}>", "").strip()
                        # carry any attached images/files too (saved locally → the room can Read them)
                        atts = await _save_attachments(msg)
                        task = _augment_with_attachments(task, atts)
                        if task:
                            target = client.get_channel(routed.id) or routed
                            note = " (with attachment)" if atts else ""
                            await msg.channel.send(f"📨 routing to <#{routed.id}> (**{sc['name']}**){note}…")
                            r = await _dispatch(target, "scope-" + sc["name"], task,
                                                sc.get("system"), sc.get("permissions", "readonly"),
                                                sc.get("allowed_tools"), sc.get("model"))
                            if r:
                                await msg.channel.send(
                                    f"📋 <#{routed.id}> done: {' '.join(r.split())[:280]}")
                            return
                    text = (msg.content or "").strip()
                elif msg.channel.id in _SCOPES:
                    # an ACTIVATED channel → answer here AS that persona, no @mention needed.
                    # Distinct name → own history file + own brain session + own turn-lock; the
                    # persona is its system prompt; the tier is its tool fence. Different everything.
                    sc = _SCOPES[msg.channel.id]
                    text = msg.content.replace(f"<@{client.user.id}>", "").replace(
                        f"<@!{client.user.id}>", "").strip()
                    if sc.get("orchestrator"):       # this room plans → fans out to others → merges
                        if text:
                            await _orchestrate(msg.channel, text, sc)
                        return
                    eff_name = "scope-" + sc["name"]
                    eff_system = sc.get("system")
                    eff_perms = sc.get("permissions", "readonly")
                    eff_allowed = sc.get("allowed_tools")
                    eff_model = sc.get("model")      # per-room model (None → brain auto-picks)
                elif mentioned:
                    text = msg.content.replace(f"<@{client.user.id}>", "").replace(
                        f"<@!{client.user.id}>", "").strip()
                else:
                    return
            else:
                if not mentioned:
                    return
                text = msg.content.replace(f"<@{client.user.id}>", "").replace(
                    f"<@!{client.user.id}>", "").strip()

            # pull in ALL attachments (images + any file) so the brain can actually handle them
            atts = await _save_attachments(msg)
            if not text and not atts:
                return
            text = _augment_with_attachments(text, atts)

            # pending git update + owner says "yes" → pull + self-restart (deterministic,
            # never goes to the brain). Only in the home channel's main bot.
            if is_main and in_home and updater.read_pending() and updater.is_affirmative(text):
                async with msg.channel.typing():
                    result = await asyncio.to_thread(updater.accept)
                await msg.channel.send(result)
                return

            reply = await _dispatch(msg.channel, eff_name, text, eff_system, eff_perms, eff_allowed, eff_model)

            # supervision: a scoped bot finished a task in the HOME channel → main reports back
            if reply and (not is_main) and in_home and "main" in clients:
                main = clients["main"]
                ch = main.get_channel(home_channel)
                if ch:
                    summary = reply[:280].replace("\n", " ")
                    await ch.send(f"📋 monitored **{name}** — task complete. {summary}")

        return client

    async def report(message: str):
        """Post a background-job result to the home channel (main client, webhook fallback)."""
        main = clients.get("main")
        if main and main.is_ready() and home_channel:
            ch = main.get_channel(home_channel)
            if ch:
                await ch.send(message); return
        from ..core import notify
        notify.notify(message, "home")

    async def _health_card_home(title, body, accent):
        """Card → the HOME channel (main chat). Falls back to the box+webhook if home isn't ready."""
        main = clients.get("main")
        ch = main.get_channel(home_channel) if (main and main.is_ready() and home_channel) else None
        if ch:
            await _post_health_card(ch, title, body, accent)
        else:
            from ..core import notify as _n
            await asyncio.to_thread(_n.notify, _n.box(title, body, accent), config.heartbeat_webhook())

    async def _main():
        tasks = []
        for name, spec in registry.items():
            tok = bots.token(name)
            if not tok:
                print(f"[{name}] no token (secrets/bot_{name}.token) — skipping")
                continue
            tasks.append(make_client(name, spec).start(tok))
        if not tasks:
            raise SystemExit("No bot tokens — run `mindpalace setup` / `mindpalace add-bot`.")
        tasks.append(jobs.watch_loop(report))   # async dispatch: run queued bash jobs, report back
        tasks.append(jobs.agent_watch_loop(report))  # run handed-off long AGENT tasks, report back
        tasks.append(heartbeat.loop(report, config.heartbeat_minutes(), card=_health_card_home))  # → home card
        tasks.append(updater.loop(report, updater.interval_minutes()))     # git update watcher
        await asyncio.gather(*tasks)

    asyncio.run(_main())
