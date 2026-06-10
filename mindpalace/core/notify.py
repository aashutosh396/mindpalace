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


def box(title: str, body: str, accent: str = "cyan") -> str:
    """Tidy ansi colour box for system messages — coloured title, body below.
    Shared format for heartbeat / notifications / system messages."""
    fg = {"cyan": "1;36", "green": "0;32", "yellow": "1;33", "red": "1;31", "blue": "1;34"}
    fence = chr(96) * 3
    nl = chr(10)
    body = (body or "").strip().replace(fence, "ʼʼʼ")
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
