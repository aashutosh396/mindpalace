---
name: Fixing Claude Export Conversations
description: Use when a Claude Code exported `.txt` conversation (often named YYYY-MM-DD-HHMMSS-*.txt) has broken line wrapping, mangled tables, split paths, or garbled tool output — reconstructs the formatting and validates the result.
tags: [claude-code, export, line-wrapping, tables, formatting, txt, conversation, validation]
source: daymade/claude-code-skills
derived_from: fixing-claude-export-conversations
---

# Fixing Claude Code Export Conversations

Reconstruct broken line wrapping in Claude Code exported `.txt` files. Triggers on "fix export / fix conversation / make export readable" or a `.txt` with broken tables, split paths, or mangled tool output.

## Quick start
```bash
uv run <skill-path>/scripts/fix-claude-export.py <export.txt> --stats        # fix + stats
uv run <skill-path>/scripts/fix-claude-export.py <export.txt> -o fixed.txt    # custom output
uv run <skill-path>/scripts/validate-claude-export-fix.py <export.txt> fixed.txt   # 53 checks
```
Resolve `<skill-path>`: `find ~/.claude -path "*/fixing-claude-export-conversations/scripts" -type d 2>/dev/null`.

## Workflow
1. Locate the file (pattern `YYYY-MM-DD-HHMMSS-<slug>.txt`).
2. Run fix script with `--stats` (typical: 20-25% line reduction, 80+ borders, 160+ cells fixed).
3. Run validation suite — all checks must pass; investigate any failure before delivering (`--verbose` for detail).
4. Spot-check: tables have intact single-line borders; CJK/English has pangu spacing (`Portal 都需要`); tool-result blocks (`⎿`) joined fully; diff line numbers each on own line.
5. Deliver fixed file.

## What gets fixed (state machine + next-line look-ahead, 10 content types)
User prompts (`❯`), Claude responses (`●`), Claude paragraphs (2-space indent), tables (border + cell re-padding with pipe tracking), tool calls (`● Bash(`), tool results (`⎿`), plan text (5-space indent), agent tree (`├─`/`└─` preserved), separators (`────`/`---` never joined), tree connectors (standalone `│` preserved).

## Key design
- **Next-line look-ahead** (not width thresholds): asks "does the next line look like a continuation?" via lowercase start, CJK start, opening bracket, hyphen/slash/underscore.
- **Pangu spacing**: inserts spaces between ASCII alnum and CJK at join boundaries (also `%`, `#`, `+`, `:` adjacent to CJK).
- **Mid-token detection**: joins without space for identifiers (`BASE_`+`URL`), paths (`documents`+`/05-team`), hyphenated names; `--` prefix gets a space (`run`+`--headed`).

## Safety
Never modifies original. Marker counts (`❯ ● ✻ ⎿ …`) must match input/output. Warns if any line exceeds 500 display-width (runaway join). Strict UTF-8.

## Dependencies
Python 3.10+ via `uv run`, stdlib only (`unicodedata`, `argparse`, `re`, `pathlib`, `dataclasses`).
