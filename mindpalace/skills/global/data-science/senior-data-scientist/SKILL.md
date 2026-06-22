---
name: Senior Data Scientist
description: Use when designing or analyzing experiments, building/evaluating ML models, or doing causal inference — A/B test sizing & analysis, feature pipelines, cross-validated model eval, and difference-in-differences with ready Python code + checklists.
tags: [ab-testing, experiment-design, causal-inference, feature-engineering, model-evaluation, xgboost, mlflow, statistics, did, python]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-data-scientist
---

# Senior Data Scientist

Statistical modeling, experiment design, causal inference, predictive analytics. Python (NumPy/Pandas/scikit-learn), R, SQL.

## 1. A/B test design & analysis
Sample size (per variant) from baseline rate + minimum detectable effect:
```python
def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    p1 = baseline_rate; p2 = baseline_rate * (1 + mde)
    effect = abs(p2 - p1) / np.sqrt((p1*(1-p1) + p2*(1-p2))/2)
    n = ((stats.norm.ppf(1-alpha/2) + stats.norm.ppf(power)) / effect) ** 2
    return int(np.ceil(n))
```
Analyze with a two-proportion z-test; report **lift + 95% CI**, not just p-value.

**Checklist:** ONE primary metric (pre-register secondaries) · size BEFORE starting · randomize at USER level · run ≥1 full business cycle (≈2 weeks) · check sample-ratio mismatch (<1%) · Bonferroni-correct (`alpha/n_metrics`) when testing multiple metrics.

## 2. Feature engineering pipeline
Use `ColumnTransformer`: numeric → median impute + StandardScaler; categorical → most-frequent impute + OneHotEncoder(handle_unknown='ignore'). Extract cyclical time features (sin/cos of dayofweek, month) + is_weekend.

**Checklist:** fit transformers on TRAIN only, transform test · log-transform right-skewed features before scaling · target-encode high-cardinality (>50 levels) · generate lag/rolling features BEFORE the split (avoid leakage) · document each feature's business meaning.

## 3. Train, evaluate, select
Cross-validate with `StratifiedKFold` (classification); score with `roc_auc` AND `average_precision`. Track `overfit_gap = train_mean - test_mean`. Log everything to MLflow (`log_params`, `log_metrics`, `log_model`).

**Checklist:** report AUC-PR alongside AUC-ROC for imbalanced data · flag `overfit_gap > 0.05` · calibrate probabilities (Platt/isotonic) before prod · compute SHAP to sanity-check importances · beat a DummyClassifier baseline · never compare runs from notebook output — use MLflow.

## 4. Causal inference — difference-in-differences
OLS DiD with HC3 robust SEs; the `treatment:post` interaction coefficient is the ATT:
```python
result = smf.ols(f"{outcome} ~ {treat} * {post} + {covariates}", data=df).fit(cov_type="HC3")
att = result.params[f"{treat}:{post}"]
```
**Checklist:** validate parallel trends in the pre-period · HC3 SEs for heteroskedasticity · cluster SEs at unit level for panel data · consider propensity matching if groups differ at baseline · report ATT + CI, not just significance.
