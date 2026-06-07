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
    # caps match the compaction budgets so the FULL distilled file loads (no silent tail-drop)
    parts = []
    agent = _read(config.AGENT_FILE(), 4000)
    if agent:
        parts.append("WHO YOU ARE (your persona):\n" + agent)
    user = _read(config.USER_FILE(), config.user_budget() + 1000)
    if user:
        parts.append("WHO YOU SERVE (the owner):\n" + user)
    return "\n\n".join(parts)


def memory_block() -> str:
    mem = _read(config.MEMORY_FILE(), config.memory_budget() + 1000)
    return ("YOUR MEMORY (durable facts, conventions, gotchas):\n" + mem) if mem else ""


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
