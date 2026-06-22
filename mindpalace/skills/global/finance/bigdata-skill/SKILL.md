---
name: Bigdata.com SDK + REST Toolkit
description: Use when working with Bigdata.com / RavenPack and the MCP only returns pre-synthesized prose/tearsheets but you need machine-readable structured financials, prices, analyst estimates, daily entity-sentiment, annotated chunks, or a screener — drops to the official SDK + `/v1/*` REST.
tags: [bigdata, ravenpack, financial-data, analyst-estimates, sentiment, sec-financials, screener, rest-api, investment-research, entity-resolution]
source: daymade/claude-code-skills
derived_from: bigdata-skill
---

# Bigdata.com SDK + REST Toolkit

Get the structured substrate the Bigdata.com MCP doesn't hand over. The MCP optimizes for a chat turn — its search returns chunks with no per-chunk sentiment or entity spans, and its tearsheets give aggregates, not fiscal-period time series, a universe screener, or per-field JSON. The official `bigdata-client` SDK plus a thin REST passthrough (same backend, same JWT) reach the official `/v1/*` endpoints that hold it.

> General pattern: when an MCP data source returns only synthesized output but you need the structured fields underneath, drop to the vendor SDK or REST.

Bigdata is sunsetting the SDK (EOL 2026-12-31) in favor of the REST API, so the REST layer is forward-compatible. SDK covers search + knowledge-graph; `bd._api.http` reaches every `/v1/*` endpoint the SDK never wrapped. The bundled `bigdata_toolkit` packages both behind one `BigdataClient`.

## When to use
Bigdata.com/RavenPack and MCP feels thin ("where's the sentiment score?"); want forward/structured financials (estimates, calendar, surprise, ratings, price targets, screener); want annotated news chunks with numeric sentiment + entity spans, or a sentiment time series / co-mention graph; mention a `bd_v2_` key, `rp_entity_id`, `query_unit`/chunk cost; building a reusable cost-aware research dataset.

## Setup
```bash
export BIGDATA_API_KEY=bd_v2_xxxxxxxx          # never hardcode; client fail-fasts if missing
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python bigdata-client
# proxy (if needed): export HTTPS_PROXY=http://host:port  (+ WSS_PROXY for chat)
# TLS-intercepting proxy: BigdataClient(verify_ssl="<proxy-CA>.pem")
```
Put `scripts/` on PYTHONPATH. Smoke test: `BIGDATA_API_KEY=... PYTHONPATH=scripts .venv/bin/python scripts/probe_example.py`.

## Quickstart
```python
import sys; sys.path.insert(0, "<this-skill>/scripts")
from bigdata_toolkit import BigdataClient, EntityResolver, AnnotatedSearcher, StructuredDataREST, CostTracker, rc
c = BigdataClient()
nvda = rc(lambda: EntityResolver(c).resolve_id("NVIDIA", country="US"))   # rp_entity_id is the gateway key
rest = StructuredDataREST(c)
est  = rc(lambda: rest.analyst_estimates(nvda, period="quarter", limit=5))
docs = rc(lambda: AnnotatedSearcher(c).search_entity(nvda, keyword="data center", chunk_limit=10))
```
Wrap **every** network call in `rc(lambda: ...)` — a first-handshake `SSL: UNEXPECTED_EOF` is common and the SDK's retry doesn't cover it.

## Routing (capability → method)
- Name/ISIN/CUSIP/SEDOL → `rp_entity_id`: `EntityResolver.resolve_id` / `.resolve_by_isin`.
- Forward consensus / surprise / calendar / ratings / price target: `StructuredDataREST.analyst_estimates` / `.latest_surprise` / `.events_calendar` / `.analyst_ratings` / `.price_target`.
- Statements (income/balance/cash-flow), TTM metrics/ratios, profile, daily prices/dividends, revenue segments: `.income_statement` / `.balance_sheet` / `.cash_flow_statement` / `.key_metrics_ttm` / `.company_ratios_ttm` / `.company_profile` / `.daily_prices` / `.dividends` / `.revenue_geographic_segments` / `.revenue_product_segments`.
- Daily entity-sentiment series: `.entity_sentiment` (don't self-aggregate from chunks).
- Co-mention graph (⚠️ chunk-billed): `.connected_entities`. Universe: `.company_screener`.
- Annotated chunks w/ sentiment + spans: `AnnotatedSearcher.search_entity`. Bulk 50% cheaper: `BatchSearch`.
- Unwrapped endpoint: `client.http.post("v1/<resource>/query", body)`.

`income/balance/cash-flow/daily-prices/dividends/revenue-segments` return `{fields, values}` → `fields_values_to_records()`. `*_ttm` / `company_profile` are flat.

## Two data faces
- **Structured financial** (REST): works for A-shares/Chinese names too via `rp_entity_id` resolved from the **English name or ISIN** (not the Chinese name). The daily `entity_sentiment` series lives here and works for any resolvable entity.
- **Unstructured Chinese NLP** (SDK chunk search): dead end — Chinese entity detection ≈ 0, per-chunk CJK sentiment is a doc-level inherited value, `language` mislabels Chinese filings as English. Pair with a China-domestic source for Chinese chunk content.
Do NOT say "Bigdata fails for A-shares" — state this split precisely.

## Cost discipline
`1 query_unit = 10 chunks`. Only chunk-search is billed; structured `/v1/*` endpoints are free (0 chunks). `connected_entities` + `AnnotatedSearcher` ARE chunk-billed.
1. Use `ChunkLimit(n)`, never a bare `int` (`Search.run(int)` is a document limit billed by the full chunk page — observed ~52x gap once, indicative).
2. Rerank bills only returned chunks — pass `rerank_threshold`.
3. `BatchSearch` is ~50% cheaper ($0.0075 vs $0.015/qu) for large backfills.
Use `CostModel` to veto over-budget jobs; `CostTracker.snapshot()/delta()` to measure spend.

## Known pitfalls (already guarded)
SSL EOF → `rc()`; `All(entity, Keyword(kw))` TypeError → use `&`; the 52x doc-limit trap → `ChunkLimit`; closure capture in loops → bind vars; `analyst_estimates(period="quarter")` 400s above limit≈20; `company_screener` filters must nest under `"filters"` (flat keys silently dropped); `Document.reporting_period` always None → `fetch_reporting_period_raw`.

## Will not do
Never hardcode the API key. Read-only (uploads = NotImplementedError in API-key mode). Never invent an endpoint/schema — confirm paths via `docs.bigdata.com/llms.txt`.
