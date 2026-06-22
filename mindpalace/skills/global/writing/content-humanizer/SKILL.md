---
name: Content Humanizer
description: Use when content sounds like AI, robotic, generic, full of clichés, or lacks personality — detects AI tells, fixes rhythm and specificity, and injects brand voice.
tags: [humanize, ai-detection, brand-voice, ai-tells, content-editing, rewrite, tone, writing-style, personality, anti-ai]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/content-humanizer
---

Transform machine-sounding content into writing that reads like a real person with real opinions and stakes. Not a cleaning service — rebuild the voice. (For first drafts use content-production; for short conversion copy use copywriting.)

## Three modes (run in sequence or jump in)
1. **Detect** — audit AI tells, score severity, name what's wrong before fixing.
2. **Humanize** — strip patterns, fix rhythm, replace generic with specific.
3. **Voice injection** — apply the brand's specific personality.

## Mode 1: Detect — core AI tell categories
Score 🔴 critical / 🟡 medium / 🟢 minor. Get a 0-100 human-ness score: **80+** light polish · **60-79** targeted removal (Mode 2) · **<60** fingerprint too dense → full rewrite, not a patch.
1. **Filler words** 🔴 — delve, landscape, crucial/vital/pivotal, leverage, furthermore/moreover, navigate, robust/comprehensive/holistic, foster/facilitate/ensure.
2. **Hedging chains** 🔴 — "It's important to note," "It's worth mentioning," "One might argue," "In many cases," "Needless to say."
3. **Em-dash overuse** 🟡 — compulsive clause-adding.
4. **Identical paragraph structure** 🔴 — every para: topic→explanation→example→bridge.
5. **Lack of specificity** 🔴 — "many companies," "studies show," "significantly," "leading brands," "a lot of."
6. **False certainty** 🟡 — confident claims about uncertain things.
7. **"In conclusion" paragraph** 🟡 — a carbon copy of the intro.
(Tell vocabulary is a moving target — newer models have different tells; refresh the list.)

## Mode 2: Humanize
- **Replace fillers** (never just delete): delve into→dig into/break down · leverage→use/apply · crucial→state the thing · robust→specific ("handles 10k req/sec") · facilitate→help · navigate this challenge→deal with this.
- **Fix rhythm** — break uniform 18-22 word sentences. Read aloud. Pattern: Long. Short. Long, long. Short. Use fragments for emphasis. Question? Answer. Proof.
- **Generic→specific** — replace vague claims with named source + dated data + specific number; if you lack data, be honest ("In my experience…"). Personal experience beats vague authority.
- **Vary paragraph structure** — single-sentence paras, question paras, mid-list, asides/parentheticals, confessions ("I got this wrong the first time").
- **Add friction/imperfection** — change direction mid-thought, qualify uncertainty, take opinions, react.

## Mode 3: Voice injection
Read the brand voice blueprint first (or ask for ONE example of writing they love; extract sentence length, formality, humor, relationship stance, signature phrases). Techniques: personal anecdotes · direct "you" address · opinions without apology (take a side) · the knowing aside · consistent rhythm signature.

## Proactive flags
10+ tells per 500 words → full rewrite, not edit · no voice context → ask for one example before injecting · 5+ vague claims with no data → user must supply proof · post-humanize tone mismatches the brand's other content · don't destroy the 1-2 genuinely good paragraphs buried in the mush.

When auditing: name the pattern → why it reads as AI → the specific fix (not "this sounds robotic" but "para 4 opens with a pure hedge — cut it, start with the actual note").
