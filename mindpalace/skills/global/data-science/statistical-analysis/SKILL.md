---
name: statistical-analysis
description: "Use when you need to run or interpret a statistical test and report it correctly — choosing the right test, checking assumptions, computing effect sizes, and writing APA-style results. Triggers: 'which statistical test', 't-test', 'ANOVA', 'chi-square', 'regression', 'correlation', 'is this significant', 'p-value', 'effect size', 'confidence interval', 'A/B test analysis', 'compare two groups', 'Bayesian test', 'check assumptions'. For laying out a study use experimental-design; for sample size use statistical-power."
version: 1.0.0
license: MIT
tags: [statistics, hypothesis-testing, t-test, anova, regression, correlation, effect-size, ab-testing, apa, bayesian]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/statistical-analysis
derived_from: awesomeclaude
prerequisites: "Python 3.10+ with scipy>=1.11, statsmodels>=0.14.6, pingouin>=0.6, pandas, matplotlib, seaborn. Optional Bayesian: pymc>=5, arviz."
---

# Statistical Analysis

## What it does
Guides a complete, defensible statistical analysis: pick the appropriate test for the question and data, verify assumptions before trusting results, compute and interpret effect sizes (not just p-values), and report in APA format. Useful for A/B tests, experiment readouts, survey analysis, and any "is this difference real?" question.

## When to use
- Hypothesis tests: t-tests, ANOVA, chi-square, non-parametric alternatives
- Regression (linear, multiple, logistic) and correlation
- Effect sizes, confidence intervals, multiple-comparison correction
- Bayesian alternatives (Bayes Factors, direct probability statements)
- Checking statistical assumptions and diagnostics
- Reporting results cleanly (APA-style figures/tables)

## Decision flow
1. Need to SELECT a test? → Test Selection Guide below
2. Have a test? → Check ASSUMPTIONS
3. Assumptions OK? → Run the ANALYSIS
4. Done? → REPORT with effect size + CI + interpretation

## Test selection
**Two groups:**
- Independent, continuous, normal → independent t-test
- Independent, continuous, non-normal → Mann-Whitney U
- Paired, normal → paired t-test; non-normal → Wilcoxon signed-rank
- Binary outcome → chi-square or Fisher's exact

**3+ groups:**
- Independent, normal → one-way ANOVA; non-normal → Kruskal-Wallis
- Paired, normal → repeated-measures ANOVA; non-normal → Friedman

**Relationships:**
- Two continuous → Pearson (normal) or Spearman (non-normal)
- Continuous outcome + predictors → linear regression
- Binary outcome + predictors → logistic regression

Every test has a Bayesian version giving Bayes Factors and the ability to support the null.

## Assumption checking (always before interpreting)
1. **Outliers** — IQR and z-score
2. **Normality** — Shapiro-Wilk + Q-Q plot
3. **Homogeneity of variance** — Levene's test + box plots
4. **Linearity** (regression) — residual plots

When violated:
- Normality, mild + n>30/group → parametric is robust; moderate → non-parametric; severe → transform or non-parametric
- Unequal variance → Welch's t-test / Welch's ANOVA; regression → robust SEs or WLS
- Non-linearity → polynomial terms or transformation

## Reporting
- Report the test statistic, df, exact p, **effect size**, and **confidence interval**.
- Distinguish statistical from practical significance.
- State which assumptions were checked and what you did about violations.
- APA example: `t(58) = 2.34, p = .023, d = 0.61, 95% CI [0.08, 1.13]`.

## Notes
- Pingouin 0.5+ renamed output columns (`p_unc`, `cohen_d`, `CI95`).
- Pin `statsmodels>=0.14.6` with `scipy>=1.11` to avoid `_lazywhere` import errors on SciPy 1.16+.
- For OLS/GLM/ARIMA model APIs use statsmodels directly; for full Bayesian workflows use PyMC.
