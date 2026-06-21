---
name: keyword-deep-dive
description: "Use when deciding whether and how to rank for a specific keyword. Googles it, reads the top 10 (top 3 in full), classifies intent, assesses SERP features and zero-click risk, reads competitor pages, and produces a 90-day ranking plan with difficulty, gaps, title/meta rewrites, and a realistic timeline. No keyword tool required. Triggers: keyword research, should I target this keyword, ranking plan, keyword opportunity, SERP analysis, keyword difficulty, can I rank for."
version: 1.0.0
license: MIT
tags: [keyword-research, seo, serp-analysis, search-intent, ranking-plan, competitive-analysis, zero-click, strategy]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/keyword-deep-dive
derived_from: awesomeclaude
---

# Keyword Deep Dive

A complete picture of one keyword's opportunity — intent, competition, what it takes to rank, and a specific 90-day plan. The agent does all research itself; no keyword tool needed.

## When to use

Evaluating a single keyword before committing content effort to it. For the full writer brief afterward, use `content-brief`.

## Input

Target keyword (required). Optionally a URL if you already have a page targeting it. If no keyword, ask first.

## Steps

1. **Research the SERP** — Google the keyword, read top 10 (top 3 in full). For each top-3: domain (brand vs specialist vs generalist authority proxy), format, approx words, unique angle, freshness signals, E-E-A-T signals.

2. **Classify intent** — Informational / Commercial Investigation / Transactional / Navigational. Zero-click risk: ~60% of informational searches end without a click (mobile reaches ~77%); featured snippet present = ~42.9% CTR if held, near-zero if not; AI Overview present drops organic CTR ~58–61% for the top page, but cited brands earn ~35% more clicks. Flag structurally low-CTR keywords.

3. **Assess SERP features** — featured snippet (format + holder), People Also Ask (count + questions), AI Overview, image/video carousel, local pack, sitelinks, knowledge panel.

4. **SERP volatility signal** — freshly updated top results / "Updated YYYY" titles = moderate volatility; results spread across years = stable; all dated past 6 months with news angles = turbulent; can't tell = say so, don't fabricate.

5. **Competitive read of top 3** — fetch and read each: key sections, word count, internal linking patterns, what they cover that others don't, what's genuinely hard to replicate (original data, first-party screenshots, proprietary frameworks).

## Output

- **Keyword profile** — keyword | apparent intent | estimated difficulty (Easy / Moderate / Hard from SERP, not a KD score); SERP features and CTR impact; zero-click risk Low/Medium/High.
- **Competitive read** — per top-3: URL | authority proxy | format | approx words | unique angle | what they do best.
- **Content gaps** — specific subtopics/angles top pages don't cover well — where a new entrant differentiates.
- **Ranking strategy** — if no existing page: worth pursuing? realistic timeline (Easy 3–6 mo / Moderate 6–12 / Hard 12–24 authority play); content type, word-count target (top-5 avg +10%), must-cover sections, unique angle, E-E-A-T signals. If existing page: position diagnosis vs top 3, plus quick wins, 30-day content plan, supporting cluster pages.
- **Title tag & meta rewrites** — 2 title options (≤60 chars) + 1 meta (≤160 chars), each with reasoning.
- **Ranking timeline** — current position (or "unranked") → realistic 90-day target; effort Low (CTR fix) / Medium (content update) / High (new content + links).

## What to ignore

- KD scores alone — meaningless without reading the actual SERP.
- High-volume zero-click keywords — impressions without clicks rarely worth it unless you need brand exposure.
- Fighting Wikipedia/Reddit/news aggregators for positions 1–3 — usually unwinnable.

## Next step

Use `content-brief` with this keyword to produce the writer-ready brief.
