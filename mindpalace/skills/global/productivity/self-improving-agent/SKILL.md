---
name: Self-Improving Agent — Memory Curation
description: Use when reviewing what Claude has learned about a project, promoting a recurring pattern from auto-memory to enforced rules, extracting a solution into a reusable skill, or checking memory health.
tags: [memory, auto-memory, claude-md, rules, promotion, knowledge-curation, skill-extraction, memory-health, project-knowledge]
source: alirezarezvani/claude-skills
derived_from: engineering-team/self-improving-agent (+ promote/review/extract/remember/status)
---

# Self-Improving Agent — Memory Curation

Auto-memory captures; this skill curates. Claude Code's auto-memory (`~/.claude/projects/<path>/memory/MEMORY.md`, first 200 lines load each session) records patterns automatically but has no judgment about what's permanent, what should become a rule, or what's stale. Add that judgment.

## Memory stack
- `./CLAUDE.md` — you write — project rules — full load every session.
- `~/.claude/CLAUDE.md` — you write — global preferences — full load.
- `MEMORY.md` — Claude auto-writes — learnings — first 200 lines.
- `memory/*.md` — Claude overflow — topic notes — on demand.
- `.claude/rules/*.md` — you write — scoped rules — load when matching files open.

Locate memory: `MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"`.

## REVIEW — analyze auto-memory
Read MEMORY.md fully; count vs the 200-line limit. Per entry flag: **recurrence** (same concept repeated, "again"/"still"), **staleness** (references deleted files — verify with `find`; outdated tools; contradicts CLAUDE.md), **consolidation** (multiple entries on one topic → merge), **promotion candidates** (appeared 2+ sessions, broadly useful, actionable, not already a rule). Read topic files + cross-reference CLAUDE.md and `.claude/rules/` for duplicates/conflicts/gaps. Output: health (lines/200, topic files, CLAUDE.md size, rules count), promotion candidates, stale entries, consolidation groups, conflicts, recommendations.

## PROMOTE — graduate a pattern to a rule
1. Parse the pattern; ask one clarifying question if vague.
2. Find it in MEMORY.md (`grep -ni`).
3. Pick target by scope: entire project → `./CLAUDE.md`; specific file types → `.claude/rules/<topic>.md` (with `paths:` frontmatter); all projects → `~/.claude/CLAUDE.md`.
4. Distill descriptive → prescriptive: one line, imperative voice (Use X / Always Y / Never Z), include the command/example, no backstory.
5. Write under the right heading (if CLAUDE.md would exceed 200 lines, use rules/ instead).
6. Remove the original MEMORY.md entry (confirm first) to free space.

Promote when: pattern appeared 3+ times, you corrected Claude on it more than once, it's a convention any contributor needs, or it prevents a recurring mistake. Don't promote: one-time debugging notes, session-specific context, things mid-migration, or already-covered rules.

## EXTRACT — pattern → standalone skill
Qualifies when: recurring across 2+ projects, non-obvious (needed real debugging), broadly applicable, complex multi-step, or user-flagged. Steps: find source in memory → ask ≤2 scoping questions → generate kebab-case name (2-4 words; **never** contains `claude`/`anthropic` — use `cc-` prefix for Claude Code skills) → create `<name>/SKILL.md` (+ README, optional reference/examples.md). Quality gates: valid frontmatter with name+description, name matches folder, "Use when:" trigger, self-contained solutions, copy-pasteable examples, no hardcoded paths/URLs/credentials.

## REMEMBER — explicit save
For knowledge too important to rely on auto-capture (hard-won debugging insight, convention not in CLAUDE.md, tool gotcha, architecture decision, preference). Parse what/why/scope → check duplicates → append one concise line to MEMORY.md (no timestamps/IDs needed) → warn if >180 lines → if it sounds like a rule (imperative, always/never), suggest PROMOTE instead. Never store credentials/tokens/secrets in memory.

## STATUS — health dashboard
Count MEMORY.md lines, topic files, CLAUDE.md (project + global) lines, rules count. Capacity bands: MEMORY.md <120 healthy / 120-180 warning / >180 critical. Quick stale check: grep file-path references and verify each still exists. Green <60% (working well), Yellow 60-90% (run REVIEW), Red >90% (run REVIEW now — auto-memory may drop older entries).

## Principle
Don't fight auto-memory — orchestrate it. Promoted rules outrank MEMORY.md entries; removing promoted entries frees capacity for new learnings.
