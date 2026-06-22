---
name: A/B Test Setup
description: Use when planning, designing, or implementing an A/B test, split test, or experiment — covers hypotheses, sample size, metrics, variants, traffic allocation, and avoiding the peeking trap.
tags: [ab-test, split-test, experiment, hypothesis, sample-size, statistical-significance, conversion-experiment, mde, multivariate, cro]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/ab-test-setup
---

Design tests that produce statistically valid, actionable results. (For test ideas use page-cro; for tracking infra use analytics-tracking.)

## Core principles
1. **Start with a hypothesis** — a specific prediction, not "let's see what happens."
2. **Test one thing** — single variable, or you can't isolate what worked.
3. **Statistical rigor** — pre-determine sample size, don't peek and stop early.
4. **Measure what matters** — primary metric (business value) + secondary (context) + guardrail (prevent harm).

## Hypothesis framework
`Because [observation/data], we believe [change] will cause [expected outcome] for [audience]. We'll know it's true when [metrics].`
Weak: "changing button color might increase clicks." Strong: "Because users report difficulty finding the CTA (heatmaps + feedback), we believe a larger contrasting button will increase CTA clicks 15%+ for new visitors. Measure: CTR page-view→signup-start."

## Sample size (calculate, don't eyeball)
Two-proportion z-test, α=0.05 two-tailed, 80% power, relative MDE. Quick reference (per variant):
| Baseline | 10% lift | 20% lift | 50% lift |
|---|---|---|---|
| 1% | 163k | 43k | 7.7k |
| 3% | 53k | 14k | 2.5k |
| 5% | 31k | 8.2k | 1.5k |
| 10% | 15k | 3.8k | 683 |
Paste sample-size-per-variation + duration estimate into the test plan before approval. Cross-check against Evan Miller / Optimizely calculators.

## Metrics
Primary (single, ties to hypothesis, calls the test) · Secondary (explain why/how) · Guardrail (must not get worse; stop if significantly negative). Pricing-page example: primary = plan selection rate, secondary = time on page + plan distribution, guardrail = support tickets + refund rate.

## Variants & traffic
Vary headlines/copy, visual design, CTA, or content — single meaningful change, bold enough to detect. Allocation: 50/50 default · 90/10 or 80/20 to limit risk · ramping for technical risk. Users see the same variant on return; balance exposure across time-of-day/week.

## Implementation
Client-side (JS post-load; fast, can flicker; PostHog/Optimizely/VWO) vs server-side (pre-render, no flicker; PostHog/LaunchDarkly/Split).

## Run it
Pre-launch checklist: hypothesis documented · primary metric defined · sample size calculated · variants correct · tracking verified · QA done. During: monitor tech issues, check segment quality, document external factors. **Don't:** peek and stop early (false positives), change variants mid-test, add new traffic sources.

## Analyze
Reached sample size? → statistically significant (p<0.05)? → effect size meaningful vs MDE? → secondary metrics consistent? → guardrails ok? → segment differences (mobile/desktop, new/returning)?
Significant winner → implement · significant loser → keep control, learn why · no difference → more traffic or bolder test · mixed → segment deeper. Document every test (hypothesis, variants+screenshots, results, decision, learnings) — even a losing variant must produce a learning.
