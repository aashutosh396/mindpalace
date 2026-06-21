---
name: gmail
description: Use when the user wants to search email, read a message, send an email, create a draft, mark read/unread, archive, star, or manage Gmail labels — a lightweight Gmail connector with standalone OAuth (no MCP server). Trigger keywords: gmail, search email, send email, email draft, archive email, star email, Gmail labels.
version: 1.0.0
license: Apache-2.0
tags: [gmail, email, google, oauth, connector, saas, productivity, inbox]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/gmail
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Gmail

Lightweight Gmail integration with standalone OAuth. No MCP server required.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login    # opens browser to authenticate
python scripts/auth.py status   # check auth status
python scripts/auth.py logout
```

All operations run via `scripts/gmail.py` and auto-authenticate on first use.

## Search

```bash
python scripts/gmail.py search "from:someone@example.com is:unread"
python scripts/gmail.py search --limit 20
python scripts/gmail.py search --label INBOX --limit 10
python scripts/gmail.py search "subject:important" --include-spam-trash
```

## Read

```bash
python scripts/gmail.py get MESSAGE_ID                    # full content
python scripts/gmail.py get MESSAGE_ID --format metadata  # headers only
python scripts/gmail.py get MESSAGE_ID --format minimal   # IDs only
```

## Send

```bash
python scripts/gmail.py send --to "user@example.com" --subject "Hello" --body "Body"
python scripts/gmail.py send --to a@x.com --cc cc@x.com --bcc bcc@x.com --subject S --body B
python scripts/gmail.py send --to a@x.com --subject S --body B --from "Name <alias@x.io>"  # alias must be configured
python scripts/gmail.py send --to a@x.com --subject S --body "<h1>Hi</h1>" --html
```

## Drafts

```bash
python scripts/gmail.py create-draft --to a@x.com --subject S --body B
python scripts/gmail.py send-draft DRAFT_ID
```

## Modify labels

```bash
python scripts/gmail.py modify MESSAGE_ID --remove-label UNREAD   # mark read
python scripts/gmail.py modify MESSAGE_ID --add-label UNREAD      # mark unread
python scripts/gmail.py modify MESSAGE_ID --remove-label INBOX    # archive
python scripts/gmail.py modify MESSAGE_ID --add-label STARRED     # star
python scripts/gmail.py modify MESSAGE_ID --add-label IMPORTANT
python scripts/gmail.py modify MESSAGE_ID --remove-label UNREAD --add-label STARRED
python scripts/gmail.py list-labels
```

## Query syntax

`from:` `to:` `subject:` `is:unread` `is:starred` `is:important` `has:attachment`
`after:2024/01/01` `before:2024/12/31` `newer_than:7d` `older_than:1m` `label:work`
`in:inbox` `in:sent` `in:trash`. Combine with space (AND), `OR`, `-` (NOT).

System label IDs: `INBOX`, `SENT`, `DRAFT`, `SPAM`, `TRASH`, `STARRED`, `IMPORTANT`, `UNREAD`.

## Tokens

Stored in the system keyring (macOS Keychain / Windows Credential Locker / Linux Secret Service).
Service name `gmail-skill-oauth`. Tokens auto-refresh when expired.
