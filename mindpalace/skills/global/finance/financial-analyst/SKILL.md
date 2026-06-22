---
name: Financial Analyst
description: Use when analyzing financial statements, building a DCF valuation, assessing budget variances, or constructing driver-based forecasts — runs ratio analysis (5 categories), WACC/terminal-value DCF with sensitivity, variance with materiality filtering, and base/bull/bear scenarios.
tags: [financial-analysis, ratio-analysis, dcf, valuation, wacc, budget-variance, forecasting, cash-flow, financial-modeling]
source: alirezarezvani/claude-skills
derived_from: finance/skills/financial-analyst
---

# Financial Analyst

Ratio analysis, DCF valuation, budget variance, and rolling forecasts for strategic decisions.

## 5-phase workflow

1. **Scoping** — objectives + stakeholders, data sources + periods, materiality thresholds + accuracy targets, choose frameworks.
2. **Data analysis & modeling** — collect + validate statements (income, balance sheet, cash flow); validate completeness (missing fields, nulls, implausible values) before computing; calculate ratios across 5 categories; build DCF (WACC + terminal value) and cross-check outputs against sanity bounds (implied multiples vs comparables); construct variance with favorable/unfavorable classification; develop driver-based forecasts with scenarios.
3. **Insight generation** — interpret ratio trends vs industry benchmarks, identify material variances + root causes, assess valuation ranges via sensitivity, evaluate base/bull/bear.
4. **Reporting** — executive summary, variance reports by dept/category, DCF with sensitivity tables, rolling forecasts with trend analysis.
5. **Follow-up** — track forecast accuracy (target ±5% revenue, ±3% expenses), update with actuals, refine assumptions.

## Ratio categories

- **Profitability** — ROE, ROA, Gross/Operating/Net Margin
- **Liquidity** — Current, Quick, Cash ratios
- **Leverage** — Debt-to-Equity, Interest Coverage, DSCR
- **Efficiency** — Asset/Inventory/Receivables Turnover, DSO
- **Valuation** — P/E, P/B, P/S, EV/EBITDA, PEG

## DCF valuation

WACC via CAPM → revenue + free-cash-flow projections (5-year default) → terminal value (perpetuity growth AND exit multiple) → enterprise value → equity value → two-way sensitivity (discount rate × growth rate).

## Budget variance

Dollar + percentage variance (actual vs budget vs prior year) → materiality threshold filter (default 10% or $50K) → favorable/unfavorable classification with revenue/expense logic → department + category breakdown → executive summary.

## Forecast builder

Driver-based revenue model → 13-week rolling cash-flow projection → base/bull/bear scenarios → trend analysis via simple linear regression.

## Targets

Forecast accuracy: ±5% revenue, ±3% expenses · report delivery 100% on time · complete documentation for all assumptions · 100% of material variances explained.

> Validate every output against the user's source data; this is analysis support, not investment advice. Tooling is stdlib-only (math/statistics/json), no numpy/pandas required; accepts flat per-tool keys or one nested bundle. Related: business-investment-advisor (single capex), saas-metrics-coach (SaaS unit economics).
