---
name: VPE Review — Engineering Throughput Forcing Questions
description: Use when cycle time balloons, DORA metrics slide, or before committing to an eng hiring wave or a reorg — throughput-first interrogation of delivery, hiring funnel, team structure, and production discipline.
tags: [engineering-management, dora, cycle-time, throughput, hiring-funnel, team-topology, slo, reorg, vpe]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/vpe-review
---

# VPE Forcing Questions

Throughput-first pressure test of any plan touching eng operations. Six questions before any delivery commitment, hiring expansion, restructure, or production-discipline change.

## When to run
- Before quarterly delivery commitment, approving an eng hiring plan, or restructuring squads.
- When production incidents rise, or velocity drops while everyone "works hard."
- When deciding whether to hire a VPE separate from CTO.

## The six questions
1. **What's the cycle time, and where does work wait?** No DORA, no diagnosis. Lead Time for Changes is the single best health metric. Decompose cycle time into stages to find the bottleneck.
2. **What's the DORA level on all 4 metrics?** Deployment Frequency, Lead Time, MTTR, Change Failure Rate. The worst metric defines the overall level. Fix lead time first.
3. **Where is the hiring funnel leaking?** "Can't find good engineers" is wrong — a specific stage over-filters, top-of-funnel volume is low, or offer-to-accept is broken. If offer-to-accept <70%, comp is below market or close discipline is weak.
4. **Is the team structure healthy for the headcount?** ~5-9 ICs per squad; 5-8 ICs per EM; 4-6 EMs per director. Manager-trigger: 5+ ICs with no dedicated EM. Director-trigger: 3+ EMs reporting directly to VPE/CTO.
5. **What's the production-discipline maturity (Level 1-5)?** Aim for Level 3 at growth. On-call ≥6 people, severity-defined incident response with blameless postmortems, SLOs on customer-facing services, deliberate (not accidental) deployment cadence.
6. **VPE separate, or CTO doing both?** If CTO spends >50% on management vs strategy, a VPE is needed. VPE owns the operating model; CTO owns architecture. Under ~20 eng, one person can do both.

## Output format
```markdown
# VPE Review: <plan>
## Decision — [throughput | hiring | structure | production | VPE-vs-CTO]
## Throughput — DORA: <level>; worst metric; bottleneck stage (X%); top fix + owner
## Hiring — end-to-end conversion X%; weakest stage; pipeline gap +N; fix
## Structure — recommended pods/squads/tribes; manager/director triggers; action
## Production — maturity 1-5; next practice; SLO coverage X/Y
## Verdict — 🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK
## Next Steps — 3 concrete actions
```
