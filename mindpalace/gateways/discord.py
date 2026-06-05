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

from ..core import brain, jobs, heartbeat
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


_REFLECT_KEYWORDS = ("ssh", "login", "log in", "password", "passwd", "cred", "secret", "token",
                     "api key", "apikey", "deploy", "server", "vps", "host", "port", "database",
                     " db ", "project", "webhook", "domain", "dns", "access", "setup", "set up",
                     "install", "configure", "connect", "backup", "restart", "migrate", "scrape",
                     "create", "build", "fix", "cron", "schedule")


def _worth_reflecting(text, reply):
    # substantial work, or anything that smells like a procedure/resource worth capturing
    blob = (text + " " + reply).lower()
    return len(reply) > 300 or any(k in blob for k in _REFLECT_KEYWORDS)


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
            "**commands** (admins): `!admins`, `!add-admin @user`, `!remove-admin @user`, "
            "`!bots`, `!add-webhook <name> <url>`")
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

        async def on_progress(line):
            try:
                await channel.send(f"_{line}_")        # live step, e.g. 🔧 Bash: ssh …
            except Exception:
                pass

        async with channel.typing():                   # instant + continuous typing
            reply = await brain.ask_async_streaming(
                text, history, on_progress, system=system, permissions=perms, allowed_tools=allowed)
        for c in _chunks(reply):
            await channel.send(c)
        history += [{"role": "Owner", "content": text}, {"role": "Assistant", "content": reply}]
        _save(name, history)
        mem.save_exchange(text, reply)
        # background analyst: reason → file facts + skillify reusable procedures (runs in parallel)
        if _worth_reflecting(text, reply):
            asyncio.create_task(_reflect(channel, text, reply))
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

            if not text:
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
        await asyncio.gather(*tasks)

    asyncio.run(_main())
