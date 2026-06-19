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

from ..core import brain, jobs, heartbeat, updater, notify
from .. import bots, config
from ..memory import store as mem

HEARTBEAT_AFTER = 60
KEEP = 24


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
            try:
                out = await heartbeat.run_once(_rep)      # full → updates webhook, tally → here
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
    elif cmd in ("curate", "curator"):
        sub = args[0].lower() if args else "status"
        if sub in ("now", "run", "force"):
            await msg.channel.send("🧹 running skill curation now — one sec…")
            async def _rep(m):
                await msg.channel.send(m)
            try:
                out = await heartbeat.run_curation(_rep, force=True)
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

    clients: dict[str, "discord.Client"] = {}   # name -> client
    scoped_ids: set[int] = set()                 # user-ids of non-main bots (for mention checks)

    async def _run_brain(channel, name, text, system, perms, allowed):
        """Drive one bot's brain; STREAM its steps live; reply; persist; file in background."""
        history = _load(name)

        # Chips (⚡ …) stack into ONE growing blockquote message — compact, Hermes-style.
        # A prose line breaks the block and posts on its own, then the next chips start fresh.
        st = {"chips": [], "msg": None}

        async def on_progress(line):
            try:
                if line.startswith("⚡"):
                    st["chips"].append(line)
                    body = "\n".join(f"> {c}" for c in st["chips"])
                    if st["msg"] is not None:
                        await st["msg"].edit(content=body)
                    else:
                        st["msg"] = await channel.send(body)
                else:                                   # prose → its own line; reset the chip block
                    st["chips"], st["msg"] = [], None
                    await channel.send(f"_{line}_")
            except Exception:
                pass

        async with channel.typing():                   # instant + continuous typing
            reply = await brain.ask_async_streaming(
                text, history, on_progress, system=system, permissions=perms, allowed_tools=allowed)
        reply, _files = _extract_attachments(reply)
        reply = notify.prettify_tables(reply)        # md tables → aligned, fenced (Discord can't render md tables)
        for c in _chunks(reply):
            await channel.send(c)
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
            if is_main and in_home and raw.startswith("!"):
                await _handle_command(msg, raw)
                return

            mentioned = client.user in msg.mentions
            scoped_mention = any(m.id in scoped_ids for m in msg.mentions)

            if is_main:
                # home: handle everything EXCEPT messages aimed at a scoped bot (supervise instead)
                if in_home:
                    if scoped_mention:
                        return  # the scoped bot handles it; we report after (see scoped branch)
                    text = (msg.content or "").strip()
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
            if atts:
                imgs = [a for a in atts if a["is_image"]]
                files = [a for a in atts if not a["is_image"]]
                notes = []
                if imgs:
                    notes.append("VIEW these image(s) with the Read tool: "
                                 + ", ".join(a["path"] for a in imgs))
                if files:
                    notes.append("READ/process these file(s) with the Read tool or bash "
                                 "(they are saved locally): "
                                 + ", ".join(f'{a["name"]} -> {a["path"]}' for a in files))
                text = (text or "(no caption)") + (
                    "\n\n[The owner attached files. " + " | ".join(notes)
                    + ". Open them before replying — don't say the attachment didn't load.]")

            # pending git update + owner says "yes" → pull + self-restart (deterministic,
            # never goes to the brain). Only in the home channel's main bot.
            if is_main and in_home and updater.read_pending() and updater.is_affirmative(text):
                async with msg.channel.typing():
                    result = await asyncio.to_thread(updater.accept)
                await msg.channel.send(result)
                return

            reply = await _run_brain(msg.channel, name, text, system, perms, allowed)

            # supervision: a scoped bot finished a task in the HOME channel → main reports back
            if (not is_main) and in_home and "main" in clients:
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
        tasks.append(jobs.watch_loop(report))   # async dispatch: run queued jobs, report back
        tasks.append(heartbeat.loop(report, config.heartbeat_minutes()))   # autonomous self-tick
        tasks.append(updater.loop(report, updater.interval_minutes()))     # git update watcher
        await asyncio.gather(*tasks)

    asyncio.run(_main())
