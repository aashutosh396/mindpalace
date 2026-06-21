---
name: content-brief
description: "Use when planning a new article or writing a content brief. Googles the keyword, reads the top 10 results, classifies search intent, maps the content gap, and produces a writer-ready brief with structure, outline, title/meta, schema, and E-E-A-T signals. No keyword tool needed. Triggers: content brief, blog brief, article outline, content plan, brief for keyword, what to write about."
version: 1.0.0
license: MIT
tags: [content-brief, seo, serp-analysis, search-intent, content-outline, content-gap, keyword, writing]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/content-brief
derived_from: awesomeclaude
---

# Content Brief

A writer-ready content brief built from real SERP analysis, not a generic template. Google the keyword, read what actually ranks now, and produce the brief. No keyword-tool exports needed.

## When to use

Planning a new article or page and you need a brief a writer (human or agent) can execute. For improving an existing page, use `improve-content` instead.

## Input

Target keyword (required). Optionally business context for audience/tone. If no keyword given, ask first.

## Steps

1. **Research the SERP** — Google the keyword, read the top 10. For each: content format (listicle / guide / comparison / how-to / tool / video), approx word count, heading structure (H1, main H2s), angle/hook, what they cover that others don't, whether they hold a featured snippet or PAA positions.

2. **Identify intent** — classify Informational / Commercial Investigation / Transactional / Navigational. Length guidance: Informational 1,500–3,000+ (completeness, PAA coverage); Commercial 2,000–4,000 (features, comparison, objectivity); Transactional 800–1,500 (trust signals, CTAs, specs); Navigational 500–1,000 (speed, direct info). Target word count = average of top 5 + 10%. Never pad to hit a number.

3. **Map People Also Ask** — if PAA appears, record questions verbatim; they become H2/H3 headings.

4. **Pick content type** from the SERP pattern (how-to, definition, comparison, listicle, product-review, case-study, pillar-page, faq-page, landing-page, service-page, buying-guide, alternatives-page, etc.).

5. **Produce the brief.**

## Brief structure

- **Target keyword analysis** — primary keyword | apparent difficulty from SERP competition | dominant intent. Difficulty strategy: easy SERP (low-DR, mixed intent) = 3–6 mo; moderate (top all DR 40+, uniform intent) = 6–12 mo; hard (top all DR 60+, long-form) = 12+ mo authority play. Related terms to target on the same page.
- **SERP competitive intelligence** — for top 3: URL | est. words | format | key sections | what they miss.
- **Content gap analysis** — subtopics covered by 2+ top competitors but thin/missing elsewhere. Name exact missing sections, not "add more depth."
- **Recommended outline** — H1 + H2/H3 aligned to intent and gaps. Mark the H2 that hosts the 40–60 word featured-snippet answer. Integrate PAA as headings. Add FAQ section if 3+ PAA questions.
- **Hub & spoke** — is this hub / spoke / standalone; recommended internal linking pattern.
- **Technical optimization** — title tag (50–60 chars, keyword near front); meta description (150–160 chars, intent + CTA); schema (Article / FAQ / HowTo / Product / Review by type); snippet format (paragraph for "what is", ordered list for "how to", table for comparison).
- **E-E-A-T signals required** — author expertise markers, original data/research to include, authoritative sources to cite.
- **Resource assessment** — effort Low (500–1,000w, 2–4h) / Medium (1,000–2,500w, 6–12h) / High (2,500w+, 16h+); realistic 3-month target position.

## What to ignore

- Keyword density targets — write naturally (~2% body is a ceiling, not a target).
- NLP term lists of 50+ words — focus on 5–8 core entities that must appear.
- Word count without checking SERP — padding to hit a number creates weak content.

## Next step

Hand the brief to `write-content` to draft the article.
