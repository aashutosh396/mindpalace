---
name: TC Tracker
description: Use when tracking technical code changes, creating change records, managing change lifecycles, or handing off in-progress work between AI sessions — structured JSON records with an enforced state machine and session-handoff format.
tags: [change-tracking, audit-trail, session-handoff, state-machine, technical-change, json-records, lifecycle, ai-continuity]
source: alirezarezvani/claude-skills
derived_from: tc-tracker
---

# TC Tracker

Track every code change as a structured JSON record (what/why/who/when/how-tested/where-it-stands) with an enforced state machine and a session-handoff format that lets a new AI session resume cleanly. Records live in `{project}/docs/TC/`, validated against a strict schema.

## Use vs not
**Use** for change audit trails, handing off in-progress work to a future session, structured release notes beyond commits, retroactive change docs on onboarding. **Don't** use for git-history changelogs (→ changelog-generator), tech-debt items (→ tech-debt-tracker), or trivial changes (typos/formatting).

## Storage layout
`docs/TC/` holds `tc_config.json`, `tc_registry.json` (index + stats), `records/TC-NNN-MM-DD-YY-slug/tc_record.json` (source of truth), and `evidence/TC-NNN/`. IDs: parent `TC-NNN-MM-DD-YY-functionality-slug`; sub-TC `TC-NNN.A` or `TC-NNN.A.1`.

## State machine
`planned → in_progress → implemented → tested → deployed`, with `blocked` (from planned/in_progress, back to planned) and rework loop back to `in_progress` from implemented/tested/deployed. Only valid transitions allowed.

## Commands (deterministic, stdlib-only, atomic writes)
- **init** — create the `docs/TC/` structure (idempotent).
- **create** — next sequential ID, populated record (status `planned`, R1 revision), registry update.
- **update** — status transition (validated), add file, append handoff progress/next-steps. Every change appends a sequential `R<n>` revision; re-validates before atomic write.
- **status** — single TC or full registry summary.
- **validate** — schema + state-machine legality + sequential `R<n>`/`T<n>` IDs + approval consistency.
- **resume / close / export / dashboard** via the `/tc` dispatcher.

## Session handoff (`session_context.handoff`)
The single most important field for AI continuity: `progress_summary`, ordered `next_steps`, `blockers`, `key_context` (decisions/gotchas/patterns), `files_in_progress` (with state: editing/needs_review/partially_done/ready), `decisions_made` (rationale + timestamp).

## Always-enforced rules
Valid transitions only · sequential append-only revision history (never edit/delete) · approval consistency (`approved=true` requires `approved_by` + `approved_date`) · TC/sub-TC ID format · atomic writes (`.tmp` then rename) · registry stats recomputed on every write.

## Non-blocking bookkeeping
Never stop coding to update records inline. Spawn a background subagent at milestones. Ask "create a TC?" once per session, not per file. Write a final handoff block at session end.

## Anti-patterns
Editing revision_history to fix a typo (add a correcting revision instead) · skipping the state machine · one TC per file (use one per logical unit) · inline updates between every edit · `approved=true` without `approved_by` · editing tc_record.json by hand · secrets in notes/evidence · recycling deleted TC IDs · letting `next_steps` go stale.
