---
name: Financial Data Collector (yfinance)
description: Use when collecting real financial data for a US public company (price, financials, WACC inputs, analyst estimates) into structured JSON for DCF/comps/earnings analysis — enforces NO FALLBACK, sign conventions, and validation.
tags: [yfinance, financial-data, dcf, wacc, market-data, json, no-fallback, validation, capex]
source: daymade/claude-code-skills
derived_from: financial-data-collector
---

# Financial Data Collector

Collect + validate real financial data for US public companies (free sources). Output: standardized JSON for downstream financial skills.

## Critical constraints
- **NO FALLBACK values**: if a field can't be retrieved, set `null` + `_source: "missing"`. Never substitute defaults (`beta or 1.0`). Downstream decides.
- **Source attribution mandatory**: every section has a `_source`.
- **CapEx sign**: yfinance returns negative (outflow). Preserve original sign; document convention; do NOT flip.
- **yfinance FCF ≠ IB FCF**: yfinance FCF = OperatingCF + CapEx, no SBC deduction. Flag in metadata (for mega-caps SBC is $20-30B/yr → ~30% overstatement).

## Workflow
1. `python scripts/collect_data.py TICKER [--years 5] [--output path.json]` — priority: yfinance (market/financials/beta/estimates) → yfinance `^TNX` (10Y Treasury = risk-free proxy) → user supplement for NaN years (report, don't guess).
2. `python scripts/validate_data.py path.json` — completeness, cross-field (MktCap = Price×Shares), range sanity (WACC 5-20%, beta 0.3-3.0), sign conventions.
3. Deliver single file `{TICKER}_financial_data.json`. Do NOT create README/CSV/summary.

## Output sections
`market_data`, `income_statement` (per year), `cash_flow`, `balance_sheet`, `wacc_inputs`, `analyst_estimates`, `metadata` (with `_capex_convention`, `_fcf_note`).

## Correct patterns
- Missing year: `if pd.isna(revenue): result[year] = {"revenue": None, "_source": "yfinance NaN — supplement from 10-K"}`. Report, don't skip/fill.
- CapEx: `float(cash_flow.loc["Capital Expenditure", col])` preserve negative.
- Datetime cols: `[c for c in financials.columns if c.year == target][0]`.
- Field guards: try `"Total Revenue"` then `"Revenue"` else None.

## Mistakes to avoid
Default values for missing data; assuming all years have data; using yfinance FCF directly in DCF; flipping CapEx sign (`abs()` → double-negation downstream).
