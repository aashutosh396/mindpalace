---
name: avoid-ai-writing
description: "Use when asked to remove AI-isms, clean up AI writing, humanize text, edit/audit writing for AI patterns or tells, make this sound less like AI, strip em dashes, or cut words like delve/leverage/robust/seamless from a draft."
version: 1.0.0
license: MIT
tags: [writing, editing, humanize, ai-detection, voice, prose, copyediting, style]
source: https://github.com/conorbronsdon/avoid-ai-writing
derived_from: awesomeclaude
---

# Avoid AI Writing — audit & rewrite

Edit content to remove AI writing patterns ("AI-isms") that make text read as machine-generated.

These patterns are statistically more common in LLM output, but humans on deadline, in unfamiliar genres, or writing in a second language produce the same shapes. Treat flags as signals, not proof. Do not use them as the sole basis for a consequential call (academic integrity, hiring). Worth acting on; not worth ruining someone's day over.

## Modes

- **rewrite** (default) — flag AI-isms and return a clean rewrite.
- **detect** — flag only, no rewriting. Triggers: "detect," "flag only," "audit only," "just scan," "what AI patterns are in this." Use when the writer wants to decide fixes themselves, the patterns may be intentional, or the text is published/someone else's.
- **edit** — edit a file in place (writer names a file: "clean up `draft.md`"). Make minimal, targeted Edit-tool changes to flagged spans only; leave already-human passages untouched. Do not edit quoted material, code blocks, or text attributed to others — flag those instead. Re-read after to confirm.

Optional knobs: voice (casual / professional / technical / warm / blunt), context profile (linkedin / blog / technical-blog / investor-email / docs / casual), iterate N (cap N=2 — rewrite mode already runs one corrective second pass).

## What to remove or fix

Formatting:
- **Em dashes (— and --)**: replace with commas/periods/parentheses or split sentences. Target zero; hard max one per 1,000 words. Applies to headings too.
- **Bold overuse**: at most one bolded phrase per major section; restructure to lead with what's important.
- **Emoji in headers**: remove. (Social posts may use 1-2 at end of line.)
- **Excessive bullet lists**: convert to prose unless content is genuinely list-like (steps, params, comparisons).
- **Curly quotes**: weak signal only; replace with straight quotes in plain-text/code, leave in finished publications.
- **Title-case headings**: use sentence case for subheads.

Sentence structure:
- "It's not X — it's Y" → direct positive statement.
- Hollow intensifiers (genuine, truly, real, "to be honest," "let's be clear," "it's worth noting that") → cut.
- Vague endorsement ("worth reading/a look/exploring") → say *why* it matters.
- Hedging (perhaps, could potentially, "it's important to note") → state the point.
- Compulsive rule of three → vary groupings; max one triad per piece.
- Copula avoidance (serves as, features, boasts, presents, represents) → default to "is"/"has."
- Synonym cycling (developers… engineers… practitioners…) → repeat the clearest word.

Words to replace (match inflected forms — `-ly`, `-ing`, plurals, conjugations):
- **Tier 1, always replace**: delve, landscape (metaphor), tapestry, realm, paradigm, embark, beacon, testament to, robust, comprehensive, cutting-edge, leverage (v), pivotal, underscores, meticulous, seamless, game-changer, utilize, nestled, vibrant, thriving, showcasing, deep dive, unpack, intricate, ever-evolving, daunting, holistic, actionable, impactful, learnings, thought leader, best practices, "at its core," synergy, interplay, "in order to," "due to the fact that," commence, ascertain, endeavor, embrace (metaphor). Replace with the plain word (use, important, strong, thorough, etc.).
- **Tier 2, flag when 2+ in one paragraph**: harness, navigate, foster, elevate, unleash, streamline, empower, bolster, spearhead, resonate, revolutionize, facilitate, underpin, nuanced, crucial, multifaceted, ecosystem (metaphor), myriad, plethora, encompass, catalyze, reimagine, augment, cultivate, illuminate, elucidate, cornerstone, paramount, poised, burgeoning, nascent, quintessential, overarching.
- **Tier 3, flag only at high density (~3%+)**: significant, innovative, effective, dynamic, scalable, compelling, unprecedented, exceptional, remarkable, sophisticated, instrumental, world-class / state-of-the-art / best-in-class. Replace with specifics: numbers, comparisons, examples.

Template / transition phrases:
- Slot-fill ("a [adj] step towards [adj] AI infrastructure," "Whether you're X or Y," "I recently had the pleasure of") → name the specific thing or pick the real audience.
- Transitions (Moreover, Furthermore, Additionally, "In today's X," "When it comes to," "At the end of the day," "That said," "In conclusion") → restructure so the connection is obvious, or cut.
- Reader-steering ("Here's what's interesting," "Here's what stood out") → let the content signal importance.

Significance & prediction inflation:
- Inflated routine events ("marking a pivotal moment," "watershed moment") → state what happened; if it works after deleting the clause, delete it.
- Generic future closers ("may become one of the most important narratives of the next cycle," "poised to become the next chapter") → make it falsifiable or cut.
- Hedge-stacked predictions ("could potentially," "may eventually unlock") → pick one word.
- Real/actual adjective inflation ("real on-chain tokenomics," "genuine utility") → drop the adjective and add the specific claim. Carve-out: keep if the contrast is named ("actual revenue, not grants").

