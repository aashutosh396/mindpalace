---
name: semantic-gap-analysis
description: "Use when a page ranks for a keyword but isn't in the top 3 and you want to know exactly what's missing. Compares the page to top-ranking competitors and produces a specific list of entities, subtopics, predicates, and Entity-Attribute-Value relationships to add. Triggers: semantic gap, what's my page missing, entity coverage, topical depth, content gap analysis, why am I stuck at position 5, semantic SEO, NLP coverage."
version: 1.0.0
license: MIT
tags: [semantic-seo, content-gap, entities, topical-authority, nlp, eav, on-page, competitive-analysis]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/semantic-gap-analysis
derived_from: awesomeclaude
---

# Semantic Gap Analysis

Identifies the exact entities, subtopics, predicates, and relationships missing from your page but present in top-ranking competitors. This is the content brief for what to add — not a generic "write more depth."

Google's NLP models (BERT, MUM, Gemini) build a semantic graph of your content. Missing nodes/edges that competitors have make your page read shallow to the algorithm. This finds the exact missing nodes.

## When to use

A page already ranks but is stuck outside the top 3 for a known keyword.

## Input

URL of your page (required) and the target keyword (required).

## Steps

1. **Read your page** — extract main topic and sub-topics; all named entities (people, places, products, concepts, dates, orgs); all predicates (verbs that signal depth — for "coffee brewing": grind, extract, bloom, tamp); H2/H3 hierarchy; what it explicitly covers vs implicitly assumes.

2. **Read the top 3 competitors** — Google the keyword, fetch top 3 in full. Extract entities/predicates/structure the same way. Note what they cover that you don't and the depth (single mention vs full section).

3. **Build the semantic inventory** — three lists side by side: what your page covers | what competitors cover but you don't | unique to your page. Be specific: not "pricing models" but "three-tier vs usage-based pricing with examples from Stripe and Twilio."

4. **Classify the gaps** — Core (all 3 cover, you don't — critical); Differentiator (1–2 cover and it's working — worth adding); Commodity (everyone covers superficially — brief or skip); Opportunity (competitors skip — you could own it).

5. **Map entity relationships** — for core gaps, identify Entity-Attribute-Value triples. Example for "espresso machine reviews": Entity = La Marzocco Linea Mini; Attribute = brew pressure, boiler type, price; Relation = competes with Rocket Appartamento, used by third-wave cafes. This is the density competitors implicitly encode.

## Output

- **Semantic fingerprint** — one sentence on what your page "talks about" to an NLP model vs what it should.
- **Your page** — entities and predicates present.
- **Competitor coverage** — what each top-3 covers that yours doesn't, with why.
- **Gap list** — table: Gap | Importance (Core/Differentiator/Commodity/Opportunity) | Add to section | Depth (paragraph/subsection/full section).
- **Entity relationships to encode** — the EAV triples that should appear, even in passing.
- **Unique angle to preserve** — what your page does well; don't lose it when adding depth.
- **Content addition plan** — sections to add/expand in priority order, each with heading, 2–3 sentence description, estimated word count.

## What to ignore

- Keyword density for related terms — cover the entities, don't force variants.
- Fluff additions — every added section must carry real information.
- Wikipedia-style completeness — cover enough that an NLP model recognizes topic depth, not everything.

## Next step

Turn the addition plan into a rewrite with `improve-content` (paste the gap list as context).
