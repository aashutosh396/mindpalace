---
name: write-content
description: "Use when writing a complete SEO article or any long-form content that must not sound AI-generated. Includes the full anti-AI-slop ruleset (banned vocabulary, banned phrases, banned structural patterns) plus voice and rhythm rules that read like a practitioner. Researches the SERP itself if no brief is provided. Triggers: write an article, write a blog post, draft content, write this section, make it sound human, anti AI slop, SEO writing."
version: 1.0.0
license: MIT
tags: [writing, content, anti-ai-slop, seo, copywriting, voice, blog, article, human-writing]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/write-content
derived_from: awesomeclaude
---

# Write Content

Writes a complete article in four phases: research → content-type decision → knowledge extraction → write. The value is the anti-slop ruleset and voice rules that stop the draft sounding like a press release.

## When to use

Drafting any long-form piece where it must read human and rank. The banned-word/phrase/pattern list below is reusable for editing ANY writing, not just SEO.

## Input

Topic or keyword (required). Optionally an existing content brief (skip research) or expert-interview output. If no topic, ask first.

## Business context (persist, don't re-ask)

On first use ask 4–5 questions and save the answers to a persistent location, confirming the path with the user first: Claude Code → `~/.claude/projects/<path>/memory/business-context.md` (do NOT append to `./CLAUDE.md` unasked); Cursor → `.cursor/rules/business-context.md`; else `seo-context.md` in the working dir. Load it on every later use. Questions: what the business does and for whom; brand tone (Professional / Casual / Technical / Authoritative / Conversational); language; topics that must NEVER appear; 2–3 main competitors.

## Phase 1: Research

If no brief provided, Google the topic, read top 5, note formats/angles/gaps as 3–5 bullets. Skip if a brief or prior context already has SERP analysis.

## Phase 2: Content type decision

Pick from what ranks (how-to, definition, comparison, listicle, product review, case study, pillar guide, FAQ, landing page, service page, news/trend). State it and wait for confirmation: "The top results for [keyword] are all [format]. I'll write a [type] with [key element]. Sound good?"

## Phase 3: Knowledge extraction

Ask 2–3 quick questions, one at a time, to extract first-party knowledge: "What do most people get wrong about [topic]?" / "A specific example — a client, project, number?" / "What surprised you when you actually did this?" / "Who should NOT follow this advice?"

## Phase 4: Write

**Length**: match the depth of top-ranking content. Never target a number or pad.

**Voice & stance**: practitioner to a peer, not a textbook. Take positions. Use "you" and "I/we". Specific numbers, names, dates — never "many companies". Weave interview answers as first-person. Contractions. Show thinking changing ("At first I thought X — turns out it was Y").

**Rhythm & structure**: vary sentence length dramatically (5-word punches to 30-word complexes); vary paragraph length; use fragments and start with "And"/"But" when natural; parenthetical asides; shift registers; break the topic-sentence-support pattern; cover sections asymmetrically; don't summarize section ends unless genuinely complex.

**Show, don't state**: narrate moments instead of flat claims. "Page speed affects rankings" → "You click a result. Three seconds pass. Still loading. You hit back."

**Anti-slop — NEVER use these words**: delve, landscape (metaphorical), testament, leverage, utilize, robust, seamless, furthermore, moreover, additionally, pivotal, multifaceted, harness, embark, navigate (metaphorical), showcase, streamline, paramount, culminate, spearhead, commence, endeavor, vibrant, innovative, comprehensive (as adjective).

**NEVER use these phrases**: "It's worth noting", "In today's [anything]", "Let's dive in", "In conclusion", "plays a crucial/vital/pivotal role", "It goes without saying", "In the realm of".

**Avoid these patterns**: rule-of-three groupings (use 2 or 4); synonym cycling (repeat the right word); copula avoidance ("serves as" → "is"); em-dash chains (max 1–2 per 1,000 words); binary contrasts ("it's not X, it's Y"); participial tack-ons ("...highlighting the importance of X"); clustering of however/notably/essentially/that said/arguably (3+ flags AI).

**Content-type structure**: how-to → 40–60 word answer first, then numbered steps each with "what goes wrong"; comparison → verdict first; listicle → summary table above fold + consistent eval framework; definition → "[Term] is..." first sentence; case study → result number first, then story; service/landing → PAS (pain, agitate, solve).

**SEO**: primary keyword in title, H1, first 100 words, 2–3 H2s (~2% density, natural); 40–60 word direct answer after the most important H2 for featured snippets; weave 2–3 PAA as headings; 3–5 internal links per 1,000 words with descriptive anchors; front-load value.

**Long articles (1,500+)**: write section by section to avoid repetition; at least 30% must contain details no generic AI could produce (user's data, examples, opinions, experience).

**Final checks**: (1) "So what?" test per section — could anyone have written this for anyone? If yes, inject specifics. (2) Self-check for blacklisted words, topic-sentence runs, needless summaries, participial tack-ons. Fix before delivering.

**Output**: clean markdown, title + article only. Write in the business-context language, else match the user's messages.
