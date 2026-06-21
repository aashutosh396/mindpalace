---
name: google-slides
description: Use when the user wants to read a presentation's text, find presentations, create a presentation, add or delete slides, or replace text across slides — a lightweight Google Slides connector with standalone OAuth and full read/write (no MCP server). Trigger keywords: google slides, presentation, create slides, add slide, replace text in deck, slide deck.
version: 1.0.0
license: Apache-2.0
tags: [google-slides, slides, presentations, google, oauth, connector, productivity, documents]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-slides
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Slides

Lightweight Google Slides integration with standalone OAuth. No MCP server required. Full read/write.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/slides.py`, auto-authenticating on first use.

## Read

```bash
python scripts/slides.py get-text "1abc123xyz789"
python scripts/slides.py get-text "https://docs.google.com/presentation/d/1abc123xyz789/edit"
python scripts/slides.py find "quarterly report" [--limit 5]
python scripts/slides.py get-metadata "1abc123xyz789"   # title, slide count, slide object IDs
```

## Write

```bash
python scripts/slides.py create "Q4 Sales Report"
python scripts/slides.py add-slide "1abc123xyz789"
python scripts/slides.py add-slide "1abc123xyz789" --layout TITLE_AND_BODY
python scripts/slides.py add-slide "1abc123xyz789" --layout TITLE --at 0     # 0-based index
python scripts/slides.py replace-text "1abc123xyz789" "old text" "new text" [--match-case]
python scripts/slides.py delete-slide "1abc123xyz789" "g123abc456"           # object ID from get-metadata
python scripts/slides.py batch-update "1abc123xyz789" '[{"replaceAllText":{"containsText":{"text":"foo"},"replaceText":"bar"}}]'
```

## Slide layouts

`BLANK` (default), `TITLE`, `TITLE_AND_BODY`, `TITLE_AND_TWO_COLUMNS`, `TITLE_ONLY`,
`SECTION_HEADER`, `ONE_COLUMN_TEXT`, `MAIN_POINT`, `BIG_NUMBER`.

## Presentation ID

Pass the ID (`1abc123xyz789`) or full URL; the ID is extracted automatically.

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-slides-skill-oauth`. Auto-refresh on expiry.
