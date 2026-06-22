---
name: CRO Review — Revenue Forcing Questions
description: Use when the forecast misses pipeline coverage, win rates drop, or before scaling the sales team — pipeline-paranoid interrogation of coverage, win rate, NRR decomposition, ramp time, discount discipline, and source mix.
tags: [revenue, sales, pipeline-coverage, win-rate, nrr, ramp-time, discount, forecast, cro]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cro-review
---

# CRO Forcing Questions

Pipeline-paranoid pressure test of revenue assumptions. Six questions that surface next-quarter pain this quarter.

## When to run
- Before committing a quarterly revenue target; before changing sales motion (PLG↔sales-led, mid-market↔enterprise).
- Before hiring a batch of reps; when coverage drops below 3x; when NRR trends down.

## The six questions
1. **Pipeline Coverage** — by stage. Inbound-heavy target 3x, outbound-heavy 4x. Stage-weighted, not just total. Below threshold = act now.
2. **Win Rate Trajectory** — this quarter vs last 4, stage-by-stage. If one stage softens, find why before forecasting.
3. **NRR Decomposition** — gross retention, contraction, expansion *separately*. 110% NRR with 95% gross is very different from 110% with 80%.
4. **Ramp Time** — for the last 4 hires, days to first deal and to quota. If ramp >90 days at growth stage, hiring profile or enablement is broken. Forecast hires must build in ramp.
5. **Discount Discipline** — median discount this quarter vs last 4; where is it creeping? Discount creep is the leading indicator of pricing/positioning weakness. Cap by approver tier.
6. **Pipeline Source Mix** — % marketing- / sales- / partner-sourced. If one source >80%, you have concentration risk.

## Output format
```markdown
# CRO Review: <plan>
## Pipeline — coverage X.Xx (target 3x+); win rate X% (4Q trend); top leaking stage
## Retention — gross X%; NRR X%; expansion X%; contraction X%
## Ramp — new hires N; median days to first deal / to quota
## Discount — median X%; trend vs 4Q ago
## Source Mix — Marketing X% | Sales X% | Partner X%
## Verdict — 🟢 ON PLAN | 🟡 GAP | 🔴 PIPELINE CRISIS
## Next Steps — 3 concrete actions
```
