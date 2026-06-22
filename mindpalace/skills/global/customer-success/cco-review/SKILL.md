---
name: CCO Review — Retention Forcing Questions
description: Use when gross retention is slipping, before approving CSM headcount, or when deciding which customer segments to keep or fire — six retention-obsessed questions on GRR (not NRR), churn root cause, time-to-value, kill-list, coverage ratio, and CS comp.
tags: [customer-success, retention, grr, nrr, churn, segmentation, csm-coverage, time-to-value, cs-comp, cco]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cco-review
---

# CCO Forcing Questions

Retention-obsessed pressure test of any plan touching customer experience. Six questions before any retention claim, segmentation change, CS expansion, or major CS hire.

## When to run
Before any board narrative with a retention number, before approving CS headcount, before re-segmenting, before a major CS hire, or when NRR looks great but CSM churn complaints rise.

## The six questions
1. **What's the GROSS retention rate?** Not NRR — gross. GRR healthy ≥90% at growth, ≥95% at scale. If GRR <85% but NRR >100%, the product fails for 15%+ of customers and expansion is masking it.
2. **What's the #1 reason customers leave?** If you can't name it, you don't understand churn. 7-category taxonomy: product_fit / competitor_loss / no_value_realized / pricing / champion_left / company_event / tactical_failure. Preventable = product_fit + no_value_realized + tactical_failure. If preventable >50%, CS has leverage; <30%, churn is structural.
3. **Median time-to-value (TTV) by segment?** Long TTV in low tier = ICP misfit (downgrade/kill); long TTV in high tier = broken onboarding handoff. TTV leads GRR.
4. **Which customer would you fire today?** If "none," segmentation is broken. Some accounts cost more than they earn. Kill-candidate paths: non-renewal / downgrade-to-tech-touch / raise-price-to-cost-recover.
5. **ARR-per-CSM ratio, pooled or named?** Strategic: named + sponsor, $300K-$1M; Enterprise: named, $500K-$2M; Mid-market: pooled, $2M-$5M; SMB: tech-touch, $5M+.
6. **Is CS in the comp plan, and how does it differ from Sales?** Typical 70/30 base/variable; variable = 50% gross retention + 30% net + 20% activity. Anti-patterns: comp on NPS (gamed); comp same as Sales (CSMs sell instead of serve).

## Output format
```markdown
# CCO Review: <plan>
## Decision — retention | segmentation | coverage | next hire
## Retention — GRR X% (vs vanity NRR Y%); top churn driver X%; preventable X%; leaky-bucket?
## Segmentation — tier distribution; kill-list size (N, X% ARR); upgrade candidates
## Coverage — current/required-now/required-12mo CSMs; annual cost; manager trigger
## Verdict — 🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK
```
