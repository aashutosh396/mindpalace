---
name: Pricing Strategist
description: Use when designing or revisiting product pricing — selecting a pricing model (seat/usage/value/freemium/hybrid), running Van Westendorp PSM on WTP survey data, or designing Good/Better/Best packaging tiers. Recommends a model + range, never a single number.
tags: [commercial, pricing, packaging, wtp, van-westendorp, value-based-pricing, saas-pricing, good-better-best, freemium]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/pricing-strategist
---

# Pricing Strategist

Pricing-design decision support. Recommends **a model and a range**; the human picks the number. (Not per-deal discounting, not brand positioning.)

## Workflow
1. **Assess customer context** — industry, avg deal size, customer count, value drivers, adoption curve, consumption pattern (seat/usage/value/hybrid), competitor models.
2. **Pick the pricing model** — rank 5 models (subscription seat-based / usage-based / value-based / freemium / hybrid) by fit 0-100. Deterministic logic: low usage variance + high seat-attach → subscription; power-law usage + variable customer value → usage-based.
3. **Validate WTP with Van Westendorp PSM** — needs ≥4 questions/respondent (too cheap / bargain / getting expensive / too expensive). Output: 4 intersection points (OPP, IDP, PMC, PME) + the Range of Acceptable Prices. **N≥30 minimum, ≥100 preferred** — below 30 the result is statistical noise. PSM gives a range, not the price.
4. **Design packaging** — 3-tier Good/Better/Best with anti-pattern flags (decoy tier, feature dump, no upgrade trigger, Bronze loss leader, Enterprise no-anchor).
5. **Decide** — take model + range + packaging to the pricing committee.

## Anti-patterns
- Recommending a specific number (emit a model + range).
- Using PSM with N<30; treating PSM as "the price" (test the range in market).
- Picking value-based without a measurable value metric (collapses into bad usage-based).
- Designing tiers before picking a model.
- Feature-dumping the Best tier (3x features for 2x price → customers buy Better, never upgrade).
- Hidden usage-based pricing inside a subscription tier (pick one model).

## Forcing questions (one at a time, recommended + canon)
1. Paying for outcomes, seats, or usage? → outcomes if measurable; usage if marginal cost is variable; seats only if usage is flat per user. (Ramanujam *Monetizing Innovation* mistake #1)
2. Measurable value metric, or guessing? → instrument it BEFORE going value-based. (ProfitWell)
3. Usage variance top-decile vs median? → >10x usage-based; <3x subscription; between hybrid+overage. (Poyar)
4. Competitor's pricing model — same or different, and why? → surface the differentiation hypothesis. (Skok: pricing is a positioning signal)
5. Sample size for WTP, segmented? → N≥30/segment PSM, ≥100 conjoint. (van Westendorp 1976; Sawtooth)
6. The ONE feature that forces a tier upgrade? → every Better/Best needs a single non-negotiable trigger. (Ramanujam mistake #4)
