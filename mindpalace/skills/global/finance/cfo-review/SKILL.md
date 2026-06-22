---
name: CFO Review — Money Forcing Questions
description: Use when a plan commits meaningful spend — a hiring wave, a fundraise, a new channel budget — runs six numerate-skeptic questions on unit economics, runway, dilution, and capital allocation before any spend.
tags: [finance, burn-rate, runway, unit-economics, ltv-cac, dilution, capital-allocation, fundraise, cfo]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cfo-review
---

# CFO Forcing Questions

The numerate skeptic stress-tests anything that touches money. Six questions before any spend or fundraise — answered with numbers, not adjectives.

## When to run
- Before any spend >1% of revenue; before opening a hiring requisition; before any fundraise conversation.
- Before changing pricing/unit economics; before signing a multi-year contract.

## The six questions
1. **Burn & Runway** — burn multiple (net burn ÷ net new ARR; above 2x is a problem) and months of cash at base/bull/bear. If bear case <12 months, you're already in fundraising mode.
2. **Unit Economics** — LTV/CAC per channel and payback on the top 2. LTV/CAC >3x and payback <12 months are healthy. If either is broken, don't scale that channel.
3. **Dilution Path** — if a raise is required, founder dilution at base and bear valuations; cumulative dilution to next 2 rounds.
4. **Capital Allocation Alternative** — if this dollar weren't spent here, where else (hiring/product/marketing) and at what return? Make opportunity cost explicit.
5. **Revenue Quality** — gross margin and its trend at scale. If margin compresses with scale, the model is broken; cost-of-revenue should grow slower than revenue.
6. **Bear Case Survival** — if revenue is 50% of plan, does the company survive 18 months? Default-alive is non-negotiable; if not, identify cut triggers in advance.

## Output format
```markdown
# CFO Review: <plan>
## Numbers
- Burn multiple: X.Xx
- Runway (base/bull/bear): X / X / X months
- LTV/CAC top channel: X.Xx, payback Y months
- Gross margin: X% (trend)
- Dilution this round: X%
- Bear-case survival: PASS / FAIL
## Verdict — 🟢 GREEN (fund) | 🟡 YELLOW (fund with cut triggers) | 🔴 RED (kill/revise)
## Conditions (if YELLOW) — cut trigger: <metric> < <threshold> → <action>; review date
## Recommendation — 3 next steps
```
