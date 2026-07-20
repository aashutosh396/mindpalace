"""Ticket worker — what makes the board ALIVE.

Watches for 'todo' cards, claims the oldest, runs it through the configured
provider (Claude Max in v3.0) with the project's repos + assets as its world,
then parks the card in 'review' with the result and posts the reply into the
room's chat. Progress streams out over the WS bus so the card visibly works.

Crash recovery (the v2 lesson): a daemon restart orphans 'in_progress' cards —
they'd sit there working forever. Requeue them to 'todo' at watcher start.
"""
from __future__ import annotations

import asyncio
import re

from .. import config
from . import store
from ..providers import get_provider
from ..providers.base import TaskContext

_SYSTEM = (
    "You are the resident agent of the room '{name}'.\n"
    "{context}"
    "Projects connected to this room — do your work INSIDE their folders:\n{repos}\n"
    "Room assets folder (briefs, designs, uploads the owner gave you): {assets}\n"
    "You have full machine access; stay within this room's world unless the "
    "ticket explicitly points elsewhere."
)

_WRAP = (
    "You are working ticket #{tid} from the project board — the owner is NOT "
    "waiting live, so work autonomously and DON'T ask questions; make sensible "
    "decisions and proceed. Do this end to end:\n\n{task}\n\n"
    "When finished, reply in 3-4 short lines MAX: 'Done:' + one ✓ line per thing "
    "done (a few words each), then ONE next-step proposal if there is an obvious "
    "one. Simple everyday English. No essays, no file attachments.\n"
    "END your reply with exactly one verdict line:\n"
    "  VERDICT: done    — you verified the work yourself and nothing needs the "
    "owner's eyes (chores, small fixes you tested, lookups)\n"
    "  VERDICT: review  — the owner should look (visual changes, risky edits, "
    "decisions you made, anything you could not verify)"
)


_KEEPER = (
    "You are the PALACE-KEEPER — you work general cards about the palace itself.\n"
    "The palace has TWO layers: PROJECTS are inventory (a name + folders/repos on "
    "disk — you manage these); ROOMS are the owner's channels (the owner creates "
    "those — NEVER create or delete rooms).\n"
    "Manage the inventory through the local API at http://127.0.0.1:{port}:\n"
    "  GET  /api/projects                       — list projects (with folders + rooms using them)\n"
    "  POST /api/projects {{\"name\": ...}}        — create a project (inventory entry)\n"
    "  POST /api/projects/<id>/repos {{\"path\": \"/abs/folder\"}}\n"
    "      — attach a project's MAIN FOLDER (nested git repos auto-discovered)\n"
    "  GET  /api/rooms                          — list the owner's rooms (read-only for you)\n"
    "Typical chores: scan the owner's machine or vault for projects, create project "
    "entries, attach their folders, deduplicate the inventory.\n"
    "IRON RULE: a project without its folder is useless — when you create one, "
    "attach its folder in the same run and verify with GET before reporting done."
)


def _ctx_for(task: dict) -> TaskContext | None:
    from .. import config
    r = store.get_room(task["room_id"])
    if not r:
        return None
    paths = store.room_paths(task["room_id"])
    assets = str(store.room_dir(r["slug"]) / "assets")
    projects = store.projects_for_room(task["room_id"])
    repos_block = "\n".join(
        f"  - {p['name']}: " + (", ".join(x["path"] for x in p["repos"]) or "(no folders)")
        for p in projects) or "  (no projects connected yet)"
    ctx_line = f"What this room is for: {r['context']}\n" if r.get("context") else ""
    system = _SYSTEM.format(name=r["name"], context=ctx_line, repos=repos_block, assets=assets)
    if r["slug"] == store.HOME_SLUG:
        port = int(config.load_config().get("web", {}).get("port", 7777))
        system = _KEEPER.format(port=port)
    return TaskContext(project_slug=r["slug"], repo_paths=paths, asset_dir=assets, system=system)


_GOAL_WRAP = (
    "You are grinding GOAL card #{tid} — iteration {n} of at most {cap}. The goal:\n\n"
    "{task}\n\n"
    "{prev}"
    "Work autonomously on the next concrete chunk of progress. When — and ONLY "
    "when — the goal is TRULY, verifiably complete, include the exact phrase "
    "{promise} in your reply. Otherwise end with 2-3 short lines: what you did "
    "this iteration and what's next. Never claim completion early."
)

_FOLLOWUP_WRAP = (
    "You are CONTINUING work on card #{tid} after the owner replied on it.\n\n"
    "The card: {task}\n\nYour previous report:\n{result}\n\n{thread}"
    "The owner now says:\n{reply}\n\n"
    "Do what they ask, end to end, then reply in 3-4 short lines MAX "
    "('Done:' + ✓ lines, simple English)."
)

