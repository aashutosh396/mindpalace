---
name: Answer Engine Optimization (AEO)
description: Use when optimizing content to be cited by AI engines (ChatGPT, Perplexity, Claude, Gemini, Mistral), auditing E-E-A-T, tracking LLM citations, or building AI-search content strategy — distinct from click-through SEO.
tags: [aeo, answer-engine-optimization, e-e-a-t, llm-citation, chatgpt, perplexity, ai-search, structured-data, generative-engine-optimization, citation-tracking]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/aeo (ported from alirezarezvani/aeo-box)
---

Optimize content for **citation** in LLM-generated responses — distinct from SEO (which optimizes for rankings). Audit, optimize, track.

## AEO vs SEO
| | SEO | AEO |
|---|---|---|
| Optimizes for | Click-through rankings | Being cited as authoritative source |
| Audience | Humans browsing results | LLMs answering questions |
| Success metric | Position 1-10, traffic | Citation count across LLMs |
| Key signals | Backlinks, keywords, speed | E-E-A-T, structured data, factual density |
They're complements — AEO citations often come from sources that already rank well.

## When NOT to use
Pure click-through SEO (use seo-audit) · brand content with no factual claims (nothing to cite) · topics LLMs already know well (elementary math) · breaking news (training lag delays citations months).

## Workflow
0. **Pre-flight: bot access** — check robots.txt against the AI-crawler matrix; a blocked GPTBot/PerplexityBot/ClaudeBot/Google-Extended zeroes that platform and is always the first fix.
1. **Audit** existing content → composite score 0-100 + 4-dimension breakdown.
2. **Optimize** → variant with citations + schema + structural fixes.
3. **Publish + track** citations in a local ledger.
4. **Report** per-page citation stats (count, LLMs, queries, velocity).

## E-E-A-T scoring (4 dimensions)
- **Experience** — first-person evidence, dated examples, case studies.
- **Expertise** — author bio + credentials, peer-reviewed citations, technical depth.
- **Authoritativeness** — backlinks from authority domains, schema.org markup.
- **Trustworthiness** — HTTPS, contact info, corrections policy, factual density (verifiable claims per 1000 words).

## Optimization modes
conservative (touch <10% words) · balanced (<30%) · aggressive (max AEO rewrite). Structure rewrite (H2/H3 for LLM parsing) · citation density boost ([1]-style refs) · schema injection (FAQ/HowTo/Article JSON-LD) · fact-first lede (verifiable claims in first 200 words).

## Industry E-E-A-T thresholds (min composite)
Healthcare/Finance/Legal 85 (need medical/CFA/jurisdiction byline + disclaimers + primary citations) · Education 75 · SaaS/B2B/Media 70 · E-commerce 65.

## Anti-patterns rejected
Keyword stuffing for AI (LLMs extract topic semantically) · pure AI content with no human review (RAG de-prioritizes generic output) · citation farms / link wheels · schema spam (unverifiable claims get filtered) · per-LLM hacks (citation distributions are highly correlated — optimize shared E-E-A-T signals) · ignoring SEO entirely.

Storage is local-first (citation ledger, patterns, saved audits) — no telemetry, no cloud sync.
