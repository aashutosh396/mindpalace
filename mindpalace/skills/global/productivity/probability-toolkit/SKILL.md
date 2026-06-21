---
name: probability-toolkit
description: "Use when you say 'how likely', 'am I overconfident', 'quantify this', 'what's the base rate', 'expected value', 'scenario weighting', or need to reason about uncertainty, estimates, and risk. Routes to base-rate anchoring, confidence calibration, expected-value calculation, or scenario weighting."
version: 1.0.0
license: MIT
tags: [probability, uncertainty, base-rates, calibration, expected-value, scenarios, risk, forecasting]
source: https://github.com/human-avatar/skills-for-humanity/tree/main/skills/s4h-probability
derived_from: awesomeclaude
---

# Probability Toolkit

Applies probabilistic thinking to estimates, decisions, and uncertainty. Confirm the subject being estimated and the core uncertainty in one sentence, then route.

## Which tool fits

| You need to... | Tool |
|---|---|
| Anchor estimates in historical base rates | Base Rate Anchoring |
| Test whether confidence matches evidence | Confidence Calibration |
| Compare options under uncertainty by EV | Expected Value Calculation |
| Assign probabilities to distinct scenarios | Scenario Weighting |

When unclear → Confidence Calibration; establishing warranted confidence usually determines what other analysis is needed.

## Base Rate Anchoring

Before adjusting for what makes this case special, establish what usually happens in cases like it. Find the reference class, get its historical base rate, then adjust for specific factors — modestly unless those factors are genuinely exceptional. Most people underweight the base rate and overweight the specifics.
**Output:** Reference class, base rate, justified adjustments, final calibrated estimate.

## Confidence Calibration

State the current confidence. Audit it: evidence for? how strong? evidence against considered? Over-confident (common) or under-confident (real but rarer)? Good calibration means your 80%-confident predictions come true ~80% of the time.
**Output:** Evidence for, evidence against, sources of mis-calibration, and a recalibrated confidence level with reasoning.

## Expected Value Calculation

For each option: list outcomes and probabilities, estimate the value (±) of each, compute EV = Σ(probability × value). Compare across options. Flag asymmetric risk — limited downside, large upside — which EV captures but intuition misses.
**Output:** EV per option, comparison table, and interpretation of the asymmetry/risk profile.

## Scenario Weighting

Define 3–5 mutually exclusive, collectively exhaustive scenarios. For each: key conditions, an assigned probability (must sum to 100%), and the optimal decision within it. Aggregate: given the probabilities, the best overall decision.
**Output:** Scenario inventory with probabilities, optimal decision per scenario, and the probability-weighted overall recommendation.
