"""
Autonomous heartbeat — the agent wakes itself on a timer (no human asking), reviews its
vault + the health of services it knows about, files anything new, and posts a short report
to the home channel if something's worth saying. This is what makes it proactive, not just
reactive.

Interval = config "heartbeat_minutes" (0 disables). Safe by default: it FILES + PROPOSES,
and does not take destructive/irreversible actions unprompted.
"""
from __future__ import annotations

import asyncio

from .. import config

PROMPT = (
    "[AUTONOMOUS HEARTBEAT — no human is asking; you woke yourself on a timer.]\n"
    "Do a quick proactive pass:\n"
    "1. Skim your vault (infra/, projects/, recent LOG.md) and check the health of services "
    "you have notes on (only cheap, safe checks).\n"
    "2. File any new facts into the right vault files + append a line to LOG.md (per your doctrine).\n"
    "3. If something needs attention or you did something, write a SHORT report: what you "
    "found/did + any proposed next action. Do NOT take destructive or irreversible actions "
    "unprompted — propose them instead.\n"
    "If everything is quiet and nothing is worth reporting, reply with EXACTLY: NOTHING"
)


def _due_for_curate(days: int = 7) -> bool:
    """True at most once per `days` — gates the slow skill-curation pass on idle ticks."""
    import time
    from .. import config
    p = config.state_dir() / "curator_last.txt"
    try:
        last = float(p.read_text().strip())
    except (FileNotFoundError, ValueError):
        last = 0.0
    if time.time() - last < days * 86400:
        return False
    try:
        config.state_dir().mkdir(parents=True, exist_ok=True)
        p.write_text(str(time.time()))
    except OSError:
        pass
    return True


import re as _re


async def _deliver(report, emoji, title, body, accent):
    """Full (boxed) report → the logs/updates webhook channel. To home: only a SHORT one-line note
    — for a health check, the at-a-glance tally (N ✓ · N ⚠ · N ✗) so the owner can spot a problem
    and go look. Keeps long reports out of the main channel."""
    from . import notify
    hook = config.heartbeat_webhook()
    where = config.heartbeat_channel_label()       # friendly channel name for the note
    full = notify.box(f"{emoji} {title}", body, accent)
    sent = await asyncio.to_thread(notify.notify, full, hook)
    if not sent:                                   # no such webhook → don't lose it, post here
        await report(full)
        return
    m = _re.search(r"✓\s*(\d+)\s*⚠\s*(\d+)\s*✗\s*(\d+)", body)
    if m:
        ok, warn, fail = (int(x) for x in m.groups())
        tally = f"{ok} ✓ · {warn} ⚠️ · {fail} ✗"
        if warn or fail:
            note = f"💓 health check: **{tally}** — 👀 something to look at, full report in **{where}**."
        else:
            note = f"💓 health check: **{tally}** — all clear ✅ (log in **{where}**)."
    else:
        note = f"{emoji} {title.lower()} ran — full rundown in **{where}**, keeping it tidy here."
    await report(note)


async def loop(report, interval_min: int):
    # interval is read LIVE from config each cycle, so `!heartbeat <n>` applies without a restart.
    print("heartbeat: dynamic (reads heartbeat_minutes each cycle)")
    while True:
        interval = config.heartbeat_minutes()
        if interval <= 0:
            await asyncio.sleep(60)               # off — re-check every minute (re-enable live)
            continue
        await asyncio.sleep(interval * 60)
        if config.heartbeat_minutes() <= 0:       # turned off during the sleep
            continue
        try:
            from ..agents import analyst
            reply = await analyst.review()        # the Analyst agent's autonomous pass
            if reply and reply.strip().upper() not in ("NOTHING", ""):
                await _deliver(report, "💓", "Heartbeat", reply, "cyan")
            if _due_for_curate():                 # slow cadence: consolidate/archive skills
                c = await analyst.curate()
                if c and c.strip().upper() not in ("NOTHING", ""):
                    await _deliver(report, "🧹", "Skill upkeep", c, "green")
        except Exception as e:
            print(f"heartbeat error: {e}")
