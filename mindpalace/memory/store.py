"""Durable text memory + identity files — read helpers for the briefing."""
from __future__ import annotations

import time
from .. import config
from .session_store import SessionStore

_store: SessionStore | None = None


def store() -> SessionStore:
    global _store
    if _store is None:
        _store = SessionStore()
    return _store


def session_id() -> str:
    return time.strftime("%Y-%m-%d")


def _read(path, cap):
    try:
        c = path.read_text().strip()
        return c[:cap] if c else ""
    except FileNotFoundError:
        return ""


def identity_block() -> str:
    """Brain-style WORKING memory — kept tiny so each prompt stays light. The owner's essence
    + a map of what's known live in CORE.md; the full USER.md / MEMORY.md / vault are long-term,
    recalled on demand. Before CORE.md exists, fall back to a trimmed USER.md so nothing's empty."""
    parts = []
    agent = _read(config.AGENT_FILE(), 4000)
    if agent:
        parts.append("WHO YOU ARE (your persona):\n" + agent)
    core = _read(config.CORE_FILE(), config.core_budget() + 500)
    if core:
        parts.append(
            "WORKING MEMORY — your live, distilled sense of the owner + a MAP of what you know. "
            "This is your PRESENT memory. Deeper detail is long-term in USER.md, MEMORY.md and the "
            "vault: when the owner references something not in front of you, RECALL it (grep/read "
            "those) before assuming you don't know:\n" + core)
    else:                                            # bootstrap until the first compaction builds CORE.md
        user = _read(config.USER_FILE(), 1800)
        if user:
            parts.append("WHO YOU SERVE (the owner):\n" + user)
    return "\n\n".join(parts)


def memory_block() -> str:
    # Once CORE.md exists it carries the working memory + map, so we DON'T bulk-load MEMORY.md
    # each turn (it's long-term — recalled on demand). Only a small head as bootstrap before then.
    if config.CORE_FILE().exists():
        return ""
    mem = _read(config.MEMORY_FILE(), 1800)
    return ("YOUR MEMORY (durable facts — bootstrap; moves to working memory on next compaction):\n"
            + mem) if mem else ""


def recall_block(query: str, limit: int = 3) -> str:
    hits = store().search(query, limit=limit)
    if not hits:
        return ""
    lines = ["RELEVANT PAST CONTEXT (recalled from history):"]
    for role, content, ts in hits:
        date = time.strftime("%Y-%m-%d", time.localtime(ts))
        lines.append(f"  [{date}] {role}: {content[:300].strip().replace(chr(10), ' ')}")
    return "\n".join(lines)


def save_exchange(owner_text: str, agent_text: str) -> None:
    s, sid = store(), session_id()
    s.save_turn(sid, "Owner", owner_text)
    s.save_turn(sid, "Assistant", agent_text)
