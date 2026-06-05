"""
Bot registry — one main bot + optional scoped bots, all in USER-DATA.

Each bot = a triple that travels with the instance:
  • token        secrets/bot_<name>.token
  • system.md    bots/<name>/system.md   (its scope/persona — used as the system prompt)
  • policy       config["bots"][name]     (permissions tier + trigger)

Security per bot = owner-lock (gateway) + tool fence (brain `--allowedTools`), declared
here and enforced every time the bot speaks. Adding a bot writes all three; that's its
"block." `permissions`: full | readonly | custom(+allowed_tools).
"""
from __future__ import annotations

from . import config
from .core import brain

DRAFT_INSTRUCTION = (
    "You are writing a SYSTEM PROMPT for a scoped Discord assistant bot. "
    "The owner wants a bot that does ONLY this:\n\n  {intent}\n\n"
    "Write 100–500 words, second person ('You are ...'). It must: name the bot's single "
    "purpose; state precisely what it will do; explicitly REFUSE anything outside that scope; "
    "set a concise, helpful tone. Do not include code fences or preamble — output ONLY the "
    "system prompt text."
)


def registry() -> dict:
    return config.load_config().get("bots", {})


def get(name: str) -> dict | None:
    return registry().get(name)


def system_path(name: str):
    return config.home() / "bots" / name / "system.md"


def load_system(name: str) -> str | None:
    p = system_path(name)
    return p.read_text() if p.exists() else None


def token(name: str) -> str | None:
    return config.read_secret(f"bot_{name}.token")


def _ask(prompt, default=""):
    try:
        v = input(prompt).strip()
    except EOFError:
        v = ""
    return v or default


def add_bot_interactive():
    """`mindpalace add-bot` — describe it in plain language; Claude drafts the scope."""
    print("\n=== add a bot ===")
    name = _ask("Short name (e.g. deploy, reports, saauzi): ").strip().replace(" ", "-")
    if not name:
        print("  cancelled."); return
    intent = _ask("What should this bot do? (one or two sentences): ")
    if not intent:
        print("  cancelled."); return

    print("\n…drafting its scoped system prompt with Claude")
    draft = brain.ask_sync(DRAFT_INSTRUCTION.format(intent=intent), [])
    print("\n----- proposed system.md -----\n")
    print(draft)
    print("\n------------------------------")
    if not _ask("Use this? [Y/n]: ", "y").lower().startswith("y"):
        edited = _ask("Paste your own system prompt (or Enter to keep draft): ")
        if edited:
            draft = edited

    print("\nPermission tier (the real fence):")
    print("  1) readonly — can read/search, CANNOT run commands or write files (safest)")
    print("  2) full     — full bash/file power (trust the scope prompt)")
    print("  3) custom   — you name the allowed tools")
    tier = _ask("Choose [1]: ", "1")
    permissions, allowed = "readonly", None
    if tier.startswith("2"):
        permissions = "full"
    elif tier.startswith("3"):
        permissions = "custom"
        allowed = _ask("  Allowed tools (comma-sep, e.g. Read,Bash,Write): ", "Read")

    tok = _ask("\nBot token (from discord.com/developers — enable Message Content intent): ")
    if not tok:
        print("  no token — cancelled."); return

    # persist all three
    config.ensure_dirs()
    system_path(name).parent.mkdir(parents=True, exist_ok=True)
    system_path(name).write_text(draft.strip() + "\n")
    config.write_secret(f"bot_{name}.token", tok)
    cfg = config.load_config()
    cfg.setdefault("bots", {})[name] = {
        "permissions": permissions,
        "allowed_tools": allowed,
        "trigger": "mention",   # scoped bots answer when @mentioned, any channel
        "created": __import__("time").strftime("%Y-%m-%d"),
    }
    config.save_config(cfg)
    print(f"\n✓ bot '{name}' added ({permissions}). @mention it in any channel it's in.")
    print("  Restart the gateway (`mindpalace`) to bring it online.\n")