GOAL_CAP = 8
DEFAULT_PROMISE = "GOAL COMPLETE"


def _on_event_for(task: dict, broadcast):
    async def on_event(ev):
        store.add_task_log(task["id"], ev.text)     # durable trail for the card modal
        await broadcast("task.progress", {"task_id": task["id"], "text": ev.text})
    return on_event


_PROPOSE = (
    "You are the owner's agent in the room \"{room}\". A card just finished:\n"
    "  Card #{tid}: {title}\n  Result (tail): {result}\n\n"
    "THE BOARD RIGHT NOW:\n{board}\n\n"
    "RECENT ROOM CHAT:\n{chat}\n\n"
    "Propose the ONE best next move for the owner — something concrete that keeps "
    "the work flowing (a follow-up, the thing this unblocks, a merge/deploy/check). "
    "Simple everyday English, a few words each. If nothing is genuinely worth "
    "proposing, say so.\n"
    "Answer STRICT JSON only: {{\"proposal\": \"<the move>\", \"reason\": \"<few words>\"}} "
    "or {{\"proposal\": null}}"
)


async def _propose_next(task: dict, room: dict, broadcast) -> None:
    """The Discord habit, kept: after work lands, offer the one best next move
    ('Next I propose X. reason: … Start?'). A 'start' reply in the room files it."""
    from ..core import brain
    try:
        board = "\n".join(
            f"- #{t['id']} [{t['status']}] {t['title']}"
            for t in store.list_tasks(task["room_id"]) if t["status"] != "done") or "(board is clear)"
        chat = "\n".join(
            f"{m['role']}: {m['text'][:120]}" for m in store.list_chat(task["room_id"], 6))
        prompt = _PROPOSE.format(
            room=room["name"], tid=task["id"], title=task["title"],
            result=(task.get("result") or "")[-400:], board=board, chat=chat)
        proc = await asyncio.create_subprocess_exec(
            brain.claude_bin(), "-p", prompt, "--model", "sonnet",
            env=brain._env(),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=90)
        import json as _json
        raw = out.decode(errors="replace").strip()
        d = _json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
        if not d.get("proposal"):
            return
        reason = (d.get("reason") or "").strip()
        line = f"Next I propose {d['proposal'].strip()}"
        if reason:
            line += f". reason: {reason}"
        line += ". Start?"
        store.set_proposal(room["id"], f"{d['proposal'].strip()}" + (f" — {reason}" if reason else ""))
        msg = store.add_chat(task["room_id"], "agent", line)
        await broadcast("chat.message", msg)
    except Exception:
        pass                                          # proposals are a bonus, never a failure


async def _finish(task: dict, reply: str, broadcast) -> None:
    # Review = the "needs your eyes" queue ONLY. The agent ends each run with a
    # verdict: self-verified work closes straight to done; anything visual,
    # risky, or unverified stops in Review. Failures always stop in Review.
    failed = reply.startswith("(")
    verdict = None
    m = re.search(r"\n?\s*VERDICT:\s*(done|review)\W*$", reply.strip(), re.IGNORECASE)
    if m:
        verdict = m.group(1).lower()
        reply = reply.strip()[:m.start()].rstrip()
    if failed:
        status = "review"
    elif task.get("created_by") == "routine":
        status = "done"
    elif verdict == "done":
        status = "done"
    else:
        status = "review"
    t = store.set_task_status(task["id"], status, result=reply)
    room = store.get_room(task["room_id"])
    if room and room["slug"] == store.HOME_SLUG:
        # keeper cards: the hall IS their room — deliver the result there
        hmsg = store.add_home_chat("agent", reply, ref_room_id=room["id"], task_id=task["id"])
        await broadcast("home.message", hmsg)
    else:
        msg = store.add_chat(task["room_id"], "agent", reply, task_id=task["id"])
        await broadcast("chat.message", msg)
        if room:                                     # and announce delivery in the hall
            if status != "done":
                where = "waiting in Review"
            elif task.get("created_by") == "routine":
                where = "closed (routine)"
            else:
                where = "closed — self-verified"
            note = store.add_home_chat(
                "agent", f"✅ Card #{task['id']} done in {room['name']} — {where}",
                ref_room_id=room["id"], task_id=task["id"])
            await broadcast("home.message", note)
        if room and not failed and task.get("created_by") != "routine":
            asyncio.create_task(_propose_next({**task, "result": reply}, room, broadcast))
    if t:
        await broadcast("task.updated", t)


