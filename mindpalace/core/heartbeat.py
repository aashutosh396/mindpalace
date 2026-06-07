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


async def loop(report, interval_min: int):
    if interval_min <= 0:
        return
    print(f"heartbeat: every {interval_min}m")
    while True:
        await asyncio.sleep(interval_min * 60)
        try:
            from ..agents import analyst
            reply = await analyst.review()        # the Analyst agent's autonomous pass
            if reply and reply.strip().upper() not in ("NOTHING", ""):
                await report("💓 " + reply)
            if _due_for_curate():                 # slow cadence: consolidate/archive skills
                c = await analyst.curate()
                if c and c.strip().upper() not in ("NOTHING", ""):
                    await report("🧹 " + c)
        except Exception as e:
            print(f"heartbeat error: {e}")
