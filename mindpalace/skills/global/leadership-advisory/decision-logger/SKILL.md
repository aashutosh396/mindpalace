---
name: Decision Logger (Two-Layer Memory)
description: Use when logging decisions after a deliberation, reviewing past decisions, or checking overdue action items — a two-layer memory that stores everything but only feeds approved decisions back into future meetings.
tags: [decision-log, memory, approved-decisions, action-items, board-minutes, conflict-detection, do-not-resurface]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/skills/decision-logger
---

# Decision Logger

Two-layer memory. Layer 1 stores everything; Layer 2 stores only what was approved. Future meetings read Layer 2 only — this prevents hallucinated consensus from past debates bleeding into new deliberations.

## Two-layer architecture

**Layer 1 — raw transcripts** (`decisions/raw/YYYY-MM-DD-<slug>.md`): full contributions, critique, synthesis, all rejected arguments. NEVER auto-loaded; only on explicit request. Archive after 90 days.

**Layer 2 — approved decisions** (`decisions/approved/` one record per decision + append-only index `decisions.md`): only approved decisions, action items, user corrections. Loaded automatically at the start of every deliberation. Append-only — decisions are never deleted, only superseded.

## Decision entry format

```markdown
## [YYYY-MM-DD] — [TITLE]
**Decision:** [one clear statement]
**Owner:** [one person/role]   **Deadline:** [date]   **Review:** [date]
**Rationale:** [why this over alternatives, 1–2 sentences]
**User Override:** [if founder changed the recommendation — what + why]
**Rejected:** [proposal] — [reason] [DO_NOT_RESURFACE]
**Action Items:** - [ ] [action] — Owner — Due — Review
**Supersedes / Superseded by:** [date]
**Raw transcript:** decisions/raw/[date]-<slug>.md
```

## Conflict detection (before logging)

1. **DO_NOT_RESURFACE violation** — new decision matches a rejected proposal → block: "was rejected on [date], reason [X]; to reopen, founder must explicitly say 'reopen [topic] from [date]'."
2. **Topic contradiction** — two active decisions on same topic, different conclusions → offer: supersede / merge / defer to founder.
3. **Owner conflict** — same action assigned to different people.

## Logging workflow

Founder approves → write raw transcript → check conflicts against approved index → surface conflicts, wait for resolution → write approved record + append to index → confirm logged.

## Marking complete

`- [x] [action] — Owner — Completed: [date] — Result: [one sentence]`. Never delete completed items; the history is the record.
