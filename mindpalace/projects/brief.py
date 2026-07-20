"""The morning brief — the hall reports to the owner, once a day.

Deterministic (pure SQL, no model call): what's waiting in Review, what got
done, what's still running. Generated lazily the first time the hall is opened
each day, stored as a home_chat row with role='brief'.
"""
from __future__ import annotations

from . import store


def ensure_daily_brief() -> dict | None:
    """Insert today's brief if it doesn't exist yet. Returns the new row or None."""
    if store.has_brief_today():
        return None
    if not store.list_rooms() and not store.all_tasks():
        return None                                  # empty palace — nothing to say
    from .. import config
    name = config.load_config().get("web", {}).get("owner_name", "")
    s = store.brief_stats()
    lines = [f"🌅 Morning brief{' — ' + name if name else ''}"]

    if s["review"]:
        lines.append(f"Waiting for your review ({len(s['review'])}):")
        for t in s["review"][:6]:
            failed = (t["result"] or "").startswith("(")
            lines.append(f"  • #{t['id']} {t['title'][:60]} — {t['room']}"
                         + ("  ⚠️ looks failed" if failed else ""))
        if len(s["review"]) > 6:
            lines.append(f"  … and {len(s['review']) - 6} more")
    else:
        lines.append("Nothing waiting for review.")

    if s["done"]:
        lines.append(f"Closed in the last day: {len(s['done'])} "
                     f"({', '.join(sorted({t['room'] for t in s['done']}))})")
    if s["working"]:
        lines.append("Still working: " +
                     ", ".join(f"#{t['id']} {t['title'][:40]} ({t['room']})"
                               for t in s["working"][:4]))
    if s["created"]:
        lines.append(f"{s['created']} card(s) created in the last day.")
    if len(lines) == 2 and not s["review"]:
        lines.append("A quiet day in the palace.")

    return store.add_home_chat("brief", "\n".join(lines))
