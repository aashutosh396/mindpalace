---
name: Product Analytics
description: Use when defining product KPIs, building metric dashboards, running cohort/retention analysis, or interpreting feature adoption — picks the right metric framework per product stage and reads retention curves correctly.
tags: [product-analytics, kpi, retention, cohort, funnel, aarrr, north-star, heart, dashboard, metrics]
source: alirezarezvani/claude-skills
derived_from: product-team/product-analytics
---

# Product Analytics

Define, track, and interpret product metrics across discovery, growth, and mature stages.

## Workflow

1. **Select framework** — AARRR (growth loops, funnel visibility); North Star (cross-functional strategic alignment); HEART (UX quality).
2. **Define stage-appropriate KPIs** (below).
3. **Design dashboard layers** — executive (5-7 directional metrics), product health (acquisition/activation/retention/engagement), feature (adoption/depth/repeat/outcome correlation).
4. **Run cohort + retention** — segment by signup or feature-exposure cohort; compare curves not snapshots; find inflection around onboarding + first-value moment.
5. **Interpret & act** — connect movement to product changes/release timeline; separate signal from noise via period-over-period; propose one product action per major risk/opportunity.

## KPIs by Stage

- **Pre-PMF** — activation rate, week-1 retention, time-to-first-value, problem-solution-fit interview score.
- **Growth** — funnel conversion by stage, monthly retained users, feature adoption among new cohorts, expansion/upsell proxies.
- **Mature** — NRR-aligned product metrics, power-user share + depth, churn-risk indicators by segment, reliability/support-deflection metrics.

## Dashboard Principles

Show trends not point estimates · one owner per KPI · pair each KPI with target + threshold + decision rule · cohort/segment filters by default · comparable time windows.

## Cohort Analysis Method

1. Define cohort anchor event (signup/activation/first purchase). 2. Define retained behavior (active day/key action/repeat session). 3. Build retention matrix by cohort period × age period. 4. Compare curve shape across cohorts. 5. Flag early drop points and investigate journey friction.

## Retention Curve Interpretation

- Sharp early drop, low plateau → onboarding mismatch / weak initial value.
- Moderate drop, stable plateau → healthy core, predictable churn.
- Flattening at low level → occasional use, revisit value metric.
- Improving newer cohorts → onboarding/positioning improvements working.

## Anti-Patterns

Vanity metrics (pair acquisition with activation + retention); single-point retention (compare curves); dashboard overload (exec 5-7, feature per-feature only); no decision rule (every KPI needs target/threshold/owner + "if below X then Y"); averaging across segments (segment by cohort/tier/channel/geo); ignoring seasonality (period-over-period with same-period-last-year).
