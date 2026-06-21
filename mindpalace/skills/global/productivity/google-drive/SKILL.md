---
name: google-drive
description: Use when the user wants to search Google Drive, find a file or folder, list Drive contents, download or upload files, create folders, or move/copy/rename/trash files — a lightweight Google Drive connector with standalone OAuth and full read/write (no MCP server). Trigger keywords: google drive, search drive, find file, upload file, download file, create folder, move file, organize drive.
version: 1.0.0
license: Apache-2.0
tags: [google-drive, drive, files, storage, google, oauth, connector, productivity]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-drive
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Drive

Lightweight Google Drive integration with standalone OAuth. No MCP server required. Full read/write.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/drive.py`, auto-authenticating on first use.

## Read

```bash
python scripts/drive.py search "quarterly report"           # full-text
python scripts/drive.py search "title:budget"               # title only
python scripts/drive.py search "https://drive.google.com/drive/folders/1ABC..."  # by URL
python scripts/drive.py search --shared-with-me
python scripts/drive.py search "report" --limit 5 --page-token "..."
python scripts/drive.py find-folder "Project Documents"
python scripts/drive.py list                                # root
python scripts/drive.py list 1ABC123xyz --limit 20          # specific folder
python scripts/drive.py download 1ABC123xyz ./downloads/report.pdf
```

## Write

```bash
python scripts/drive.py upload ~/Documents/report.pdf
python scripts/drive.py upload ~/Documents/report.pdf --folder 1ABC123xyz
python scripts/drive.py upload ~/Documents/report.pdf --name "Q4 Report.pdf"
python scripts/drive.py create-folder "Project Documents"
python scripts/drive.py create-folder "Attachments" --parent 1ABC123xyz
python scripts/drive.py move FILE_ID DESTINATION_FOLDER_ID
python scripts/drive.py copy FILE_ID [--name "Report Copy" --folder 1ABC123xyz]
python scripts/drive.py rename FILE_ID "New Name.pdf"
python scripts/drive.py trash FILE_ID
```

## Search query formats

| Format | Example |
|--------|---------|
| Full-text | `"quarterly report"` |
| Title | `"title:budget"` |
| URL | `https://drive.google.com/...` (extracts ID) |
| Folder ID | `1ABC123...` (25+ char → lists contents) |
| Native query | `mimeType='application/pdf'` |

## Download limits

Regular files (PDF, images) download directly. Google Docs/Sheets/Slides cannot be downloaded
via this tool — use export or the dedicated google-docs/sheets/slides skills.

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-drive-skill-oauth`. Auto-refresh on expiry.
