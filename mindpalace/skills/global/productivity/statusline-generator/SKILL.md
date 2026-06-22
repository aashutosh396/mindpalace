---
name: Claude Code Statusline Generator
description: Use when installing, customizing, or fixing the Claude Code statusline (cwd, model, token counts) — minimal vs full layouts, absolute token counts, cost via ccusage, and fixing a blank/stuck statusline (usually missing chmod +x).
tags: [statusline, claude-code, settings-json, token-count, ccusage, chmod, health-check, customization]
source: daymade/claude-code-skills
derived_from: statusline-generator
---

# Statusline Generator

Single-source-of-truth statusline for Claude Code. One script, two layouts, end-to-end self-verification.

## Health check (start here when broken)
```bash
bash scripts/health_check.sh
```
Validates 4 layers: (1) `~/.claude/statusline.sh` exists + is executable — **missing `chmod +x` is the #1 silent-failure cause** (Claude Code's `exec` fails → blank, no error); (2) `settings.json` `statusLine` block points at the script; (3) mock stdin tests (complete data, zero tokens, missing fields, `$HOME` shortening); (4) real stdin replay from `/tmp/.claude-statusline-last-stdin.json` if debug was on. Each failure prints a one-line fix.

## Install
```bash
bash scripts/install_statusline.sh
```
Backs up existing files, copies `generate_statusline.sh` → `~/.claude/statusline.sh` + `chmod +x`, wires `settings.json` via `jq` (preserves other settings), **mandatorily runs health_check.sh** (install isn't "complete" until it passes). Restart Claude Code / send a message to refresh.

## Layouts (set via env, not flags — stdin carries JSON)
```bash
export CLAUDE_STATUSLINE_LAYOUT=minimal   # default: ~/path  Model  ctx: 108K / 1M
export CLAUDE_STATUSLINE_LAYOUT=full      # user(model)[$cost] color-coded ctx / path / git branch
```
Full: line1 = user, model, ccusage session/daily cost, color ctx (green ≤50%, yellow 51-80%, red >80%); line2 = short path; line3 = `[git:main*+]`. Set in `~/.zshrc`/`~/.bashrc`, source, send a message (refresh <300ms).

## Debug stdin
`export CLAUDE_STATUSLINE_DEBUG=1` → each invocation writes stdin to `/tmp/.claude-statusline-last-stdin.json`. Re-run against real input: `cat that.json | ~/.claude/statusline.sh`.

## Authoring rules (sealed in code)
1. **Always `chmod +x`, verify by running** — hand-written script: `echo '{}' | bash your-script.sh` before declaring done.
2. **"Configuration complete" is meaningless without evidence** — installer always runs health_check.sh and exits non-zero on failure. Treat any agent's "complete!" without evidence as suspect.

## Dependencies (graceful degrade)
`jq` (preferred, falls back to python3), `python3` (fallback, else bare cwd), `awk` (required for K/M formatting), `git` (full layout, silent skip), `ccusage` (cost, silent skip).

## Troubleshooting symptoms
Blank/never updates (chmod); ctx missing/wrong (field traps: `used_percentage` null at session start, `total_input_tokens` semantics across versions); want counts not percentages (layout switch); colors as raw escape codes (terminal compat); edits no effect (path mismatch); slow refresh (jq vs python3).