async def run_one(task: dict, broadcast) -> None:
    ctx = _ctx_for(task)
    if ctx is None:                                   # room vanished under the card
        store.set_task_status(task["id"], "done", result="(room was deleted)")
        return
    on_event = _on_event_for(task, broadcast)

    if (task.get("kind") or "task") == "goal":
        promise = task.get("promise") or DEFAULT_PROMISE
        reply, prev = "", ""
        for n in range(1, GOAL_CAP + 1):
            t = store.set_task_iterations(task["id"], n)
            if t:
                await broadcast("task.updated", t)
            store.add_task_log(task["id"], f"— iteration {n} —")
            instruction = _GOAL_WRAP.format(
                tid=task["id"], n=n, cap=GOAL_CAP,
                task=task["body"] or task["title"], promise=promise,
                prev=f"Your last iteration reported:\n{prev}\n\n" if prev else "")
            reply = await get_provider().run_task(instruction, ctx, on_event)
            store.set_task_result(task["id"], reply)
            if promise in reply:
                break
            prev = reply
        await _finish(task, reply, broadcast)
        return

    instruction = _WRAP.format(tid=task["id"], task=task["body"] or task["title"])
    reply = await get_provider().run_task(instruction, ctx, on_event)
    await _finish(task, reply, broadcast)


async def run_followup(task: dict, reply_text: str, broadcast) -> None:
    """The owner replied on a card — continue that work with its context."""
    ctx = _ctx_for(task)
    if ctx is None:
        return
    marker = f"— follow-up: {reply_text.strip()[:70]} —"
    store.add_task_log(task["id"], marker)           # divides runs inside the trail
    await broadcast("task.progress", {"task_id": task["id"], "text": marker})
    thread = store.list_thread(task["id"])[:-1]      # everything before this reply
    thread_txt = ("Earlier follow-ups:\n" +
                  "\n".join(f"{m['role']}: {m['text'][:300]}" for m in thread) + "\n\n"
                  ) if thread else ""
    instruction = _FOLLOWUP_WRAP.format(
        tid=task["id"], task=task["body"] or task["title"],
        result=(task.get("result") or "(none)")[:1500],
        thread=thread_txt, reply=reply_text)
    reply = await get_provider().run_task(instruction, ctx, _on_event_for(task, broadcast))
    tmsg = store.add_thread(task["id"], "agent", reply)
    await broadcast("task.thread", tmsg)
    t = store.set_task_status(task["id"], "review", result=reply)
    if t:
        await broadcast("task.updated", t)
    room = store.get_room(task["room_id"])
    if room and room["slug"] != store.HOME_SLUG:
        note = store.add_home_chat(
            "agent", f"✅ Follow-up on card #{task['id']} done in {room['name']} — back in Review",
            ref_room_id=room["id"], task_id=task["id"])
        await broadcast("home.message", note)


_CHAT_WRAP = (
    "The owner is TALKING to you in the project room — this is conversation, not a "
    "ticket. Answer briefly (a few lines, simple everyday English), grounded in the "
    "project's actual state (read files if it helps — you may READ, never modify). "
    "If the message actually needs real work done, say so and suggest they send it "
    "as a ticket.\n\nRecent conversation:\n{hist}\n\nOwner: {text}"
)


async def run_chat(rid: int, text: str, broadcast) -> None:
    """Chat-lane turn: answer in the room, read-only, no card."""
    task_like = {"room_id": rid, "id": 0}
    ctx = _ctx_for(task_like)
    if ctx is None:
        return
    ctx.readonly = True
    hist = store.list_chat(rid, 20)[:-1]              # everything before this message
    hist_txt = "\n".join(f"{m['role']}: {m['text'][:300]}" for m in hist) or "(none)"
    try:
        reply = await get_provider().run_task(
            _CHAT_WRAP.format(hist=hist_txt, text=text), ctx, None)
    except Exception as e:
        reply = f"(error: {str(e)[:160]})"
    msg = store.add_chat(rid, "agent", reply)
    await broadcast("chat.message", msg)


def recover() -> int:
    """Requeue cards orphaned in 'in_progress' by a crash/restart."""
    n = 0
    for r in store.list_rooms(include_home=True):
        for t in store.list_tasks(r["id"]):
            if t["status"] == "in_progress":
                store.set_task_status(t["id"], "todo")
                n += 1
    return n


_ROUTINE_WRAP = (
    "You are running the scheduled routine \"{title}\" in the room \"{room}\". "
    "The owner is not watching — work autonomously, no questions.\n\n"
    "INSTRUCTION:\n{body}\n\n"
    "Do the work now, directly in this run. Create a CARD only if the instruction "
    "itself asks to file/queue tracked work for later (e.g. 'post a blog task') — "
    "then per card:\n"
    "  curl -X POST http://127.0.0.1:{port}/api/rooms/{rid}/tasks "
    "-H 'Content-Type: application/json' -d '{{\"title\": \"...\", \"body\": \"...\"}}'\n"
    "For a routine check/chore that you complete right here, do NOT create any card.\n"
    "When finished reply 2-3 short lines: what you did or found, simple English."
)


