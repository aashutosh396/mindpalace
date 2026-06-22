---
name: One-Page Strategy Brief
description: Use when a strategic question needs framing before group deliberation — turns raw intake (or office-hours output) into a one-page brief locking the question, 2-3 options, assumptions, constraints, affected roles, and pre-committed success/kill criteria.
tags: [strategy-brief, framing, options, assumptions, constraints, success-criteria, kill-criteria, decision-prep]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/brief
---

# One-Page Strategy Brief

Turns intake into a one-page brief a board can deliberate on. The biggest decision-making failure is debating implementation before agreeing on the question — the brief locks the question, options, and success criteria so deliberation runs without scope creep. It's also the artifact handoff: the next step consumes this file, not your memory.

## Inputs
A topic string, or (preferred) an office-hours brief, plus loaded company context.

## Output structure
```markdown
# Strategy Brief: <topic>   Status: DRAFT | UNDER REVIEW | APPROVED | RETIRED

## Context — 1-2 paragraphs: where the company sits on this today (from company context)
## Question — the one sentence the board must answer
## Options — min 2; "do nothing" is always an option
  1. Option A — one-line summary
  2. Option B — one-line summary
## Assumptions — explicit, listed
## Constraints — Time (deadline) / Money (envelope) / People (who can move) / Reversibility (one-way vs two-way door)
## Affected Roles — which advisors weigh in (drives boardroom panel composition)
## Success Criteria — measurable, set BEFORE the decision (metric, threshold, timeframe)
## Kill Criteria — what in 90 days says this was wrong (metric, threshold, action)
```

## Workflow
1. Load company context.
2. Parse office-hours answers, or prompt for missing pieces.
3. Draft 2-3 options — never one; every brief needs a counterfactual.
4. Make assumptions and constraints explicit.
5. Identify affected roles → panel composition.
6. Write success + kill criteria before the decision (the rigor moment).
7. Save the brief.
