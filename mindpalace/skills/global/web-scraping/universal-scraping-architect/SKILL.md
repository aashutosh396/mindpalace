---
name: Universal Scraping Architect
description: Use when scraping a site, crawling docs, extracting from PDFs/Excel/HTML, or building a validation-heavy data-extraction pipeline — routes between API (Firecrawl) and local Python, with budgets, checkpointing, and validation.
tags: [web-scraping, crawling, firecrawl, beautifulsoup, data-extraction, pipeline, pagination, validation, pdf-extraction]
source: alirezarezvani/claude-skills
derived_from: engineering/universal-scraping-architect
---

# Universal Scraping Architect

Design complete, robust data-extraction pipelines with intelligent routing, validation, and token-budget tracking — not brittle one-off scripts.

**Before starting:** read `project-context.md` if it exists. Determine target data format, scale of extraction, and deployment environment before writing code. API keys load only via env vars (BYOK) — never hardcode.

## Three extraction modes (route explicitly)

- **Mode 1 — API-driven (Firecrawl):** public URL, heavily dynamic (JS/SPA), search-first discovery, or bulk crawl across a domain.
- **Mode 2 — Local Python (bs4/pandas):** local files (PDF/Excel/CSV), private/sensitive data, or a simple static HTML page where Firecrawl is overkill.
- **Mode 3 — Hybrid:** Firecrawl handles discovery/web extraction; local Python (Pandas) cleans, normalizes, and structures before saving.

## The extraction pipeline (always in order)

1. **Route the approach** — state explicitly whether Firecrawl or local Python, and why.
2. **Track budgets** — estimate Firecrawl quota / LLM token context limits before large jobs.
3. **Extract safely** — checkpoint multi-page jobs; handle pagination and dynamic layouts. Run any runner template with a `--sample` / offline mode first to confirm the expected output shape before going live.
4. **Validate & clean** — structurally validate every result before delivering: exit OK only on well-formed, non-empty output; empty or malformed → fix and re-extract, never ship unvalidated data. Also check required fields and duplicates against the spec.
5. **Format** — CSV for tabular, JSON for nested, Markdown for clean text (chunk for LLM token limits).

## Proactive triggers (flag without being asked)
- **Hardcoded API keys** → rewrite to `os.getenv('FIRECRAWL_API_KEY')`.
- **Private-data leakage** → asking to send local sensitive files to an external API? Flag the privacy risk, suggest Mode 2.
- **Missing pagination** → target implies hundreds of records but no pagination/checkpoint logic? Add it.

## Anti-patterns
- Brittle selectors (`div > span > ul > li:nth-child(3)`) — use data attributes or robust structural anchors.
- Ignoring etiquette — always check `robots.txt`, implement sensible rate limits.
- No validation — never write scraped data without checking for empty arrays or missing critical keys.