async def run_routine(r: dict, run_id: int, broadcast) -> None:
    """A fire = a direct agent run, NOT a card. The run row carries the tick;
    the agent files cards only when the instruction genuinely asks for them."""
    from .. import config
    ctx = _ctx_for({"room_id": r["room_id"]})
    room = store.get_room(r["room_id"])
    if ctx is None or room is None:
        store.finish_routine_run(run_id, "failed", "(room was deleted)")
        return
    port = int(config.load_config().get("web", {}).get("port", 7777))
    instruction = _ROUTINE_WRAP.format(
        title=r["title"], room=room["name"], body=r["body"] or r["title"],
        port=port, rid=r["room_id"])
    try:
        reply = await get_provider().run_task(instruction, ctx, None)
    except Exception as e:
        reply = f"({e})"
    failed = reply.startswith("(")
    store.finish_routine_run(run_id, "failed" if failed else "ok", reply)
    run = {"id": run_id, "routine_id": r["id"], "room_id": r["room_id"],
           "title": r["title"], "room_name": room["name"],
           "status": "failed" if failed else "ok"}
    await broadcast("routine.ran", run)
    if failed:                                        # failures must reach the owner
        msg = store.add_chat(r["room_id"], "agent",
                             f"❌ Routine \"{r['title']}\" failed — {reply[:300]}")
        await broadcast("chat.message", msg)


async def routine_loop(broadcast, interval: int = 60):
    """When a routine is due, run it directly (no card) and record the tick;
    reminders fire here too."""
    print("[worker] routine scheduler started")
    while True:
        try:
            due = store.due_reminders()
            for rem in due:
                await broadcast("reminder.due", rem)
                hmsg = store.add_home_chat("agent", f"⏰ Reminder: {rem['text']}")
                await broadcast("home.message", hmsg)
            if due:                                   # repeating ones moved forward
                await broadcast("reminders.changed", {})
            for r in store.due_routines():
                store.mark_routine_run(r["id"], r["schedule"])
                run = store.add_routine_run(r["id"], r["room_id"])
                await broadcast("routine.ran", {**run, "title": r["title"]})
                asyncio.create_task(run_routine(r, run["id"], broadcast))
        except Exception as e:
            print(f"[routines] error: {e}")
        await asyncio.sleep(interval)


RUNNING: dict[int, asyncio.Task] = {}     # live runs, stoppable by card id


def _register(tid: int, atask: asyncio.Task) -> None:
    RUNNING[tid] = atask
    atask.add_done_callback(lambda _f: RUNNING.pop(tid, None))


def cancel_task(tid: int) -> bool:
    """Stop a running card mid-flight. The guarded runner parks it in Review."""
    atask = RUNNING.get(tid)
    if not atask:
        return False
    atask.cancel()
    return True


async def _stopped(task: dict, broadcast) -> None:
    t = store.set_task_status(task["id"], "review", result="(stopped by you)")
    if t:
        await broadcast("task.updated", t)
    store.add_task_log(task["id"], "⏹ stopped by the owner")


async def _run_guarded(task: dict, broadcast) -> None:
    try:
        await run_one(task, broadcast)
    except asyncio.CancelledError:
        await _stopped(task, broadcast)
    except Exception as e:
        print(f"[worker] card #{task['id']} crashed: {e}")
        store.set_task_status(task["id"], "review", result=f"(worker error: {str(e)[:200]})")


def spawn_followup(task: dict, reply_text: str, broadcast) -> None:
    async def _guarded():
        try:
            await run_followup(task, reply_text, broadcast)
        except asyncio.CancelledError:
            await _stopped(task, broadcast)
        except Exception as e:
            print(f"[worker] follow-up on #{task['id']} crashed: {e}")
            store.set_task_status(task["id"], "review", result=f"(worker error: {str(e)[:200]})")
    _register(task["id"], asyncio.create_task(_guarded()))


async def watch_loop(broadcast, interval: int = 2):
    n = recover()
    if n:
        print(f"[worker] requeued {n} card(s) orphaned by a restart")
    from .. import config
    cap = max(1, min(4, config.concurrency()))   # cards run in parallel, bounded;
    running: set[int] = set()                    # brain's semaphore caps claude procs anyway
    print(f"[worker] ticket watcher started (up to {cap} cards in parallel)")
    while True:
        try:
            while len(running) < cap:
                task = store.claim_next_todo()
                if not task:
                    break
                await broadcast("task.updated", task)   # card slides to In progress live
                running.add(task["id"])
                t = asyncio.create_task(_run_guarded(task, broadcast))
                t.add_done_callback(lambda _f, tid=task["id"]: running.discard(tid))
                _register(task["id"], t)
        except Exception as e:
            print(f"[worker] error: {e}")
        await asyncio.sleep(interval)
