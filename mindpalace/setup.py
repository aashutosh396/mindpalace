"""
First-run onboarding (the `mindpalace` command runs this when no config exists):

  1. Verify Claude CLI (your Max subscription is the engine).
  2. Choose a gateway:
       - terminal : a Claude-CLI-style chat UI in your shell (no bot needed).
       - discord  : always-on bot; you chat from anywhere. Asks for bot token + channel.
  3. Create the agent's identity & soul (interview → USER.md / AGENT.md).
  4. Write config. Then the agent starts and you begin talking.
"""
from __future__ import annotations

import shutil
import subprocess

from . import config, identity


def _ask(prompt, default=""):
    try:
        v = input(prompt).strip()
    except EOFError:
        v = ""
    return v or default


def _check_claude() -> str | None:
    path = shutil.which("claude")
    if not path:
        print("  ⚠ Claude CLI not found. Install it + log in to your Max plan:")
        print("    https://docs.claude.com/claude-code  →  then run `claude` once to log in.")
        return None
    print(f"  ✓ Claude CLI: {path}")
    return path


def _claude_auth():
    """Use existing `claude` login by default; allow pasting an OAuth token to override."""
    print("\nClaude auth — mindpalace runs on your Claude Max subscription.")
    print("  If you've already run `claude` and logged in, just press Enter.")
    tok = _ask("  Paste a CLAUDE_CODE_OAUTH_TOKEN to override (or Enter to use existing login): ")
    if tok:
        config.write_secret("claude_token", tok)
        print("  ✓ token stored")
    else:
        print("  ✓ using ambient Claude CLI login")


def _gateway() -> dict:
    print("\nHow do you want to talk to your agent?")
    print("  1) terminal  — chat right here in your shell (Claude-CLI style)")
    print("  2) discord   — always-on bot; chat from your phone/anywhere")
    choice = _ask("Choose [1]: ", "1")
    if choice.startswith("2") or choice.lower().startswith("d"):
        return _discord_gateway()
    return {"gateway": "terminal"}


def _discord_gateway() -> dict:
    print("\nDiscord setup — create a bot at https://discord.com/developers (enable MESSAGE CONTENT INTENT).")
    print("This is your MAIN bot. Its HOME CHANNEL is where you chat with it AND where all")
    print("its updates (cron results, task completions, alerts) get posted.")
    token = _ask("  Main bot token: ")
    if token:
        config.write_secret("bot_main.token", token)        # registry naming
    home = _ask("  Home channel ID (chat + updates hub): ")
    hook = _ask("  Home channel webhook URL for background/cron updates (optional, Enter to skip): ")
    verify_discord(token, home)
    print("  (the first person to message in the home channel becomes the first admin)")
    cfg = {
        "gateway": "discord",
        "discord": {
            "home_channel": int(home) if home.isdigit() else home,
            "admins": [],                       # auto-bootstrapped from first home message
        },
        # main bot uses the agent's own AGENT.md as its system prompt; full power.
        "bots": {"main": {"permissions": "full", "trigger": "home"}},
    }
    if hook:
        cfg["webhooks"] = {"home": hook}
    return cfg


def verify_discord(token: str, channel: str) -> None:
    """Best-effort token sanity check via the Discord REST API (no extra deps)."""
    if not token:
        return
    try:
        import http.client, json
        c = http.client.HTTPSConnection("discord.com", timeout=10)
        c.request("GET", "/api/v10/users/@me",
                  headers={"Authorization": f"Bot {token}",
                           "User-Agent": "DiscordBot (https://github.com/aashutosh396/mindpalace, 0.1)"})
        r = c.getresponse(); body = r.read(); c.close()
        if r.status == 200:
            who = json.loads(body).get("username", "?")
            print(f"  ✓ bot token valid — connected as {who}")
        else:
            print(f"  ⚠ token check returned {r.status} — double-check the token")
    except Exception as e:
        print(f"  ⚠ couldn't verify token now ({str(e)[:60]}) — will try at runtime")


def run() -> dict:
    print("\n=== mindpalace setup ===")
    config.ensure_dirs()
    has_claude = _check_claude()
    cfg = _gateway()
    if has_claude:
        _claude_auth()
    print()
    answers = identity.create(use_claude=bool(has_claude))
    cfg["agent_name"] = answers.get("agent_name") or "mindpalace"
    cfg["initialized"] = True
    config.save_config(cfg)
    print(f"\n✓ mindpalace ready. Data: {config.home()}")
    print("  Run `mindpalace` again any time to start talking.\n")
    return cfg
