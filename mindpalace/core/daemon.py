"""
The background daemon — always-on, like a systemd service.

It runs:
  • the job watcher (executes queued background jobs, reports results), and
  • the Discord bot(s), IF Discord is configured.

The terminal chat is always available separately (`mindpalace`) and auto-starts this
daemon in the background when Discord is configured — so you're reachable from BOTH the
terminal and Discord at once, and long jobs run in the background either way.

Run directly (foreground, for systemd/launchd):  mindpalace daemon
"""
from __future__ import annotations

import asyncio
import atexit
import os

from .. import config
from . import jobs


def discord_configured() -> bool:
    cfg = config.load_config()
    return bool(config.read_secret("bot_main.token") and cfg.get("discord", {}).get("home_channel"))


def _write_pid():
    """Record our PID so `status`/`stop` work however we were started (systemd, spawn, foreground)."""
    config.ensure_dirs()
    pf = config.state_dir() / "daemon.pid"
    pf.write_text(str(os.getpid()))
    atexit.register(lambda: pf.unlink(missing_ok=True))


def run():
    _write_pid()
    if discord_configured():
        from ..gateways import discord       # bot + job watcher run together
        discord.run()
    else:
        from . import heartbeat

        async def report(msg):
            from . import notify
            notify.notify(msg, "home")        # no-op if no webhook

        async def _go():
            await asyncio.gather(
                jobs.watch_loop(report),
                heartbeat.loop(report, config.heartbeat_minutes()))
        print("daemon: job watcher + heartbeat (Discord not configured)")
        asyncio.run(_go())
