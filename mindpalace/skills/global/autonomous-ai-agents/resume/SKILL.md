---
name: Autoresearch Resume (/ar:resume)
description: Use when picking up a previously started autoresearch experiment after a pause or context limit — checks out the branch, loads full results history, reports state, and continues.
tags: [autoresearch, resume, experiment, continue, results-history, ar-resume]
source: alirezarezvani/claude-skills
derived_from: engineering/autoresearch-agent/skills/resume
---

# /ar:resume — Resume Experiment

Resume a paused or context-limited experiment. Reads all history and continues where you left off.

## Steps
1. **List experiments** (if none specified) — show status per experiment (active/paused/done by results.tsv age); let user pick.
2. **Load full context** — checkout `autoresearch/{domain}/{name}`; read config.cfg, program.md (strategy), results.tsv (full history), `git log --oneline -20`.
3. **Report current state** — target, metric + direction, total/kept/discarded/crashed counts, best metric (+Δ from baseline), last experiment result, and recent patterns (e.g., "caching changes: 3 kept, 1 discarded — consistently helpful").
4. **Ask next action:**
   - Single iteration (`/ar:run`) — one change + evaluate
   - Start a loop (`/ar:loop`) — autonomous scheduled
   - Show results only — review and decide
   Hand off to `/ar:loop` (pre-selected) or `/ar:run` per choice.
