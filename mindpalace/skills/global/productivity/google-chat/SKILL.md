---
name: google-chat
description: Use when the user wants to send or read Google Chat messages, list chat spaces, find a chat room, send a DM, or create a new chat space — a lightweight Google Chat connector with standalone OAuth (no MCP server). Trigger keywords: google chat, chat message, chat space, send DM, chat room, gchat.
version: 1.0.0
license: Apache-2.0
tags: [google-chat, chat, messaging, google, oauth, connector, productivity, collaboration]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-chat
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Chat

Lightweight Google Chat integration with standalone OAuth. No MCP server required.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/chat.py`, auto-authenticating on first use.

## Commands

```bash
# Spaces
python scripts/chat.py list-spaces
python scripts/chat.py find-space "Project Alpha"
python scripts/chat.py setup-space "New Project" user1@example.com user2@example.com

# Messages
python scripts/chat.py get-messages spaces/AAAA123 --limit 10
python scripts/chat.py send-message spaces/AAAA123 "Hello team!"
python scripts/chat.py send-message spaces/AAAA123 "Here's the report" --attachment /path/file.pdf
python scripts/chat.py list-threads spaces/AAAA123

# Direct messages
python scripts/chat.py send-dm user@example.com "Hey, quick question..."
python scripts/chat.py send-dm user@example.com "Please review" --attachment /path/file.pdf
python scripts/chat.py find-dm user@example.com   # find or create DM space
```

## Space name format

Google Chat uses `spaces/AAAA123`. Get names from `list-spaces` or `find-space`.

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-chat-skill-oauth`. Auto-refresh on expiry.
