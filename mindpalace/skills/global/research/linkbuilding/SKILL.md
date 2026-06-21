---
name: linkbuilding
description: "Use when planning link acquisition or a backlink strategy. Classifies the site's authority phase (Foundation / Growth / Authority) from site age and visible signals, then recommends phase-appropriate tactics plus anchor-text safety ranges and link-velocity guidelines. No backlink tool required. Triggers: link building, backlinks, get backlinks, link strategy, outreach, guest posting, anchor text, referring domains, link velocity, DR, domain authority."
version: 1.0.0
license: MIT
tags: [link-building, backlinks, seo, outreach, anchor-text, domain-authority, off-page, strategy]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/linkbuilding
derived_from: awesomeclaude
---

# Link Building

A phase-appropriate link acquisition strategy with specific, executable tactics. The agent classifies your site's authority phase from what it can read (domain, site age, homepage), then recommends matching tactics.

## When to use

Planning how to earn backlinks, or diagnosing whether your link profile is safe.

## Input

Your domain or a URL (required). Optionally niche, what you sell, and constraints ("no budget for outreach", "already tried guest posting"). If the user names an action, adapt: "find easy opportunities" → low-effort/high-conversion (existing relationships, testimonials, citations, entity stacking); "help with outreach" → guest posting + resource pages with search operators and pitch angles; "create link-worthy content" → skyscraper + statistics pages; "full strategy" → run the whole workflow.

## Step 1: Phase assessment

Fetch the homepage, Google the brand. Check site age (WHOIS / first Wayback snapshot), content volume (`site:domain.com`), brand presence (knowledge panel? company card? news?), apparent size. Classify:
- **Foundation**: new (<1 yr), thin content, no brand signals, ~DR 0–15.
- **Growth**: 1–3 yrs, 20–100 pages, some brand mentions, ~DR 16–40.
- **Authority**: 3+ yrs, established brand, knowledge panel, media mentions, ~DR 41+.

State your reasoning. If ambiguous, ask the user rather than guess.

## Step 2: Phase-appropriate tactics

**Foundation (do first):**
- **Entity stacking** — consistent brand presence on 20+ platforms (Google Business, LinkedIn, Crunchbase, Medium, GitHub, Wikidata). ~20–30 referring domains month 1; Wikidata is highest-leverage for entity recognition.
- **Citations & directories** — industry/local directories; Chamber of Commerce links are DR 50–70 dofollow.

**Growth (next):**
- **Competitor backlink gap** (needs a backlink tool) — domains linking to 2+ competitors but not you convert ~3x better than cold targets.
- **Guest posting** — DR 30+ sites with real traffic; contextual in-article links worth 5–10x bio links.
- **Resource pages** — search `intitle:resources [niche]`; university pages (DR 70–90+) are gold; pitch as gap-filler.
- **Skyscraper** — find the most-linked content in your niche, make something 10x better, reach out to everyone who linked the original.

**Authority (scale):**
- **Strategic partnerships** — joint research, co-authored guides, integration pages (permanent, high-authority links).
- **Podcast guesting** — target shows with 1,000–10,000 listeners (the sweet spot); show-notes host links are dofollow and high-authority.

## Step 3: Anchor text safety

If the user can share anchor distribution, compare to safe ranges: branded 40–50%; naked URL 15–20%; generic ("click here") 15–20%; partial match 10–15%; exact match 3–5% MAX (over 5% = penalty risk). If exact > 5%, recommend branded/generic anchors for the next 10–15 links before outreach. Skip if no data.

## Step 4: Output

- **Authority phase assessment** with reasoning.
- **Top 3 recommended tactics** matched to phase — each with why it fits, expected referring domains, time investment, specific first action.
- **Link velocity guidelines** — Month 1: 15–25 foundation links; Months 2–3: 5–10 quality; Months 4–6: 8–15; Month 7+: 10–30. Red flags: 50+ in one month, all same country, exact-match anchor spike.

## What to ignore

- Link farms, PBNs, link exchanges — SpamBrain detects these.
- Sites with no real traffic regardless of DR — prioritize relevance + traffic.
- Mass directory submissions — quality directories only.
