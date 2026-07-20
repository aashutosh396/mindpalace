"""One inbound-message pipeline for every gateway (web GUI, Discord bridge).

A room message goes through the same stations regardless of where it was
typed: start-accept (files the pending proposal) → close-by-id → project
auto-connect → triage → chat turn or card. Gateways just deliver text here
and mirror the broadcasts back out.
"""
from __future__ import annotations

import asyncio
import re

from . import store, triage, worker


async def handle_room_message(rid: int, text: str, broadcast,
                              lane: str = "auto") -> dict:
    """Returns {message, task, lane?} exactly like the web endpoint did."""
    room = store.get_room(rid)
    if not room:
        return {"error": "room not found"}

    if re.match(r"(?i)^(yes[,! ]*)?(start|go|do it|start it|go ahead|yes)[.! ]*$", text) \
            and room.get("pending_proposal"):
        prop = room["pending_proposal"]
        umsg = store.add_chat(rid, "user", text)
        await broadcast("chat.message", umsg)
        title = prop.split(" — ")[0][:120]
        task = store.create_task(rid, title, f"{prop}\n\n(accepted from my proposal)")
        store.set_proposal(rid, None)
        amsg = store.add_chat(rid, "agent",
                              f"🛠️ Queued — card #{task['id']}. I'll report here when done.",
                              task_id=task["id"])
        await broadcast("task.created", task)
        await broadcast("chat.message", amsg)
        return {"message": umsg, "task": task}

    m = re.match(r"(?i)^close\s+(?:card|task|ticket)?\s*#?(\d+)$", text)
    if m:
        tid = int(m.group(1))
        umsg = store.add_chat(rid, "user", text)
        await broadcast("chat.message", umsg)
        t = store.get_task(tid)
        if t and t["room_id"] == rid:
            t = store.set_task_status(tid, "done")
            reply = f"Closed card #{tid} — {t['title']}"
            await broadcast("task.updated", t)
        else:
            reply = f"No card #{tid} in this room."
        amsg = store.add_chat(rid, "agent", reply, task_id=tid if t else None)
        await broadcast("chat.message", amsg)
        return {"message": umsg, "task": None}

    # projects mentioned in the message connect themselves to the room
    if room["slug"] != store.HOME_SLUG:
        hits = store.match_projects_in_text(text, exclude_room=rid)[:3]
        if hits:
            for p in hits:
                store.connect_project(rid, p["id"])
            await broadcast("room.projects", {"room_id": rid})
            note = store.add_chat(
                rid, "agent",
                "🔗 Connected project" + ("s" if len(hits) > 1 else "")
                + " to this room: " + ", ".join(p["name"] for p in hits))
            await broadcast("chat.message", note)

    if lane == "auto":
        lane = await triage.classify(text)

    if lane == "chat":
        msg = store.add_chat(rid, "user", text)
        await broadcast("chat.message", msg)
        asyncio.get_running_loop().create_task(worker.run_chat(rid, text, broadcast))
        return {"message": msg, "task": None, "lane": "chat"}

    kind = "goal" if lane == "goal" else "task"
    task = store.create_task(rid, text.splitlines()[0][:120], text, kind=kind,
                             promise=worker.DEFAULT_PROMISE if kind == "goal" else None)
    msg = store.add_chat(rid, "user", text, task_id=task["id"])
    await broadcast("chat.message", msg)
    await broadcast("task.created", task)
    return {"message": msg, "task": task, "lane": kind}
