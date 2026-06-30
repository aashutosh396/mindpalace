"""
Post an update to a channel via webhook — used by the agent, by cron jobs, and by the
background job watcher to report into the HOME channel (or any named channel you've hooked).

Webhooks live in user-data config ("webhooks": {"home": "...", "<name>": "..."}).
  python3 -m mindpalace.notify "backups done"            # -> home channel
  python3 -m mindpalace.notify "deploy ok" --channel ops # -> 'ops' channel
Add one with:  mindpalace add-webhook <name> <discord-webhook-url>
"""
from __future__ import annotations

import http.client
import json
import ssl
import sys

from .. import config


import re as _re

_SEP = _re.compile(r"^:?-{1,}:?$")


def _align_tables(text: str) -> str:
    """Convert markdown pipe-tables → clean space-aligned columns that line up in a monospace
    (code-block) context. Non-table text passes through untouched. Deterministic — doesn't rely
    on the model formatting the table."""
    lines = (text or "").split("\n")
    out, i = [], 0
    while i < len(lines):
        if "|" in lines[i] and lines[i].strip():
            j, block = i, []
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                block.append(lines[j]); j += 1
            if len(block) >= 2:                              # 2+ piped lines = a table
                rows = []
                for ln in block:
                    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                    if cells and all(_SEP.match(c or "-") for c in cells):
                        continue                             # drop the |---|---| separator row
                    rows.append(cells)
                if rows:
                    ncol = max(len(r) for r in rows)
                    rows = [r + [""] * (ncol - len(r)) for r in rows]
                    w = [max(len(r[c]) for r in rows) for c in range(ncol)]
                    fmt = lambda r: "  ".join(r[c].ljust(w[c]) for c in range(ncol)).rstrip()
                    aligned = [fmt(rows[0]), "  ".join("-" * w[c] for c in range(ncol))]
                    aligned += [fmt(r) for r in rows[1:]]
                    out.append("\n".join(aligned)); i = j; continue
        out.append(lines[i]); i += 1
    return "\n".join(out)


_TABLE_WIDTH_BUDGET = 58   # aligned cols past this wrap + shatter in Discord → render vertically


def _parse_rows(block: list[str]) -> list[list[str]]:
    """Pipe-table lines → rows of cells (separator row dropped, ragged rows padded)."""
    rows = []
    for ln in block:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells and all(_SEP.match(c or "-") for c in cells):
            continue
        rows.append(cells)
    if rows:
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
    return rows


def _aligned_block(rows: list[list[str]]) -> tuple[str, int]:
    """Space-aligned monospace columns + the total rendered width (to decide if it fits)."""
    ncol = len(rows[0])
    w = [max(len(r[c]) for r in rows) for c in range(ncol)]
    fmt = lambda r: "  ".join(r[c].ljust(w[c]) for c in range(ncol)).rstrip()
    aligned = [fmt(rows[0]), "  ".join("-" * w[c] for c in range(ncol))] + [fmt(r) for r in rows[1:]]
    return "\n".join(aligned), sum(w) + 2 * (ncol - 1)


def _vertical_block(rows: list[list[str]]) -> str:
    """Wide table → one readable record per row: a bold title (first column) then `field: value`
    bullet lines. Wraps naturally on any screen instead of breaking column alignment."""
    header = rows[0]
    out = []
    for r in rows[1:]:
        title = (r[0] if r else "").strip()
        out.append(f"**{title}**" if title else "•")
        for c in range(1, len(header)):
            val = (r[c] if c < len(r) else "").strip()
            if val and val != "-":
                lbl = header[c].strip()
                out.append(f"   • {lbl}: {val}" if lbl else f"   • {val}")
        out.append("")                                   # blank line between records
    return "\n".join(out).rstrip()


def prettify_tables(text: str) -> str:
    """Make markdown tables readable in Discord (they don't render natively). Narrow tables →
    aligned monospace in a ``` fence. WIDE tables → vertical records (bold title + field:value
    lines), because fixed columns wrap and shatter once they exceed Discord's width."""
    lines = (text or "").split("\n")
    out, i = [], 0
    while i < len(lines):
        if "|" in lines[i] and lines[i].strip():
            j, block = i, []
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                block.append(lines[j]); j += 1
            if len(block) >= 2:
                rows = _parse_rows(block)
                if len(rows) >= 2:
                    aligned, width = _aligned_block(rows)
                    out.append("```\n" + aligned + "\n```" if width <= _TABLE_WIDTH_BUDGET
                               else _vertical_block(rows))
                    i = j; continue
        out.append(lines[i]); i += 1
    return "\n".join(out)


def _strip_md(text: str) -> str:
    """Markdown doesn't render inside a monospace box, so '**bold**', '## Heading', and `code`
    show as literal junk. Make it READABLE: drop bold/code markers, turn headings into clean
    UPPERCASE lines, normalize bullets to '• '. Tables (handled by _align_tables) pass through."""
    out = []
    for ln in (text or "").split("\n"):
        h = _re.match(r"^\s*#{1,6}\s+(.*)$", ln)
        if h:                                            # '## ✓ All good' → '✓ ALL GOOD'
            out.append(h.group(1).strip().rstrip("#").strip().upper()); continue
        s = _re.sub(r"\*\*(.+?)\*\*", r"\1", ln)         # **bold**
        s = _re.sub(r"__(.+?)__", r"\1", s)              # __bold__
        s = s.replace("`", "")                            # inline-code backticks
        s = _re.sub(r"^(\s*)[-*]\s+", r"\1• ", s)        # - / * bullets → •
        out.append(s)
    return "\n".join(out)


def box(title: str, body: str, accent: str = "cyan") -> str:
    """Tidy ansi colour box for system messages — coloured title, body below.
    Shared format for heartbeat / notifications / system messages."""
    fg = {"cyan": "1;36", "green": "0;32", "yellow": "1;33", "red": "1;31", "blue": "1;34"}
    fence = chr(96) * 3
    nl = chr(10)
    # strip markdown (won't render in monospace) THEN align tables, then protect the fence
    body = _align_tables(_strip_md((body or "").strip())).replace(fence, "ʼʼʼ")
    if len(body) > 1700:
        body = body[:1699].rstrip() + "…"
    esc = chr(27)
    title_line = esc + "[" + fg.get(accent, "1;36") + "m" + title + esc + "[0m"
    return fence + "ansi" + nl + title_line + nl + nl + body + nl + fence


def notify(message: str, channel: str = "home", username: str = "mindpalace") -> bool:
    url = config.webhooks().get(channel)
    if not url or not url.startswith("https://discord.com"):
        print(f"(notify: no webhook for '{channel}' — add with `mindpalace add-webhook {channel} <url>`)")
        return False
    path = url[len("https://discord.com"):]
    payload = json.dumps({"content": message[:1900], "username": username}).encode()
    conn = http.client.HTTPSConnection("discord.com", timeout=10, context=ssl.create_default_context())
    conn.request("POST", path, body=payload,
                 headers={"Content-Type": "application/json",
                          "User-Agent": "mindpalace/0.1",
                          "Content-Length": str(len(payload))})
    r = conn.getresponse(); r.read(); conn.close()
    return r.status in (200, 204)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    channel = "home"
    if "--channel" in argv:
        i = argv.index("--channel")
        channel = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    msg = " ".join(argv).strip() or "(empty)"
    print("sent" if notify(msg, channel) else "not sent")


if __name__ == "__main__":
    main()
