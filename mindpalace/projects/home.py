"""The Home hall — one conversation that reaches every room.

The owner just talks. The concierge decides, in ONE model call that also writes
the user-facing reply:
  • chat    → answer directly (it sees every room's board + projects)
  • file    → work for an EXISTING room → ticket goes there
  • general → work about the palace itself → the keeper's hidden workroom

ROOMS ARE THE OWNER'S — the concierge NEVER creates one. When no room fits, it
answers in chat and suggests making a room (or naming one). Every routing is
announced in the reply so a wrong guess is visible and cheap to correct.
"""
from __future__ import annotations

import asyncio
import difflib
import json

from . import store

_PROMPT = (
    "You are the concierge of the owner's palace. ROOMS are the owner's channels "
    "(each has a kanban board, chat, connected projects). PROJECTS are inventory "
    "(folders/repos on disk) managed by the palace-keeper.\n\n"
    "THE ROOMS RIGHT NOW:\n{rooms}\n\n"
    "RECENT HALL CONVERSATION:\n{hist}\n\n"
    "THE OWNER JUST SAID:\n{text}\n\n"
    "Decide what this is and answer with STRICT JSON only (no prose, no fences):\n"
    '  {{"action":"chat","reply":"..."}}\n'
    '      conversation, questions, status checks — answer from the data above. '
    "ALSO use this when work fits NO existing room: say so and suggest the owner "
    "create a room (you can never create rooms — they are the owner's).\n"
    '  {{"action":"file","room":"<existing slug>","title":"...","body":"...","reply":"..."}}\n'
    '      work that belongs to an EXISTING room (match loosely by name/topic/projects)\n'
    '  {{"action":"general","title":"...","body":"...","reply":"..."}}\n'
    '      work about the PALACE ITSELF — scanning for projects, managing the '
    "project inventory, machine-wide chores. Goes to the palace-keeper.\n\n"
    "Rules: body = the owner's full instruction. reply = 1-3 short lines, simple "
    "English; when you file, SAY where it went. JSON only."
)


def _rooms_block() -> str:
    idx = store.rooms_index()
    if not idx:
        return "(no rooms yet — the owner hasn't created any)"
    lines = []
    for r in idx:
        c = r["counts"]
        lines.append(
            f"- {r['slug']} (\"{r['name']}\") — projects: {', '.join(r['projects']) or 'none'}; "
            f"todo {c['todo']}, doing {c['in_progress']}, review {c['review']}, done {c['done']}"
            + (f"; open: {'; '.join(r['open_titles'])}" if r["open_titles"] else ""))
    return "\n".join(lines)


def _parse(raw: str) -> dict | None:
    s = raw.strip()
    if s.startswith("```"):
        s = s.strip("`").lstrip("json").strip()
    try:
        start = s.index("{")
        return json.loads(s[start:s.rindex("}") + 1])
    except (ValueError, json.JSONDecodeError):
        return None


async def _decide(text: str) -> dict:
    from ..core import brain
    hist = store.list_home_chat(16)[:-1]
    prompt = _PROMPT.format(
        rooms=_rooms_block(),
        hist="\n".join(f"{m['role']}: {m['text'][:200]}" for m in hist) or "(empty)",
        text=text.strip()[:1500])
    try:
        proc = await asyncio.create_subprocess_exec(
            brain.claude_bin(), "-p", prompt, "--model", "sonnet",
            env=brain._env(),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=90)
        d = _parse(out.decode(errors="replace"))
        if d and d.get("action") in ("chat", "file", "general"):
            return d
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
    return {"action": "chat", "reply": "(I hit an error deciding — say it again, or open a "
                                       "room and send it there directly.)"}


def _match_room(slug_or_name: str) -> dict | None:
    rooms = store.list_rooms()
    by_slug = {r["slug"]: r for r in rooms}
    if slug_or_name in by_slug:
        return by_slug[slug_or_name]
    close = difflib.get_close_matches(slug_or_name.lower(),
                                      [r["slug"] for r in rooms]
                                      + [r["name"].lower() for r in rooms], n=1, cutoff=0.6)
    if close:
        for r in rooms:
            if close[0] in (r["slug"], r["name"].lower()):
                return r
    return None


async def handle(text: str, broadcast) -> None:
    """One hall turn: decide → execute → reply. The user message is already stored."""
    d = await _decide(text)
    action, ref_rid, task_id = d.get("action"), None, None
    reply = d.get("reply") or "Done."

    if action == "general":
        room = store.ensure_home_room()
        title = (d.get("title") or text.splitlines()[0])[:120]
        task = store.create_task(room["id"], title, d.get("body") or text)
        ref_rid, task_id = room["id"], task["id"]
        await broadcast("task.created", task)

    elif action == "file":
        room = _match_room(d.get("room", ""))
        if room is None:                             # named a room that doesn't exist
            reply = (f"No room matches \"{d.get('room', '?')}\" — rooms are yours to make. "
                     "Create one in the sidebar, then send this again (or name another room).")
        else:
            title = (d.get("title") or text.splitlines()[0])[:120]
            body = d.get("body") or text
            task = store.create_task(room["id"], title, body)
            ref_rid, task_id = room["id"], task["id"]
            msg = store.add_chat(room["id"], "user", body, task_id=task_id)
            await broadcast("chat.message", msg)
            await broadcast("task.created", task)

    hmsg = store.add_home_chat("agent", reply, ref_room_id=ref_rid, task_id=task_id)
    await broadcast("home.message", hmsg)
