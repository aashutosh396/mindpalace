---
name: Marketing Context Document
description: Use when capturing brand voice, ICP, positioning, or a style guide at the start of a project — creates the foundational marketing context all other marketing work reads so you never repeat yourself.
tags: [marketing context, brand voice, icp, positioning, target audience, style guide, customer language, personas]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/marketing-context
---

# Marketing Context Document

Capture the foundational positioning, messaging, and brand context every marketing task needs. Store at a canonical path (e.g. `.claude/product-marketing-context.md`) that all marketing skills read. Run this first on any new project.

## Modes
1. **Auto-draft from codebase** — study README, landing pages, copy, about pages, package.json, docs; draft V1; user corrects + fills gaps (fastest, most users prefer).
2. **Guided interview** — walk sections conversationally, one at a time.
3. **Update existing** — read current, summarize, ask what to update.

After a draft: "What needs correcting? What's missing?"

## Sections to capture
1. **Product overview** — one-liner, what it does, category ("shelf"), type (SaaS/marketplace/etc.), business model + pricing.
2. **Target audience** — company type, decision-makers, primary use case, jobs-to-be-done, scenarios.
3. **Personas** — per buying stakeholder (User/Champion/Decision Maker/Financial Buyer/Technical Influencer): what they care about, their challenge, value you promise.
4. **Problems & pain points** — core challenge, why current solutions fall short, what it costs (time/money/opportunity), emotional tension.
5. **Competitive landscape** — direct / secondary / indirect competitors; how each falls short.
6. **Differentiation** — key differentiators, how you solve it differently, why that's better (benefits), why customers choose you.
7. **Objections & anti-personas** — top 3 sales objections + responses; who is NOT a fit.
8. **Switching dynamics (JTBD four forces)** — push, pull, habit, anxiety.
9. **Customer language (verbatim)** — how they describe the problem and solution in their words; words to use / avoid; glossary.
10. **Brand voice** — tone, communication style, 3-5 personality adjectives, voice DOs/DON'Ts.
11. **Style guide** — grammar, capitalization, formatting, preferred terminology.
12. **Proof points** — metrics, logos, verbatim testimonials, value themes + evidence.
13. **Content & SEO context** — target keywords by cluster, internal-links map, 3-5 writing examples, tone/length prefs.
14. **Goals** — primary business goal, key conversion action, current metrics.

## Validation
Score completeness from required + optional section coverage. Below 70 → go back and fill gaps before declaring "done" — sibling skills silently degrade on an incomplete file. Re-run during freshness audits.

## Tips
Be specific ("What's the #1 frustration that brings them to you?") · capture exact words · ask for examples · validate each section before moving on · skip what doesn't apply.

## Proactive flags
Missing customer-language section → ask for 3-5 verbatim quotes. No competitive landscape → ask top 3 alternatives. Brand voice undefined → define 3-5 adjectives. Context older than 6 months → recommend review. No proof points → ask for metrics/logos/testimonials.