Other tells:
- Vague attributions ("Experts believe," "Studies show") → cite a source or state the claim directly.
- Filler ("It is important to note that," "In terms of," "The reality is that") → cut.
- Generic conclusions ("The future looks bright," "Only time will tell") → cut or make specific.
- Chatbot artifacts ("I hope this helps!," "Great question!," "Let's dive in," "In this article we will explore") → remove.
- "Let's + verb" used as a transition → start with the point.
- Promotional / tourism-brochure prose → plain description.
- "Despite challenges, X continues to thrive" → name the challenge and response or cut.
- False ranges ("from the Big Bang to dark matter") → list the actual topics.
- Rhetorical-question openers, parenthetical hedging, numbered-list inflation ("Five things to know"), emotional flatline ("What surprised me most"), self-labeling significance ("that's the contrarian move"), sycophancy, acknowledgment loops, reasoning-chain artifacts ("Let me think step by step") → cut the scaffolding, state the substance.
- Inline-header lists ("**Performance:** Performance improved…") and list-label periods (`**Intros.**` where a human writes `**Intros:**`) → fix the markup or write as prose.

Fingerprints (near-proof, strip mechanically — catch even when the rest reads fine):
- Citation markup leaks: `citeturn0search0`, `contentReference[oaicite:0]`, `oai_citation`, `[attached_file:1]`.
- AI-tool URL params: `utm_source=chatgpt.com`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`.
- Unfilled placeholders: `[Your Name]`, `[INSERT SOURCE URL]`, `2025-XX-XX`, `<!-- add citation -->`.
- Cutoff disclaimers ("As of my last update," "I don't have access to real-time data").

Rhythm & structure (the #1 detection signal — fix this even after fixing every word):
- Sentence-length uniformity (most 15-25 words) → mix short (3-8) with long (20+); fragments and questions break monotony.
- Paragraph-length uniformity → vary deliberately; some one-sentence paragraphs.
- Excessive structure: >3 headings in <300 words, or 8+ bullets in <200 words → merge / convert to prose.
- Paragraph-reshuffle test: if you can swap two body paragraphs without breaking the piece, it's a list of points, not an argument — add a through-line.
- Treadmill effect: if you can cut 40-60% with no information loss, each paragraph is restating, not advancing.
- Type-token ratio: general prose 200+ words usually 0.50-0.65; under ~0.40 is worth a look. Fix by naming concrete things, not by thesaurus.
- Do NOT over-polish: sanding away every irregularity pushes text *toward* AI statistical profiles. Keep natural disfluency and personality.

When to rewrite from scratch: 5+ vocab hits across categories + 3+ distinct pattern categories + uniform length → the structure is AI-generated; patching won't help. State the core point in one sentence and rebuild.

## Severity tiers (for quick passes / triage)

- **P0, fix immediately**: cutoff disclaimers, chatbot artifacts, vague attributions, significance inflation, hashtag stuffing on linkedin/investor-email.
- **P1, fix before publishing**: word-list violations, template phrases, "Let's" openers, synonym cycling, formulaic openings, bold overuse, em dashes above threshold, future-narrative closers, social endorsement closers, hedge-stacked predictions, real/actual inflation, Tier-3 phrase clustering.
- **P2, polish when time allows**: generic conclusions, rule of three, uniform paragraph length, copula avoidance, transition phrases.

Quick pass = P0+P1. Full audit = all three tiers.

## Context profiles (rule strictness by audience)

Auto-detect if unspecified: short + hashtags → linkedin; code blocks/APIs → technical-blog; salutation + fundraising → investor-email; steps/params/README → docs; else → blog (safest, all rules full strength). Roughly: linkedin relaxes em dashes/bold/bullets/transitions; technical-blog gives technical terms a pass (keeps robust/comprehensive/seamless/ecosystem/leverage/facilitate but still flags delve/tapestry/game-changer); investor-email is extra strict on promotion/significance; docs prioritizes clarity over voice; casual catches only the worst offenders. Say which profile you used if auto-detecting.

## Voice profiles (how prose should sound — optional, independent of context)

- **casual**: contractions, short sentences (≤14 words avg), first-person touch, near-zero jargon.
- **professional**: active voice, varied length, one concrete claim per paragraph, explicit ask.
- **technical**: plain copulatives ("X is Y"), one idea per sentence, define jargon on first use.
- **warm**: address reader as "you," stronger verbs over intensifiers, no performative empathy.
- **blunt**: lead with the claim, periods over em dashes, near-zero hedging, short declaratives.

If the writer gives a sample, match its sentence-length pattern, contraction rate, and word choices instead of a named profile — don't "upgrade" their vocabulary. Where voice and context disagree on a rule, resolve toward the stricter.

## Self-reference escape hatch

When writing *about* AI patterns (this kind of doc, tutorials), quoted examples, code blocks, and text marked illustrative ("for example, AI might write…") are exempt. Only flag patterns in the author's own prose.

## Output

- **rewrite**: (1) Issues found (quote offending text), (2) Rewritten version (preserve structure/intent/technical details), (3) What changed, (4) Second-pass audit (re-read your rewrite, fix survivors).
- **detect**: (1) Issues found grouped by P0/P1/P2, (2) Assessment — clear problem vs. judgment call.
- **edit**: (1) Edits made (location, before → after), (2) Verification (re-read confirmed; note what you left alone).

Goal: writing that sounds like a person wrote it. The replacement words are defaults, not mandates — keep a flagged word if it's clearly right in context. If the original is already strong, say so and make only necessary cuts.
