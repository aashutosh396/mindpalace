---
name: Data Quality Auditor
description: Use when checking data quality, profiling a dataset, hunting missing values/outliers, or validating data before analysis or model training — profiles, scores (DQS), and prescribes prioritized remediation.
tags: [data-quality, profiling, missing-values, outliers, mcar-mar-mnar, dqs, data-validation, anomaly-detection, remediation]
source: alirezarezvani/claude-skills
derived_from: engineering/data-quality-auditor
---

# Data Quality Auditor

Systematically assess dataset health, surface hidden issues that corrupt downstream analysis, prescribe prioritized fixes. Never let "good enough" data quietly poison a model or dashboard.

## Entry modes
- **Full audit (new dataset):** profile (shape/types/completeness/distributions) → missing-value analysis (classify MCAR/MAR/MNAR) → outliers (IQR + Z-score) → cross-column checks (referential integrity, duplicates, logical constraints) → score (DQS) + remediation plan.
- **Targeted scan (specific concern):** ask "what broke, when, what changed upstream?" → run relevant check on suspect columns → compare to known-good baseline → trace to root cause (source system, ETL transform, ingestion lag).
- **Monitoring setup:** identify 5-8 critical columns → define thresholds (null %, outlier rate, value domain) → generate monitoring checklist + alerting → schedule at ingestion cadence.

## Data Quality Score (DQS, 0-100, report at top)
| Dimension | Weight | Measures |
|---|---|---|
| Completeness | 30% | null/missing rate on critical columns |
| Consistency | 25% | type conformance, format uniformity, no mixed types |
| Validity | 20% | values within expected domain |
| Uniqueness | 15% | duplicate rows/keys, redundant columns |
| Timeliness | 10% | timestamp freshness, lag from source |

Thresholds: 85-100 production-ready · 65-84 usable with caveats · 0-64 remediation required.

## Outlier methods
IQR (robust, non-parametric) · Z-score (normal assumption) · Modified Z-score / Iglewicz-Hoaglin (robust to skew).

## Proactive risk triggers (surface unprompted)
Silent nulls (encoded as 0/""/"N/A"/"null") · leaky timestamps (future dates, pre-launch, TZ mismatch) · cardinality explosions (free-text masquerading as categorical) · duplicate keys (invalidate joins) · distribution shift (>2σ on mean/std vs baseline) · correlated missingness (nulls in one time range/segment = MNAR).

## Remediation playbook
**Missing:** <1% drop or median/mode impute · 1-10% impute + `col_was_null` indicator · 10-30% impute cautiously, investigate, document · >30% flag for domain review, don't impute blindly.
**Outliers:** likely error (impossible) → cap/correct/drop · legitimate extreme → keep, document, consider log transform · unknown → flag, don't silently remove.
**Duplicates:** confirm key with owner first; `keep='last'` for event data; `keep='first'` for SCD tables.

## Confidence tags
🟢 Verified (confirmed by inspection/owner) · 🟡 Likely (strong signal) · 🔴 Assumed (inferred — never auto-remediate without human confirmation).

## Report structure
**Bottom Line** (DQS + one-sentence verdict) → **What** (issues ranked by severity × breadth) → **Why It Matters** (business/analytical impact) → **How to Act** (ordered remediation steps).
