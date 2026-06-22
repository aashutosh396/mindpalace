---
name: Tech Debt Tracker
description: Use when discussing tech debt, code quality, refactoring priority, cleanup sprints, legacy modernization, or code-health assessment — scan, score severity, prioritize, and track trends over time.
tags: [tech-debt, code-quality, refactoring, wsjf, rice, cost-of-delay, prioritization, legacy, code-health, dashboard]
source: alirezarezvani/claude-skills
derived_from: tech-debt-tracker
---

# Tech Debt Tracker

Tech debt compounds — slowing velocity, raising maintenance cost, accruing "interest." Debt is broader than messy code: architectural shortcuts, missing tests, outdated deps, doc gaps, infra compromises. This skill identifies, scores, prioritizes, and tracks it.

## Flow: scan → prioritize → dashboard
1. **Scan** the codebase → debt inventory (`summary`, `debt_items[]`, `file_statistics`, `recommendations`). Report the summary counts.
2. **Prioritize** the backlog. Frameworks: `cost_of_delay` (default), `wsjf`, `rice`. Provide team size + sprint capacity → get `prioritized_backlog` (work top-down) + `sprint_allocation` (paste into planning) + `insights`.
3. **Track trends**: keep dated snapshots (`debt_YYYY-MM-DD.json`); dashboard reports trend direction + executive summary.

## Verification loop
After a remediation sprint: re-run the scan, re-run the dashboard with the new snapshot, and assert the targeted categories' counts dropped. A cleanup that doesn't move the dashboard is rework, not debt paydown.

## Common pitfalls
1. **Analysis paralysis** — set time limits; "good enough" scoring for most items.
2. **Perfectionism** — manage debt, don't eliminate all; some debt is acceptable.
3. **Ignoring business context** — tie debt work to business outcomes / customer impact.
4. **Inconsistent application** — make debt tracking part of the standard workflow.
5. **Tool over-engineering** — start simple, iterate from actual usage.

Tech debt management is about sustainable practices balancing short-term delivery pressure with long-term system health.
