"""Discord ↔ palace bridge — the GUI and Discord become ONE system.

Design (owner-approved):
  • Channels map to ROOMS by name (#sio ↔ room 'sio'); the hall channel maps
    to Home. Messages typed in Discord run the SAME pipeline as the GUI
    (inbox.handle_room_message / home.handle); agent replies, ✅ notices and
    ⏰ reminders mirror back to the mapped channel via the web bus.
  • The bridge is a SECOND bot with its OWN token — never the v2 Ginji bot's.
    Two clients on one token would both answer everything; a separate bot
    keeps the live v2 daemon completely untouched. Invite it only to the
    channels you want bridged.
  • Opt-in: token via  mindpalace bridge token <tok> ; then  mindpalace
    bridge on  and restart the daemon. Hall channel:  mindpalace bridge hall
    <channel_id>  (otherwise a channel named 'palace' or 'home' is the hall).

Loop safety: inbound ignores every bot author; outbound mirrors only
non-user roles. A message can never bounce.
"""
from __future__ import annotations

import asyncio

from .. import config
from ..projects import home, inbox, store

MAX_LEN = 1900                       # Discord cap is 2000; leave margin


def cfg() -> dict:
    return (config.load_config().get("web", {}) or {}).get("discord_bridge", {}) or {}


def enabled() -> bool:
    return bool(cfg().get("enabled")) and bool(config.read_secret("bridge_discord.token"))


def _hall_names() -> tuple:
    return ("palace", "home", "palace-hall", "mindpalace")


async def start(bus) -> None:
    """Run the bridge until cancelled. Guarded: missing lib/token → log + exit."""
    try:
        import discord
    except ImportError:
        print("[bridge] discord.py not installed — pip install 'mindpalace[discord]'")
        return
    token = config.read_secret("bridge_discord.token")
    if not token:
        print("[bridge] no token — run: mindpalace bridge token <tok>")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    hall_id = cfg().get("hall_channel_id")

    def room_for_channel(channel) -> dict | None:
        name = store.slugify(getattr(channel, "name", "") or "")
        for r in store.list_rooms():
            if r["slug"] == name:
                return r
        return None

    def channel_for_room(rid: int):
        room = store.get_room(rid)
        if not room:
            return None
        for ch in client.get_all_channels():
            if getattr(ch, "type", None) and str(ch.type) == "text" \
                    and store.slugify(ch.name) == room["slug"]:
                return ch
        return None

    def hall_channel():
        if hall_id:
            ch = client.get_channel(int(hall_id))
            if ch:
                return ch
        for ch in client.get_all_channels():
            if str(getattr(ch, "type", "")) == "text" and ch.name.lower() in _hall_names():
                return ch
        return None

    async def _send(ch, text: str):
        if not ch or not text:
            return
        try:
            await ch.send(text[:MAX_LEN])
        except Exception as e:
            print(f"[bridge] send failed: {e}")

    # ---- outbound: mirror palace events into Discord ----
    async def mirror(kind: str, data: dict):
        if not client.is_ready():
            return
        if kind == "home.message" and data.get("role") in ("agent", "brief"):
            await _send(hall_channel(), data.get("text", ""))
        elif kind == "chat.message" and data.get("role") == "agent":
            await _send(channel_for_room(data.get("room_id")), data.get("text", ""))
        elif kind == "reminder.due":
            await _send(hall_channel(), f"⏰ **Reminder:** {data.get('text', '')}")

    bus.listeners.append(mirror)

    @client.event
    async def on_ready():
        if not getattr(client, "_mp_announced", False):
            client._mp_announced = True
            print(f"[bridge] connected as {client.user}")
            hc = hall_channel()
            if hc:
                await _send(hc, "🏛️ palace bridge online — this channel is the hall; "
                                "channels named like your rooms are those rooms.")

    @client.event
    async def on_message(msg):
        if msg.author.bot or not msg.guild:
            return
        text = (msg.content or "").strip()

        # attachments land in the mapped room's assets, ride the message as paths
        room = room_for_channel(msg.channel)
        is_hall = (hall_id and msg.channel.id == int(hall_id)) or \
                  (not hall_id and msg.channel.name.lower() in _hall_names())
        if msg.attachments and (room or is_hall):
            slug = room["slug"] if room else store.ensure_home_room()["slug"]
            adir = store.room_dir(slug) / "assets"
            adir.mkdir(parents=True, exist_ok=True)
            saved = []
            for att in msg.attachments[:6]:
                dest = adir / att.filename.replace("/", "_")
                n = 2
                while dest.exists():
                    dest = adir / f"{dest.stem}-{n}{dest.suffix}"
                    n += 1
                try:
                    await att.save(dest)
                    saved.append(str(dest))
                except Exception:
                    pass
            if saved:
                text += ("\n\n[Attached files — read them as part of this message]:\n"
                         + "\n".join(f"- {p}" for p in saved))
        if not text:
            return

        if is_hall:
            hmsg = store.add_home_chat("user", text)
            await bus.broadcast("home.message", hmsg)
            asyncio.get_running_loop().create_task(home.handle(text, bus.broadcast))
        elif room:
            await inbox.handle_room_message(room["id"], text, bus.broadcast)
        # unmapped channels are silently ignored — invite the bot narrowly

    while True:                          # survive Discord drops without dying
        try:
            await client.start(token)
        except asyncio.CancelledError:
            try:
                await client.close()
            except Exception:
                pass
            raise
        except Exception as e:
            print(f"[bridge] connection lost: {e} — retrying in 15s")
            await asyncio.sleep(15)
