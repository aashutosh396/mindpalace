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
    "You are the resident agent of the project room '{name}'.\n"
    "The project's repositories — do your work INSIDE these paths:\n{repos}\n"
    "Project assets folder (briefs, designs, uploads the owner gave you): {assets}\n"
    "You have full machine access; stay within this project's world unless the "
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
    "You are the PALACE-KEEPER — you work general cards about the palace itself "
    "(the owner's project workspace), not any single project.\n"
    "You can manage the palace through its local API at http://127.0.0.1:{port}:\n"
    "  GET  /api/projects                     — list rooms\n"
    "  POST /api/projects {{\"name\": ...}}      — create a room\n"
    "  POST /api/projects/<id>/repos {{\"path\": \"/abs/folder\"}}\n"
    "      — attach a project's MAIN FOLDER to a room (nested git repos are "
    "auto-discovered; first attach becomes the working directory)\n"
    "Typical chores: scan the owner's machine or vault for projects, create rooms "
    "for them, attach their folders. Prefer editing the palace via the API, files "
    "via the filesystem."
)


def _ctx_for(task: dict) -> TaskContext | None:
    from .. import config
    p = store.get_project(task["project_id"])
    if not p:
        return None
    repos = store.repo_paths_for(task["project_id"])
    assets = str(store.project_dir(p["slug"]) / "assets")
    system = _SYSTEM.format(name=p["name"],
                            repos="\n".join(f"  - {r}" for r in repos) or "  (none attached yet)",
                            assets=assets)
    if p["slug"] == store.HOME_SLUG:
        port = int(config.load_config().get("web", {}).get("port", 7777))
        system = _KEEPER.format(port=port)
    return TaskContext(project_slug=p["slug"], repo_paths=repos, asset_dir=assets, system=system)


async def run_one(task: dict, broadcast) -> None:
    ctx = _ctx_for(task)
    if ctx is None:                                   # project vanished under the card
        store.set_task_status(task["id"], "done", result="(project was deleted)")
        return

    async def on_event(ev):
        store.add_task_log(task["id"], ev.text)     # durable trail for the card modal
        await broadcast("task.progress", {"task_id": task["id"], "text": ev.text})

    instruction = _WRAP.format(tid=task["id"], task=task["body"] or task["title"])
    reply = await get_provider().run_task(instruction, ctx, on_event)

    t = store.set_task_status(task["id"], "review", result=reply)
    msg = store.add_chat(task["project_id"], "agent", reply, task_id=task["id"])
    await broadcast("chat.message", msg)
    if t:
        await broadcast("task.updated", t)


_CHAT_WRAP = (
    "The owner is TALKING to you in the project room — this is conversation, not a "
    "ticket. Answer briefly (a few lines, simple everyday English), grounded in the "
    "project's actual state (read files if it helps — you may READ, never modify). "
    "If the message actually needs real work done, say so and suggest they send it "
    "as a ticket.\n\nRecent conversation:\n{hist}\n\nOwner: {text}"
)


async def run_chat(pid: int, text: str, broadcast) -> None:
    """Chat-lane turn: answer in the corridor, read-only, no card."""
    task_like = {"project_id": pid, "id": 0}
    ctx = _ctx_for(task_like)
    if ctx is None:
        return
    ctx.readonly = True
    hist = store.list_chat(pid, 20)[:-1]              # everything before this message
    hist_txt = "\n".join(f"{m['role']}: {m['text'][:300]}" for m in hist) or "(none)"
    try:
        reply = await get_provider().run_task(
            _CHAT_WRAP.format(hist=hist_txt, text=text), ctx, None)
    except Exception as e:
        reply = f"(error: {str(e)[:160]})"
    msg = store.add_chat(pid, "agent", reply)
    await broadcast("chat.message", msg)


def recover() -> int:
    """Requeue cards orphaned in 'in_progress' by a crash/restart."""
    n = 0
    for p in store.list_projects():
        for t in store.list_tasks(p["id"]):
            if t["status"] == "in_progress":
                store.set_task_status(t["id"], "todo")
                n += 1
    return n


async def watch_loop(broadcast, interval: int = 2):
    n = recover()
    if n:
        print(f"[worker] requeued {n} card(s) orphaned by a restart")
    print("[worker] ticket watcher started")
    while True:
        try:
            task = store.claim_next_todo()
            if task:
                await broadcast("task.updated", task)   # card slides to In progress live
                await run_one(task, broadcast)
                continue                                # drain the queue before sleeping
        except Exception as e:
            print(f"[worker] error: {e}")
        await asyncio.sleep(interval)
