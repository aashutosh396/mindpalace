---
name: Business Assumption Stress Test
description: Use before betting on a plan whose core assumptions are unvalidated (revenue projection, market size, moat, hiring velocity, retention) — isolates the assumption, finds counter-evidence, models the downside, calculates sensitivity, and proposes a hedge.
tags: [stress-test, assumptions, downside-modeling, sensitivity, counter-evidence, hedge, calibration]
source: alirezarezvani/claude-skills
derived_from: executive-mentor/stress-test
---

# Stress-Test — Break the Assumption Before the Market Does

The most dangerous assumptions are the ones everyone agrees on. Stress testing isn't pessimism — it's calibration.

## Methodology

**1. Isolate the assumption.** State it explicitly and specifically. Not "our market is large" but "TAM for B2B spend-management software in German SMEs is €2.3B." Vague = unfalsifiable = useless. Types: market size, customer behavior, revenue model, competitive position, execution, macro.

**2. Find the counter-evidence.** Actively search for why it's wrong: Who tried this and failed? What data contradicts it? What's the bear case? What would a smart skeptic point to? What's the base rate? The goal is to surface what you don't know, not to find a reason to stop.

**3. Model the downside.** Don't just model base + upside. Build bear (-30%), stress (-50%), catastrophic (-80%) with probabilities. Key question per level: *does the business survive? does the plan still make sense?* For qualitative assumptions: earliest signal it's wrong, how long to notice, what happens in that gap.

**4. Calculate sensitivity.** If this one assumption changes, how much does the outcome change? (CAC doubles → runway? churn 5%→10% → NRR in 24mo? cycle 3mo→6mo → Q3 revenue?) High sensitivity = key lever.

**5. Propose the hedge.** Validation hedge (test before betting — pilot/experiment), contingency hedge (plan B if wrong), early-warning hedge (leading indicator + threshold to act).

## Patterns by Assumption Type
- **Revenue** — model from historical win rates, not hoped-for. Test: top-3 deals slip a quarter; rep ramps in 4mo not 2; expansion doesn't materialize.
- **Market size** — build the actual account list, count it, ×ACV = SAM. Test: how many ICP companies can you name? what % currently spend on any solution?
- **Moat** — ask churned customers if a competitor could've kept them. Test: well-funded competitor copies best feature in 90 days — what do customers do?
- **Hiring** — model the plan with 0 net new hires; what still works? Test: VP hire takes 5mo not 2; only 70% of headcount lands.
- **Competitive response** — assume incumbents respond if you're winning; model speed + resource asymmetry.

## Output
```
ASSUMPTION (exact) / SOURCE
COUNTER-EVIDENCE (specific + comparable failure + contradicting data)
DOWNSIDE MODEL: bear -30% / stress -50% / catastrophic -80% (survive?)
SENSITIVITY: HIGH/MED/LOW — 10% change → X change in outcome
HEDGE: validation / contingency / early-warning (indicator + threshold)
```
