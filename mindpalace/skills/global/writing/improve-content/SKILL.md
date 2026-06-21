---
name: improve-content
description: "Use when rewriting or refreshing an existing page that underperforms. Fetches the URL, analyzes current content, does a lightweight SERP check, runs a short update interview, and rewrites using the full anti-AI-slop ruleset. No data exports needed. Triggers: improve this page, rewrite this article, refresh content, update old post, content refresh, why isn't this page ranking, make this better."
version: 1.0.0
license: MIT
tags: [content, rewrite, refresh, seo, anti-ai-slop, content-update, editing, optimization]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/improve-content
derived_from: awesomeclaude
---

# Improve Content

Rewrites an existing page so it outranks competitors — better structure, deeper expertise, human voice. Same anti-slop ruleset as `write-content`.

## When to use

Refreshing or rewriting a published page. For a brand-new piece, use `write-content`.

## Input

URL of the page to improve. If the fetch fails, ask the user to paste the content.

## Steps

1. **Read current content** — fetch and read the rendered page. Note title, meta, H1/H2s, word count, internal links, schema. Identify the apparent primary keyword.

2. **Research the SERP** (lightweight) — Google the primary keyword, read top 5. Note ranking formats, gaps where this page falls short, angles competitors take that this doesn't, snippet/PAA opportunities. Just enough to know what's missing.

3. **Update interview** — ask 2–3, one at a time: "What's changed since you published — new data, experience, market shifts?" / "What results did this get — traffic, leads, feedback?" / "Knowing what you know now, what would you add or cut?"

4. **Rewrite** — produce the complete rewritten article in clean markdown applying ALL the rules below.

## Rewrite rules

**Voice**: practitioner to a peer. Take positions. Use "you" and "I/we". Specific numbers, names, dates. Contractions. Show thinking changing. Shift registers — uniform register is an AI tell.

**Rhythm**: vary sentence length (5 to 30+ words) and paragraph length. Fragments. Parenthetical asides. Break the topic-sentence-support pattern. Cover sections asymmetrically. No section summaries.

**Show, don't state**: brief scenarios over flat claims.

**Anti-slop — NEVER use**: delve, landscape (metaphorical), testament, leverage, utilize, robust, seamless, furthermore, moreover, additionally, pivotal, multifaceted, harness, embark, navigate (metaphorical), showcase, streamline, paramount, culminate, spearhead, commence, endeavor, vibrant, innovative, comprehensive (adj). NEVER: "It's worth noting", "In today's [anything]", "Let's dive in", "In conclusion", "plays a crucial/vital role", "It goes without saying". Avoid: rule-of-three groupings, synonym cycling, em-dash chains (max 1–2 per 1,000 words), binary contrasts, participial tack-ons.

**SEO**: primary keyword in H1, first 100 words, 2–3 H2s (~2% density, natural). 40–60 word direct answer after the most important H2 (featured snippet). Weave PAA as H2/H3. 3–5 internal links per 1,000 words. Front-load value.

**Content type**: detect from existing page + SERP. How-to → 40–60 word quick answer then numbered steps with "what goes wrong"; comparison → verdict first; definition → "[Term] is..." first sentence; case study → result number first then story.

**Final checks**: (1) "So what?" test per section — inject specifics if anyone could have written it. (2) Self-scan for blacklisted words, topic-sentence patterns, section summaries. Fix before delivering.

**Output**: clean markdown, title + rewritten article. Write in the same language as the existing page.
