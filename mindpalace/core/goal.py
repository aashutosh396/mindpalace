"""
Ralph-Wiggum goal loop — iterate a task until it's DONE, not just one shot.

Named after Geoffrey Huntley's "Ralph" (a bash `while` loop feeding the same prompt to Claude
until a completion signal appears). Here it's an in-process loop: each iteration is a full
autonomous brain turn. Progress lives in the ARTIFACTS (files, tests, repo state), not in chat —
so every iteration re-assesses the real state, does the next concrete steps, and verifies. The
loop stops when the agent emits the completion promise, or after `max_iter` (safety).

Use for well-defined goals with checkable success (tests pass, file exists, build clean) — the
kind of thing worth grinding on unattended. Not for subjective/judgment tasks.
"""
from __future__ import annotations

from .. import config

DEFAULT_PROMISE = "GOAL_COMPLETE"


def _wrap(task: str, promise: str, i: int, n: int) -> str:
    return (
        f"You are in an autonomous GOAL LOOP — iteration {i} of at most {n}. Progress persists in "
        "the FILES / repo / system state, NOT in this chat, so FIRST inspect the current state to "
        "see what's already done, then do the next concrete step(s).\n\n"
        f"GOAL:\n{task}\n\n"
        "Each iteration: assess what remains → do the next steps → VERIFY them (run tests / checks / "
        "the actual command where possible). Be decisive; don't ask questions.\n"
        f"When — and ONLY when — the goal is FULLY met AND verified, end your reply with this exact "
        f"line on its own:\n<<{promise}>>\n"
        "If it is NOT fully done, briefly say what you did this iteration and what's left, and do "
        "NOT emit that line."
    )


def _done(reply: str, promise: str) -> bool:
    return f"<<{promise}>>" in (reply or "")


def _strip(reply: str, promise: str) -> str:
    return (reply or "").replace(f"<<{promise}>>", "").strip()


async def run_goal(task: str, on_progress, promise: str = DEFAULT_PROMISE,
                   max_iter: int | None = None, system: str | None = None) -> dict:
    """Loop a task to completion. on_progress(str) is called per iteration (and may relay each
    turn's own streamed steps). Returns {done, iterations, result}."""
    from . import brain
    n = max_iter or config.goal_max_iter()
    last = ""
    for i in range(1, n + 1):
        try:
            await on_progress(f"🔁 goal iteration {i}/{n}")
        except Exception:
            pass

        async def _relay(line):                      # surface this iteration's live steps too
            try:
                await on_progress(line)
            except Exception:
                pass

        last = await brain.ask_async_streaming(_wrap(task, promise, i, n), [], _relay, system=system)
        if _done(last, promise):
            return {"done": True, "iterations": i, "result": _strip(last, promise)}
        # not done yet → post a SHORT recap of this iteration so the owner can watch progress
        # and catch drift early (the loop is otherwise silent between iterations).
        recap = " ".join(_strip(last, promise).split())[:300]
        if recap:
            try:
                await on_progress(f"📝 iter {i}/{n}: {recap}")
            except Exception:
                pass
    return {"done": False, "iterations": n, "result": last}
