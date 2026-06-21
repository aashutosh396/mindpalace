---
name: google-sheets
description: Use when the user wants to read a spreadsheet, update cells, append rows, fetch a specific range, find a spreadsheet, or view sheet metadata — a lightweight Google Sheets connector with standalone OAuth and full read/write (no MCP server). Trigger keywords: google sheets, spreadsheet, update cells, append rows, cell values, A1 range, export spreadsheet.
version: 1.0.0
license: Apache-2.0
tags: [google-sheets, spreadsheet, data, google, oauth, connector, productivity, csv]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-sheets
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Sheets

Lightweight Google Sheets integration with standalone OAuth. No MCP server required. Full read/write.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/sheets.py`, auto-authenticating on first use.

## Read

```bash
python scripts/sheets.py get-text SPREADSHEET_ID                 # plain text (default)
python scripts/sheets.py get-text SPREADSHEET_ID --format csv
python scripts/sheets.py get-text SPREADSHEET_ID --format json
python scripts/sheets.py get-range SPREADSHEET_ID "Sheet1!A1:D10"
python scripts/sheets.py get-range SPREADSHEET_ID "A1:C5"
python scripts/sheets.py find "budget 2024" [--limit 5]
python scripts/sheets.py get-metadata SPREADSHEET_ID
```

## Write

```bash
python scripts/sheets.py update-range SPREADSHEET_ID "Sheet1!A1:B2" '[["Hello","World"],["Foo","Bar"]]'
python scripts/sheets.py update-range SPREADSHEET_ID "Sheet1!A1:B1" '[["=SUM(A1:A5)","text"]]' --raw
python scripts/sheets.py append-rows SPREADSHEET_ID "Sheet1!A:Z" '[["New A","New B"]]'
python scripts/sheets.py clear-range SPREADSHEET_ID "Sheet1!A1:B10"
python scripts/sheets.py batch-update SPREADSHEET_ID '[{"updateCells":{"range":{"sheetId":0},"fields":"userEnteredValue"}}]'
```

## Spreadsheet ID

Pass the ID (`1BxiMVs0XRA5...`) or the full URL (`https://docs.google.com/spreadsheets/d/<ID>/edit`);
the ID is extracted automatically.

## A1 notation

`Sheet1!A1:B10` (range), `Sheet1!A:A` (column), `Sheet1!1:1` (row), `A1:C5` (first sheet).

## Value input

USER_ENTERED (default): values parsed as if typed (numbers, dates, formulas interpreted).
RAW (`--raw`): values stored exactly as provided, no parsing.

## Output formats

`text` (pipe-separated, human-readable), `csv` (standard), `json` (`{sheet: [[rows]]}`).

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-sheets-skill-oauth`. Auto-refresh on expiry.
