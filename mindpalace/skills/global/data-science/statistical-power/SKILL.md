---
name: statistical-power
description: "Use when you need a sample size or power calculation for planning a study or A/B test. Triggers: 'how many subjects/samples/users do I need', 'sample size', 'power analysis', 'a priori power', 'minimum detectable effect', 'MDE', 'power curve', '80% power', 'justify sample size', 'how long to run this A/B test', or any mention of effect size + alpha + power. For laying out the study use experimental-design; for analyzing collected data use statistical-analysis."
version: 1.0.0
license: MIT
tags: [power-analysis, sample-size, mde, ab-testing, effect-size, study-planning, monte-carlo, statistics]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/statistical-power
derived_from: awesomeclaude
prerequisites: "Python 3.10+ with statsmodels>=0.14.6, scipy>=1.11, pingouin>=0.6, numpy>=1.26, matplotlib. Optional: statsmodels mixed models, lifelines for simulation-based power."
---

# Statistical Power & Sample Size

## What it does
Answers the highest-leverage pre-study question: **how large a sample do you need to reliably detect an effect of a given size, and what could you detect with the sample you can afford?** Underpowered studies waste effort and produce inconclusive/irreproducible results; overpowered ones waste resources. Get this right before collecting data.

## The core relationship
Four quantities are locked together for any test: **sample size (n)**, **effect size**, **significance level (α)**, and **power (1 − β)**. Fix any three and the fourth is determined. Every calculation here is a rearrangement of that.

## When to use
- A priori sample size before collecting data
- Minimum detectable effect (MDE) for a fixed sample size you already have
- Power curves (power vs n, or power vs effect size) for a plan or grant
- Justifying a sample size for a protocol, pre-registration, or stakeholder
- Unequal group sizes / non-1:1 allocation
- Designs without a textbook formula (mixed models, logistic/Poisson regression, cluster-randomized, survival, mediation, interactions) → simulation
- Accounting for multiple comparisons, attrition/dropout, or clustering

## Two approaches
- **Closed-form** — fast, exact for standard tests (t-tests, ANOVA, proportions, correlations, chi-square, regression). Use `statsmodels.stats.power` and friends.
- **Simulation / Monte Carlo** — works for *any* design you can simulate and analyze: pick parameters, generate many synthetic datasets, run the planned analysis on each, and the fraction that reach significance is your power. The only general method for complex models.

## Workflow
1. **State the test** you'll actually run (this dictates the power method).
2. **Choose an effect size** — usually the hardest part. Use a minimum effect worth detecting (practical significance), a pilot estimate, or a literature/benchmark value. Convert between effect-size families as needed (Cohen's d, f, h, r, odds ratio).
3. **Fix α and target power** (commonly α=0.05, power=0.80; use 0.90 for high-stakes).
4. **Solve for n** (or for MDE if n is fixed).
5. **Adjust for reality** — inflate for expected dropout/attrition, deflate effective n for clustering (design effect), apply multiple-comparison correction to α.
6. **Report** the assumptions: test, effect size and its source, α, target power, allocation, and resulting n (or MDE) — so the number is defensible.

## Practical notes
- For A/B tests: convert your baseline conversion rate + minimum lift into an effect size (proportions → Cohen's h), then solve for users per arm; combine with traffic to get test duration.
- Always state the effect size and its justification — a sample size without a stated effect is not interpretable.
- When no formula exists, simulate. It's slower but honest.
