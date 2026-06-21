---
name: google-docs
description: Use when the user wants to create a Google Doc, find a document by title, read doc content, append/insert text, or replace text in a document — a lightweight Google Docs connector with standalone OAuth (no MCP server). Trigger keywords: google doc, google docs, create document, read doc, edit doc, append text, replace text.
version: 1.0.0
license: Apache-2.0
tags: [google-docs, documents, google, oauth, connector, productivity, editing, writing]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-docs
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Docs

Lightweight Google Docs integration with standalone OAuth. No MCP server required.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/docs.py`, auto-authenticating on first use.

## Commands

```bash
# Create
python scripts/docs.py create "Meeting Notes"
python scripts/docs.py create "Project Plan" --content "# Overview\n\nThis is the project plan."

# Find
python scripts/docs.py find "meeting" --limit 10

# Read
python scripts/docs.py get-text DOC_ID
python scripts/docs.py get-text "https://docs.google.com/document/d/DOC_ID/edit"

# Edit
python scripts/docs.py append-text DOC_ID "New paragraph at the end."
python scripts/docs.py insert-text DOC_ID "Text at the beginning.\n\n"
python scripts/docs.py replace-text DOC_ID "old text" "new text"
```

## Document ID format

IDs look like `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`. You can pass the full URL
(ID is extracted automatically), just the ID, or use IDs from `find` results.

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-docs-skill-oauth`. Auto-refresh on expiry.
