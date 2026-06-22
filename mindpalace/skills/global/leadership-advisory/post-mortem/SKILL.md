---
name: Decision Post-Mortem
description: Use when a decision hits its 90-day review checkpoint or its kill criteria trigger — scores the decision against the success/kill criteria written BEFORE it was made and revisits preserved dissent, eliminating retroactive justification.
tags: [post-mortem, retrospective, kill-criteria, dissent, assumption-audit, calibration, decision-review]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/post-mortem
---

# Honest Retrospective

Closes the decision loop. Scores a decision against the success and kill criteria written *before* it (not retro-fitted) and revisits the preserved dissent.

## When to run
At the 90-day checkpoint, when a kill criterion triggers, after a major reversal, or quarterly across all recent decisions.

## Inputs
The decision record (with pre-committed criteria), the execution plan, and actual outcomes.

## Output: post-mortem record
```markdown
# Post-Mortem: <decision title>   Status: WIN / PARTIAL / LOSS / MIXED

## Outcome Scoring (against pre-committed criteria)
| Success Criterion | Threshold | Actual | Met? |
| Kill Criterion    | Threshold | Actual | Triggered? |

## What We Got Right / Wrong

## Preserved Dissent — Revisited
- <dissenter>: <original concern> → Did it materialize? YES/NO/PARTIAL; cost if YES; lesson.

## Assumption Audit
- <assumption> → Held? YES/NO/PARTIAL; why.

## Process Lessons — independent-thinking isolation worked? devil's-advocate concerns played out? cadence right?

## Forward Actions — [ ] change to operating system / new decision / update company-context
```

## Why pre-committed criteria matter
The biggest temptation is retroactive justification ("we always knew X"). Criteria signed at decision time eliminate that move — the numbers either matched or they didn't.

## Why revisit dissent
The dissent record is the single most useful piece of organizational memory; most of the time the dissenter was directionally right. Scoring it builds calibration over years.
