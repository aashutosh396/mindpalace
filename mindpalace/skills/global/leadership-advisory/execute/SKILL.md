---
name: 90-Day Execution Plan
description: Use when a logged decision needs to become an operating plan — turns an approved decision into a 90-day plan with workstreams, named DRIs, 12 weekly milestones, a check-in cadence, dependencies, a risk register, and a kill-criteria watch.
tags: [execution, 90-day-plan, dri, milestones, cadence, risk-register, workstreams, operating-plan]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/execute
---

# 90-Day Execution Plan

Turns an approved decision into a 90-day plan with weekly milestones, named DRIs, and a check-in cadence. This is where most decisions die: between "we decided" and "what's next Monday?"

## Output plan format
```markdown
# Execution Plan: <decision title>
**Owner (Sponsor):** <exec>  **Start:** YYYY-MM-DD  **Checkpoint:** +90d

## Outcome (binding) — success + kill criteria copied from the decision
## Workstreams — | workstream | DRI | success metric | status |
## Weekly Milestones — | week 1..12 | milestone | DRI | definition of done |
## Cadence — weekly owner review (15m); bi-weekly cross-functional sync (30m); day 30/60/90 checkpoints
## Dependencies — internal / external (vendors, regulators, customers)
## Risk Register — | risk | likelihood | impact | owner | mitigation |  (cross-ref devil's-advocate concerns)
## Kill Criteria Watch — reviewed at every checkpoint
```

## Workflow
1. Read the decision record.
2. Decompose the chosen option into 3-6 workstreams.
3. Name a DRI per workstream.
4. Reverse-engineer 12 weekly milestones from the checkpoint date.
5. Set cadence (weekly + bi-weekly + 30/60/90).
6. Build the risk register from the original devil's-advocate concerns.
7. Save and notify DRIs.

## Why 90 days
Long enough to show real signal (not just activity), short enough to course-correct before damage compounds, and aligned with quarterly OKR / board cadences. At day 90 (or earlier if kill criteria trigger) → run a post-mortem.
