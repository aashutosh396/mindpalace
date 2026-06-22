---
name: Claude Code History Files Finder
description: Use when the user wants to recover deleted files, search past Claude Code sessions, track changes across sessions, or analyze conversation history — extracts and recovers content from `~/.claude/projects/` session JSONL files.
tags: [claude-code, session-history, recover-deleted, jsonl, file-recovery, conversation-history, projects]
source: daymade/claude-code-skills
derived_from: claude-code-history-files-finder
---

# Claude Code History Files Finder

Extract and recover content from Claude Code session history at `~/.claude/projects/<normalized-path>/<session-id>.jsonl`.

## Capabilities
- Recover deleted/lost files written in prior sessions
- Search code or content across conversation history
- Analyze file modifications and tool usage over time
- Find sessions by keyword/topic

## Core operations

**List sessions for a project**
`python3 scripts/analyze_sessions.py list /path/to/project` — recent sessions with timestamps/sizes. `--limit N` (default 10).

**Search sessions for keywords**
`python3 scripts/analyze_sessions.py search /path/to/project kw1 kw2` — ranks by frequency, per-keyword breakdown. `--case-sensitive` for exact.

**Recover deleted content**
`python3 scripts/recover_content.py /path/to/session.jsonl` — extracts all Write tool calls to `./recovered_content/`, preserving directory structure. Filter: `-k keyword1 keyword2`. Output dir: `-o ./my_recovery/`.

**Session statistics**
`python3 scripts/analyze_sessions.py stats /path/to/session.jsonl` — message counts, tool breakdown, file op counts. `--show-files` to list ops.

## Best practices
- Recovery auto-dedups: only the latest version of each file is saved.
- Pick distinctive keywords (file paths, function/class names, unique strings, error messages).
- Use descriptive output dirs (`./recovered_deleted_docs/`, not `./output/`).
- Verify after recovery: `find ./recovered_content/ -type f`, read `recovery_report.txt`, spot-check files.

## Limits
- CAN recover: files written via Write tool; code in markdown blocks (partial); paths from Edit/Read.
- CANNOT recover: files only discussed (never written); files deleted before session start; binary files (paths only); external tool outputs not captured.
- Only captures state at Write-call time; intermediate Edits are lost (Edits store deltas, not full content).

## Troubleshooting
- No sessions: `ls ~/.claude/projects/ | grep -i project-name` (path normalization).
- Empty recovery: files Edited but never Written, keyword mismatch, or session predates file — try `--show-edits`, broaden keywords, search adjacent sessions.
- Large files (>100MB): scripts stream line-by-line; constant memory, may take 1-2 min.

## Security
Session files may hold absolute paths with usernames, API keys, company info. Sanitize before sharing: strip absolute paths, `grep -i "api_key\|password\|token"` recovered files. Recovered content inherits original sensitivity — store securely.
