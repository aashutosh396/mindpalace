---
name: ecom-report
description: "Use when reviewing a D2C / online store from an order-transaction CSV — keywords: ecommerce review, store review, store health, business review, revenue/customer/product analysis, AOV, retention, repeat purchase, churn, KPI tree, 'how was last month', 'why did revenue drop', 'how's retention'."
version: 1.0.0
license: MIT
tags: [ecommerce, d2c, analytics, kpi, revenue, retention, csv, business-review, reporting, data-science]
source: https://github.com/takechanman1228/claude-ecom
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# ecom-report — Ecommerce Business Review Toolkit

D2C ecommerce analytics over order-transaction CSVs. A bundled Python engine
computes KPIs, runs ~30 health checks, and scores performance; **you (Claude)
interpret the numbers** and write the human report.

**Key principle:** Python computes the numbers. Claude interprets them. Never
present raw numbers without business context.

## When to use

User wants a review/health-check of an online store, or asks revenue / customer
/ product questions over order data ("how was last month", "how's retention",
"why did revenue drop"). Trigger phrases: ecommerce review, store review, store
health, business review.

## Input

Order-transaction CSV — each row = one order or line item.
- Required: order ID, order date, customer ID (or email), revenue (after
  discounts, before tax/shipping).
- Optional: quantity, SKU/product, discount amount. Column names are fuzzy-matched.

If no CSV given, glob `*.csv` in the working dir; ask if multiple plausible files.

## Mode selection

| Args / intent | Mode | Output |
|---|---|---|
| empty or `review` | Full Review (auto-picks periods from data) | `REVIEW.md` |
| `review 30d` / `90d` / `365d` | Full Review, single period | `REVIEW_{PERIOD}.md` |
| a natural-language question | Focused Query | inline answer (10-30 lines), no file |

## Running the engine

The repo ships a Python package (`claude_ecom/`) exposing an `ecom` CLI plus a
launcher at `bin/ecom`. Get the source from
https://github.com/takechanman1228/claude-ecom (clone it, `pip install -e .`,
or run `bin/ecom` which bootstraps a private venv under
`~/.local/share/claude-ecom/`).

```bash
ecom review orders.csv --output <out-dir>
ecom review orders.csv --period 90d --output <out-dir>
```

Output: `review.json` (or `review_{period}.json`) in the output dir.

The engine computes, per available period: summary KPIs with prior-period
comparison, a new-vs-returning KPI tree, revenue-driver decomposition (AOV /
volume / mix), and — for 365d — repeat purchase rate plus a 12-month
monthly_trend. It evaluates ~30 health checks (Revenue, Customer, Product),
each pass / watch / fail, powering the 🟢/🟡/🔴 markers.

## Workflow

**Phase 1 — Compute (Python):** run the engine (add `--period` per Mode table).

**Phase 2 — Interpret (you):**

Full Review:
1. Read `review.json`.
2. Read the engine's `skills/ecom/references/report-format.md` (section
   templates + Finding Quality Standards) — required before writing.
3. Read `references/review-narratives.md` to pick the narrative arc.
4. Load other references as needed (see table).
5. Write `REVIEW.md` / `REVIEW_{PERIOD}.md` satisfying the Report Contract.

Focused Query:
1. Read `references/focused-query.md` (query→period mapping + answer format).
2. Run the engine per that mapping, read the JSON, answer inline. No file.

Period analysis tells you *where things are heading*; health checks tell you
*what's broken now*. The report weaves both into one story.

## Report Contract (Full Review)

All sections, this exact order (reordering = format violation):
1. Executive Summary — narrative blockquote (4-6 lines) + Scoreboard table
2. 30d Pulse (if data) — KPI tree + max 1 finding
3. 90d Momentum (if data) — KPI tree + drivers + max 2 findings
4. 365d Structure (if data) — KPI tree + drivers + max 3 findings
5. Action Plan — max 5 items by time horizon + Guardrails (required)
6. Data Notes — 2-4 lines

Hard rules:
- ~150 lines total; 5-7 findings max across all periods; never repeat a finding.
- No standalone "What's Working" / "Issues" sections — positives live in the
  Executive Summary and KPI-tree markers.
- Every period section uses the KPI tree format with 🟢/🟡/🔴 markers.
- Every finding follows **What is → Why it matters → What to do** (fact →
  data-backed tension → direction). "consider / improve / optimize / explore"
  are banned.
- Action Plan is the single source of truth for deadlines + success metrics,
  ending in Guardrails (2-3 must-not-deteriorate metrics).

## Reference files (load on-demand, from the engine's `skills/ecom/references/`)

| File | When |
|---|---|
| report-format.md | every Full Review, before writing |
| review-narratives.md | every Full Review — narrative arc |
| focused-query.md | every Focused Query |
| review-schema.md | when review.json semantics unclear |
| finding-clusters.md | grouping related issues into themes |
| recommended-actions.md | turning watch/fail checks into actions |
| impact-formulas.md | estimating revenue impact |
| health-checks.md | a check's definition/threshold unclear |
| benchmarks.md | comparing KPIs to D2C benchmarks |

## Data rules

- **review.json only.** All numbers must come from review.json or be derived
  from it. Never quote external sources (Shopify Analytics, GA, …) — though
  recommending an external investigation as an *action* is fine.
- `periods` holds only periods marked true in `data_coverage`; all `_change`
  fields are proportional vs prior period (0.08 = +8%).
- `health.top_issues` = pre-sorted failing checks; `action_candidates` =
  Python's raw suggestions — rewrite in business language, never copy verbatim.
- Never expose internal check IDs or check counts.
- When `data_quality` is non-empty, surface relevant warnings in Data Notes;
  don't present partial-month MoM as real signal.

## Gotchas / quality gates

- Omit what you can't measure — no N/A, no empty sections, no apologies.
  Shorter data = shorter report.
- Write the whole report in ONE language, matching the user's prompt/store.
- Always interpret, never dump numbers. Business language, not jargon.
- Connect findings into systemic patterns. 80/20: ~80% confirmation (trust),
  ~20% surprise (action).
- No numeric scores, letter grades, or % health ratings — pass/watch/fail only.
- First `bin/ecom` run is slow (venv bootstrap); later runs are instant.
