---
name: Repomix Unmixer
description: Use when extracting files from a repomix-packed repository (XML/Markdown/JSON) to restore the original directory structure — reverses the repomix packing process.
tags: [repomix, unpack, extract, restore-files, xml, markdown, json, code-bundle]
source: daymade/claude-code-skills
derived_from: repomix-unmixer
---

# Repomix Unmixer

Extract files from a repomix-packed file and restore the original directory tree.

## Workflow
```bash
python3 scripts/unmix_repomix.py "<repomix_file>" "<output_dir>"
```
Parses the format, extracts each file path + content, recreates dirs, writes files, reports count.

## Supported formats
- **XML** (default): `<file path="...">content</file>` blocks (regex matched).
- **Markdown**: `## File: path` followed by fenced code block.
- **JSON**: `{"files":[{"path":...,"content":...}]}`.

## Principles
- **Always specify an output dir** — never dump into cwd.
- **Extract to `/tmp` first for review**, then `tree` it, spot-check content, then move to final dest.
- **Never extract directly over important dirs** — verify before overwriting (use a fresh dir or `output-$(date +%s)`).
- For skills: validate after unmixing with skill-creator tools.

## Troubleshooting
- No files extracted → wrong/unsupported format; inspect file manually.
- Permission error → `mkdir -p` + writable dir, or use `$HOME/extracted`.
- Garbled chars → script is UTF-8; check source encoding.
- Path exists → fresh output dir or clear it first.
