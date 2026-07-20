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

from .. import config
from . import store
from ..providers import get_provider
from ..providers.base import TaskContext

_SYSTEM = (
    "You are the resident agent of the room '{name}'.\n"
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
    "one. Simple everyday English. The reply lands on the ticket for the owner's "
    "review — no essays, no file attachments."
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
    system = _SYSTEM.format(name=r["name"], repos=repos_block, assets=assets)
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


async def _finish(task: dict, reply: str, broadcast) -> None:
    t = store.set_task_status(task["id"], "review", result=reply)
    room = store.get_room(task["room_id"])
    if room and room["slug"] == store.HOME_SLUG:
        # keeper cards: the hall IS their room — deliver the result there
        hmsg = store.add_home_chat("agent", reply, ref_room_id=room["id"], task_id=task["id"])
        await broadcast("home.message", hmsg)
    else:
        msg = store.add_chat(task["room_id"], "agent", reply, task_id=task["id"])
        await broadcast("chat.message", msg)
        if room:                                     # and announce delivery in the hall
            note = store.add_home_chat(
                "agent", f"✅ Card #{task['id']} done in {room['name']} — waiting in Review",
                ref_room_id=room["id"], task_id=task["id"])
            await broadcast("home.message", note)
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


async def routine_loop(broadcast, interval: int = 60):
    """Recurring cards: when a routine is due, drop its card in 'todo' —
    the ticket worker takes it from there like any other card."""
    print("[worker] routine scheduler started")
    while True:
        try:
            for r in store.due_routines():
                task = store.create_task(r["room_id"], r["title"], r["body"],
                                         created_by="routine")
                store.mark_routine_run(r["id"], r["schedule"])
                await broadcast("task.created", task)
        except Exception as e:
            print(f"[routines] error: {e}")
        await asyncio.sleep(interval)


async def _run_guarded(task: dict, broadcast) -> None:
    try:
        await run_one(task, broadcast)
    except Exception as e:
        print(f"[worker] card #{task['id']} crashed: {e}")
        store.set_task_status(task["id"], "review", result=f"(worker error: {str(e)[:200]})")


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
        except Exception as e:
            print(f"[worker] error: {e}")
        await asyncio.sleep(interval)
