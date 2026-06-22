---
name: Revenue Operations Analytics
description: Use when analyzing sales pipeline health, forecasting revenue, or measuring go-to-market efficiency for SaaS — three deterministic analyses: pipeline coverage/velocity/risk, forecast accuracy (MAPE/bias), and GTM efficiency benchmarks.
tags: [revops, pipeline, forecast-accuracy, mape, gtm-efficiency, magic-number, ltv-cac, rule-of-40, nrr, saas]
source: alirezarezvani/claude-skills
derived_from: business-growth/skills/revenue-operations
---

# Revenue Operations

Pipeline analysis, forecast accuracy tracking, and GTM efficiency measurement for SaaS revenue teams. Three deterministic analyses (run on exported CRM/finance data; cross-check totals against source before drawing conclusions).

## 1. Pipeline analysis
Key metrics:
- **Coverage ratio** = total pipeline ÷ quota (healthy 3-4x).
- **Stage conversion rates** — stage-to-stage progression.
- **Sales velocity** = (opportunities × avg deal × win rate) ÷ avg sales cycle.
- **Deal aging** — flag deals exceeding 2× average cycle time per stage.
- **Concentration risk** — warn when >40% of pipeline sits in one deal.
- **Coverage gap** — quarters with insufficient pipeline.

## 2. Forecast accuracy
- **MAPE** = mean(|actual − forecast| ÷ |actual|) × 100.
- **Bias** — over-forecast (positive) vs under-forecast (negative).
- **Weighted accuracy** — MAPE weighted by deal value.
- **Trends** — improving / stable / declining over periods.
- **Category breakdown** — by rep, product, segment.

Ratings: <10% Excellent · 10-15% Good · 15-25% Fair · >25% Poor.

## 3. GTM efficiency benchmarks
| Metric | Formula | Target |
|---|---|---|
| Magic Number | Net New ARR ÷ prior-period S&M | >0.75 |
| LTV:CAC | (ARPA × gross margin ÷ churn) ÷ CAC | >3:1 |
| CAC Payback | CAC ÷ (ARPA × gross margin) | <18 mo |
| Burn Multiple | Net Burn ÷ Net New ARR | <2x |
| Rule of 40 | Growth% + FCF margin% | >40% |
| Net Dollar Retention | (Begin + Expansion − Contraction − Churn) ÷ Begin | >110% |

## Workflows
- **Weekly pipeline review** — verify export currency → run pipeline analysis → cross-check vs CRM → review coverage/aging/concentration/funnel shape → action aging deals and gaps.
- **Forecast review (monthly/quarterly)** — confirm all periods have actuals → analyze MAPE trend, high-error reps/segments, systematic bias → coach high-bias reps, fix data hygiene.
- **GTM audit (quarterly/board prep)** — reconcile revenue/cost/customer figures with finance → benchmark Magic Number, LTV:CAC, payback, Rule of 40 → adjust spend allocation and retention.
- **QBR** — combine all three: forward-looking coverage + backward-looking accuracy + efficiency benchmarks, cross-referenced.
