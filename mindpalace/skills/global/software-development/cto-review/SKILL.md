---
name: CTO Review — Architecture & Scaling Forcing Questions
description: Use when committing to an architecture, planning for 10x load, or weighing a rebuild against a vendor — six questions that surface the next scaling cliff, tech-debt cost, team-scaling ramp, build-vs-buy TCO, SLO/reliability, and security surface.
tags: [architecture, scaling, tech-debt, build-vs-buy, slo, reliability, team-scaling, cto, engineering-strategy]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cto-review
---

# CTO Forcing Questions

Pressure-tests architecture and engineering scaling decisions. Six questions to surface the next scaling cliff before you hit it.

## When to run
Before a major architecture change, before doubling the eng team, before a build-vs-buy >$100K/year, when SLOs are missed, or before committing to a new platform/language/DB.

## The six questions
1. **Scaling Cliff** — Where does the current architecture break, in users / requests / data volume? Be specific ("breaks at 10× because the primary DB writes saturate"). If unknown, load-test before deciding.
2. **Tech Debt Inventory** — Top debt item, cost per week (eng-hours or $), and the date it becomes blocking.
3. **Team Scaling** — For each open req, ramp time and contribution model (pairing / squad / area ownership).
4. **Build vs Buy** — Why build instead of buy, and the 3-year TCO of each? "We want control" or "it's not that hard" → push back. "This is our core moat" → build.
5. **SLO / Reliability** — What are the SLOs for this system and the current error-budget burn? Without an SLO you can't reason about reliability tradeoffs.
6. **Security & Compliance Surface** — What does this expose, and has security signed off? Architecture decisions are compliance decisions.

## Output format
```markdown
# CTO Review: <plan>
## Scaling Cliff — current capacity / break point / headroom months
## Tech Debt — top item / cost per week / blocking date
## Team — open reqs N / median ramp / contribution model
## Build vs Buy — 3yr build TCO / 3yr buy TCO / core-vs-context / decision
## Reliability — SLO defined? / error-budget burn X% (target <Y%)
## Security — sign-off ✅/❌
## Verdict — 🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK + 3 next steps
```
