---
name: Experiment Designer
description: Use when planning product experiments, writing testable hypotheses, estimating sample size, prioritizing tests, or interpreting A/B outcomes — applies practical statistical rigor to product decisions.
tags: [experiment, ab-test, hypothesis, sample-size, mde, ice-scoring, statistics, product, power-analysis]
source: alirezarezvani/claude-skills
derived_from: product-team/experiment-designer
---

# Experiment Designer

Design, prioritize, and evaluate product experiments with clear hypotheses and defensible decisions.

## Core Workflow

1. **Write hypothesis** (If/Then/Because): If we change [intervention], Then [metric] will change by [direction/magnitude], Because [behavioral mechanism].
2. **Define metrics before running** — primary (single decision metric), guardrails (quality/risk protection), secondary (diagnostics only).
3. **Estimate sample size** — from baseline rate/mean, minimum detectable effect (MDE, absolute or relative), alpha, power.
4. **Prioritize with ICE** — `(Impact × Confidence × Ease) / 10`.
5. **Launch with stopping rules** — decide fixed sample size OR fixed duration in advance; avoid repeated peeking; monitor guardrails continuously.
6. **Interpret** — statistical significance ≠ business significance; compare point estimate + CI to decision threshold; investigate novelty effects and segment heterogeneity.

## Hypothesis Quality Checklist

- [ ] Explicit intervention + audience
- [ ] Measurable metric change
- [ ] Plausible causal reason
- [ ] Expected minimum effect
- [ ] Defined failure condition

## Common Pitfalls

Underpowered tests (false negatives); too many simultaneous changes without isolation; changing targeting/implementation mid-test; stopping early on random spikes; ignoring sample-ratio mismatch + instrumentation drift; declaring success from p-value without effect-size context.

## Statistical Interpretation Guardrails

- p < alpha = evidence against null, not guaranteed truth.
- CI crossing zero/no-effect = uncertain directional claim.
- Wide intervals = low precision even when significant.
- Use practical significance thresholds tied to business impact.
