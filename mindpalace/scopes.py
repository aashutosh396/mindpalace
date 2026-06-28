"""
Channel-scoped personas — many assistants, ONE Discord connection.

A "scope" binds a Discord CHANNEL to a persona (system.md) + permission fence, all
carried by the existing MAIN bot. No new Discord application, no new token: the main
bot already sees the channel, it just answers there AS that persona.

Each scope = a triple, like a bot but keyed by channel instead of token:
  • system.md    scopes/<name>/system.md   (its persona — used as the system prompt)
  • policy       config["scopes"][<channel_id>]  = {name, permissions, allowed_tools}
  • channel      the binding key itself (one persona per channel)

This is the "easy auto-spawn" path: `mindpalace add-scope <name> <channel>` writes the
persona (Claude drafts it from one sentence) and the binding, then the next restart
makes that channel a working assistant. Scriptable — the owner OR the agent can call it.
"""
from __future__ import annotations

import re
import time

from . import config
from .bots import DRAFT_INSTRUCTION
from .core import brain


def registry() -> dict:
    """{channel_id(str): {name, permissions, allowed_tools, created}}."""
    return config.load_config().get("scopes", {})


def by_channel(channel_id) -> dict | None:
    return registry().get(str(channel_id))


def system_path(name: str):
    return config.home() / "scopes" / name / "system.md"


def load_system(name: str) -> str | None:
    p = system_path(name)
    return p.read_text() if p.exists() else None


def resolve_channel(token: str) -> int | None:
    """Accept a raw channel id or a pasted `<#123>` mention. `#name` can't be resolved
    offline (needs the live gateway) — caller should pass the numeric id for those."""
    if token is None:
        return None
    m = re.fullmatch(r"<#(\d+)>", token.strip())
    if m:
        return int(m.group(1))
    t = token.strip().lstrip("#")
    return int(t) if t.isdigit() else None


def draft_persona(intent: str) -> str:
    """Claude writes the scoped system prompt from a one-line intent (no API — claude CLI)."""
    return brain.ask_sync(DRAFT_INSTRUCTION.format(intent=intent), []).strip()


def add_scope(name: str, channel_id: int, *, system: str,
              permissions: str = "readonly", allowed_tools: str | None = None) -> dict:
    """Persist a scope (persona file + config binding). Returns the saved spec.
    Non-interactive — safe to call from the CLI, a script, or the agent itself."""
    name = (name or "").strip().replace(" ", "-")
    if not name:
        raise ValueError("scope needs a name")
    if not channel_id:
        raise ValueError("scope needs a channel id")
    if not (system or "").strip():
        raise ValueError("scope needs a persona (system prompt)")

    config.ensure_dirs()
    sp = system_path(name)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(system.strip() + "\n")

    cfg = config.load_config()
    spec = {
        "name": name,
        "permissions": permissions,
        "allowed_tools": allowed_tools,
        "created": time.strftime("%Y-%m-%d"),
    }
    cfg.setdefault("scopes", {})[str(channel_id)] = spec
    config.save_config(cfg)
    return spec


def remove(channel_id) -> bool:
    cfg = config.load_config()
    sc = cfg.get("scopes", {})
    if str(channel_id) in sc:
        sc.pop(str(channel_id))
        config.save_config(cfg)
        return True
    return False


def active_map() -> dict:
    """{channel_id(int): {name, permissions, allowed_tools, system}} for the gateway.
    Loads each persona once at startup; skips bindings whose persona file is missing."""
    out = {}
    for cid, spec in registry().items():
        try:
            icid = int(cid)
        except (TypeError, ValueError):
            continue
        sysmd = load_system(spec.get("name", ""))
        if not sysmd:
            continue
        out[icid] = {**spec, "system": sysmd}
    return out


# --- CLI ---------------------------------------------------------------------

def _ask(prompt, default=""):
    try:
        v = input(prompt).strip()
    except EOFError:
        v = ""
    return v or default


def add_scope_cli(argv: list[str]):
    """`mindpalace add-scope <name> <channel> [--intent "..."] [--tier full|readonly|custom]
    [--allow Read,Bash] [--system "..."|--system-file PATH]`.

    Scriptable: pass --intent (Claude drafts the persona) or --system/--system-file (verbatim).
    With neither, falls back to interactive prompts when run from a terminal."""
    pos, intent, tier, allow, system, sysfile = [], None, None, None, None, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--intent" and i + 1 < len(argv):
            intent = argv[i + 1]; i += 2
        elif a == "--tier" and i + 1 < len(argv):
            tier = argv[i + 1]; i += 2
        elif a == "--allow" and i + 1 < len(argv):
            allow = argv[i + 1]; i += 2
        elif a == "--system" and i + 1 < len(argv):
            system = argv[i + 1]; i += 2
        elif a == "--system-file" and i + 1 < len(argv):
            sysfile = argv[i + 1]; i += 2
        else:
            pos.append(a); i += 1

    if len(pos) < 2:
        print('usage: mindpalace add-scope <name> <channel-id> '
              '[--intent "..."] [--tier full|readonly|custom] [--allow Read,Bash]'); return
    name, chan_tok = pos[0], pos[1]
    channel_id = resolve_channel(chan_tok)
    if not channel_id:
        print(f"  bad channel '{chan_tok}' — pass the numeric channel id "
              "(Discord → right-click channel → Copy Channel ID) or a <#id> mention."); return

    # persona text: explicit file > explicit text > draft-from-intent > interactive
    if sysfile:
        try:
            system = open(sysfile).read()
        except OSError as e:
            print(f"  can't read {sysfile}: {e}"); return
    if not system:
        if not intent and __import__("sys").stdin.isatty():
            intent = _ask("What should this channel's assistant do? (one or two sentences): ")
        if intent:
            print("…drafting its persona with Claude")
            system = draft_persona(intent)
            print("\n----- proposed system.md -----\n" + system + "\n------------------------------")
            if __import__("sys").stdin.isatty() and not _ask("Use this? [Y/n]: ", "y").lower().startswith("y"):
                edited = _ask("Paste your own persona (or Enter to keep draft): ")
                if edited:
                    system = edited
        else:
            print("  need --intent or --system to give the scope a persona."); return

    # permission tier
    if not tier and __import__("sys").stdin.isatty():
        print("\nPermission tier (the fence):\n  1) readonly (safest)  2) full  3) custom")
        t = _ask("Choose [1]: ", "1")
        tier = {"1": "readonly", "2": "full", "3": "custom"}.get(t, "readonly")
    tier = (tier or "readonly").lower()
    if tier not in ("readonly", "full", "custom"):
        print("  tier must be readonly|full|custom"); return
    if tier == "custom" and not allow:
        allow = _ask("  Allowed tools (comma-sep, e.g. Read,Bash,Write): ", "Read") \
            if __import__("sys").stdin.isatty() else "Read"

    add_scope(name, channel_id, system=system, permissions=tier,
              allowed_tools=(allow if tier == "custom" else None))
    print(f"\n✓ scope '{name}' bound to channel {channel_id} ({tier}). "
          "Restart the daemon to bring it live:  mindpalace restart")


def list_cli():
    reg = registry()
    if not reg:
        print("no scopes yet — `mindpalace add-scope <name> <channel-id>` to add one.")
        return
    print("channel-scoped personas (run on the main bot):")
    for cid, s in reg.items():
        print(f"  #{cid:20} {s.get('name','?'):14} {s.get('permissions','?'):9} "
              f"{('allow=' + s['allowed_tools']) if s.get('allowed_tools') else ''}")
