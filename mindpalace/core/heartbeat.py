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


async def run_curation(report, force: bool = False) -> str:
    """Skill curation on its OWN cadence, independent of whether the health heartbeat is enabled.
    Skips unless: not paused, idle ≥ curator_idle_minutes (never rewrite skills mid-chat), and
    ≥7 days since the last run — unless force=True (manual `!curate now`). Claims the window BEFORE
    running so a crash can't re-fire it every cycle. Bumps run_count + last_summary. Returns the
    curator's note ('' when it skipped or had nothing to do)."""
    import time
    st = config.curator_state()
    if not force:
        if st["paused"]:
            return ""
        if config.idle_seconds() < config.curator_idle_minutes() * 60:
            return ""
        if time.time() - st["last_run"] < 7 * 86400:
            return ""
    st["last_run"] = time.time()                  # claim the window now → no re-fire on crash
    config.save_curator_state(st)
    from ..agents import analyst
    c = await analyst.curate()
    st = config.curator_state()                   # reload so a concurrent pause isn't clobbered
    st["run_count"] += 1
    spoke = bool(c and c.strip().upper() not in ("NOTHING", ""))
    if spoke:
        st["last_summary"] = c.strip()[:300]
    config.save_curator_state(st)
    if spoke:
        await _deliver(report, "🧹", "Skill upkeep", c, "green")
    return c or ""


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


async def run_once(report) -> str:
    """Run ONE health-check pass now (the Analyst's review) and deliver it (full → updates
    webhook, short tally → home). Shared by the scheduled tick and the manual `!heartbeat scan-now`.
    Returns the report text, or "" if all quiet."""
    from ..agents import analyst
    reply = await analyst.review()
    if reply and reply.strip().upper() not in ("NOTHING", ""):
        await _deliver(report, "💓", "Heartbeat", reply, "cyan")
        return reply
    return ""


async def loop(report, interval_min: int):
    # interval is read LIVE from config each cycle, so `!heartbeat <n>` applies without a restart.
    print("heartbeat: dynamic (reads heartbeat_minutes each cycle); curation on its own gate")
    while True:
        interval = config.heartbeat_minutes()
        if interval <= 0:
            await asyncio.sleep(60)               # health pass off — but still poll for curation
        else:
            await asyncio.sleep(interval * 60)
            if config.heartbeat_minutes() > 0:    # still on after the sleep → health pass
                try:
                    await run_once(report)        # the Analyst's autonomous health-check pass
                except Exception as e:
                    print(f"heartbeat error: {e}")
        # Skill curation runs on its OWN gate (idle + 7-day + not paused), INDEPENDENT of the
        # health heartbeat — so the library still gets tidied even when heartbeat is off.
        try:
            await run_curation(report)
        except Exception as e:
            print(f"curate error: {e}")
