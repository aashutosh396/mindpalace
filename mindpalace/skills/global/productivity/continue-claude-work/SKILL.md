---
name: Continue Claude Work (session recovery)
description: Use when continuing interrupted work from a prior Claude Code session without `claude --resume` — extracts only actionable context (last compact summary, pending work, errors, workspace state) from local .claude files, then continues.
tags: [session-recovery, claude-code, compact-summary, jsonl, resume, subagent-recovery, context-extraction]
source: daymade/claude-code-skills
derived_from: continue-claude-work
---

# Continue Claude Work

Recover actionable context from a prior Claude Code session and continue in the current conversation. Use local session files as truth, then continue with concrete edits — not just summarizing.

**Why not `claude --resume`**: it replays the full transcript (wastes tokens on resolved issues/stale state). This skill **selectively reconstructs** only actionable context — fresh start with prior knowledge.

## Workflow
### Step 1 — Extract context (one script call)
```bash
python3 scripts/extract_resume_context.py            # latest session, current project
python3 scripts/extract_resume_context.py --session <ID>
python3 scripts/extract_resume_context.py --query "auth feature"
python3 scripts/extract_resume_context.py --list
```
Outputs a Markdown briefing: session metadata, **compact summary** (highest-signal — Claude's distilled understanding at last compaction boundary), last user requests, last assistant responses, errors, unresolved tool calls (= interrupted), subagent workflow state, **session end reason**, files touched, MEMORY.md, git state. Auto-skips the active session (modified <60s ago).

### Step 2 — Branch by end reason
- **Clean exit** → continue from pending work.
- **Interrupted** (tool calls dispatched, no results) → retry interrupted calls or assess if still needed.
- **Error cascade** (3+ API errors) → diagnose root cause first, don't retry blindly.
- **Abandoned** (user msg, no response) → treat last user message as current request.
Check subagent workflow section for interrupted subagents (retry or skip).

### Step 3 — Reconcile & continue
Confirm cwd matches the session's project; note/decide on branch change; inspect files for pending work — **verify old claims still hold** (don't assume). Implement next concrete step, run deterministic verification (tests/type-check/build). If blocked, state exact blocker + one next action.

### Step 4 — Report
Context recovered (which session, key findings) / work executed (files, commands, test results) / remaining tasks.

## How it works
Compact-boundary-aware (extracts last compact summary). Size-adaptive: has compactions → summary + post-compact msgs; <500KB no compaction → last 60%; 500KB-5MB → last 30%; >5MB → last 15%. Subagent extraction parses `<session-id>/subagents/*.jsonl`. End-reason detection: completed/interrupted/error_cascade/abandoned. Noise filtering skips progress/queue-operation/file-history-snapshot/api_error/system-reminder (37-53% of lines).

## Guardrails
Don't run `claude --resume`/`--continue`. Compact summaries are lossy — always verify against workspace. Don't overwrite unrelated working-tree changes. Don't load the full session file — always use the script. Can't recover deleted `.jsonl`, other machines' sessions, or full file content from Edit deltas.
