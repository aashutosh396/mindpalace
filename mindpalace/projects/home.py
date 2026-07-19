"""The Home room (the hall) — one conversation that reaches every room.

The owner just talks. The concierge decides, in ONE model call that also writes
the user-facing reply:
  • chat    → answer directly (it sees every room's board, so cross-room
              status questions work)
  • file    → the message is work for an EXISTING room → ticket goes there
  • create  → a genuinely new project → room is created, ticket filed inside

Guard rails: prefer filing over creating (fuzzy-match the room index first);
every routing is announced in the reply so a wrong guess is visible and cheap
to correct ("move card N to X" can be said in the target room or here).
"""
from __future__ import annotations

import asyncio
import difflib
import json

from . import store

_PROMPT = (
    "You are the concierge of the owner's project palace. Every project is a room "
    "with a kanban board (todo/in progress/review/done), a chat, repos and assets.\n\n"
    "THE ROOMS RIGHT NOW:\n{rooms}\n\n"
    "RECENT HALL CONVERSATION:\n{hist}\n\n"
    "THE OWNER JUST SAID:\n{text}\n\n"
    "Decide what this is and answer with STRICT JSON only (no prose, no fences):\n"
    '  {{"action":"chat","reply":"..."}}\n'
    '      conversation, questions, status checks — answer from the room data above\n'
    '  {{"action":"file","room":"<existing slug>","title":"...","body":"...","reply":"..."}}\n'
    '      work that belongs to an EXISTING room (match loosely by name/topic)\n'
    '  {{"action":"create","room_name":"...","title":"...","body":"...","reply":"..."}}\n'
    '      work for a genuinely NEW project no room covers\n'
    '  {{"action":"general","title":"...","body":"...","reply":"..."}}\n'
    '      work about the PALACE ITSELF, not one project — scanning folders for '
    'projects, creating/organizing rooms, machine-wide chores. Files a general card '
    'the palace-keeper works.\n\n'
    "Rules: STRONGLY prefer file over create — create only when nothing plausibly "
    "matches. body = the owner's full instruction. reply = 1-3 short lines, simple "
    "English, and when you file/create, SAY where it went so a wrong guess is easy "
    "to catch. JSON only."
)


def _rooms_block() -> str:
    idx = store.rooms_index()
    if not idx:
        return "(no rooms yet)"
    lines = []
    for r in idx:
        c = r["counts"]
        lines.append(f"- {r['slug']} (\"{r['name']}\") — todo {c['todo']}, doing {c['in_progress']}, "
                     f"review {c['review']}, done {c['done']}"
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
        if d and d.get("action") in ("chat", "file", "create", "general"):
            return d
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
    return {"action": "chat", "reply": "(I hit an error deciding — say it again, or open a "
                                       "room and send it there directly.)"}


def _match_room(slug_or_name: str) -> dict | None:
    projects = store.list_projects()
    by_slug = {p["slug"]: p for p in projects}
    if slug_or_name in by_slug:
        return by_slug[slug_or_name]
    close = difflib.get_close_matches(slug_or_name.lower(),
                                      [p["slug"] for p in projects]
                                      + [p["name"].lower() for p in projects], n=1, cutoff=0.6)
    if close:
        for p in projects:
            if close[0] in (p["slug"], p["name"].lower()):
                return p
    return None


async def handle(text: str, broadcast) -> None:
    """One hall turn: decide → execute → reply. The user message is already stored."""
    d = await _decide(text)
    action, ref_pid, task_id = d.get("action"), None, None

    if action == "general":                      # palace-level work → the Home workroom
        p = store.ensure_home_project()
        title = (d.get("title") or text.splitlines()[0])[:120]
        task = store.create_task(p["id"], title, d.get("body") or text)
        ref_pid, task_id = p["id"], task["id"]
        await broadcast("task.created", task)

    if action in ("file", "create"):
        title = (d.get("title") or text.splitlines()[0])[:120]
        body = d.get("body") or text
        p = _match_room(d.get("room", "")) if action == "file" else None
        if p is None and action == "file":          # model named a room that doesn't exist
            action = "create"
        if action == "create":
            p = store.create_project(d.get("room_name") or d.get("room") or title[:40])
            await broadcast("project.created", p)
        ref_pid = p["id"]
        task = store.create_task(ref_pid, title, body)
        task_id = task["id"]
        msg = store.add_chat(ref_pid, "user", body, task_id=task_id)   # the room keeps the record
        await broadcast("chat.message", msg)
        await broadcast("task.created", task)

    reply = d.get("reply") or "Done."
    hmsg = store.add_home_chat("agent", reply, ref_project_id=ref_pid, task_id=task_id)
    await broadcast("home.message", hmsg)
