---
name: Free Tool Strategy (Engineering as Marketing)
description: Use when building a free marketing tool — calculator, generator, checker, grader — for lead gen, SEO, or backlinks. Covers idea evaluation, tool design, lead capture, and launch.
tags: [free tool, engineering as marketing, calculator, generator, lead gen tool, seo, backlinks, interactive tool]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/free-tool-strategy
---

# Free Tool Strategy

Build free tools that generate traffic, leads, and backlinks without paid ads. Decide what to build, design for value + capture, launch so people find it.

## Gather context
Product & audience (core product, adjacent problem a tool could solve, what they search that isn't your product) · resources (eng time, design/no-code, maintainer) · goals (SEO/leads/backlinks/awareness + what a "win" looks like).

## Modes
1. **Evaluate ideas** — score each against the 6-factor framework, validate keyword data before committing eng time.
2. **Design** — define value exchange (input→output), minimize friction, plan lead capture, design shareable output, plan SEO landing page.
3. **Launch & measure** — SEO page + schema + directories, launch channels (PH/HN/newsletters/social), outreach list, tracking, iterate.

## Tool types
Calculator (number/range) · Generator (text/content) · Checker (analyzes URL/text, scores) · Grader (scores vs rubric) · Converter · Template · Interactive Visualization.

## 6-factor evaluation (score each 1-5; highest builds first)
Search volume · competition (no good free alternatives = strong) · build effort (days = strong) · lead-capture potential (natural fit = strong) · SEO value (link magnet = strong) · viral potential (shareable results = strong). 25-30 build now · 18-24 strong (validate volume) · 12-17 maybe · <12 pass.

## Design principles
- **Value before gate** — show core value first, gate the upgrade (deeper report, saved results, email delivery). If it's only valuable after they give email, you built a lead form.
- **Minimal friction** — max 3 inputs to first result, no account for core value, progressive disclosure, mobile-optimized (50%+ traffic).
- **Shareable results** — unique results URL, "tweet your score," embed code, downloadable report, social-ready image.
- **Mobile-first** — touch inputs, clean mobile render, native share sheet, no hover-only UI.

## Lead capture
Gate with email when results warrant a "report," produce ongoing value, or are personalized. Don't gate when result is a single number, competitors don't, or goal is SEO/backlinks (gates hurt time-on-page + links). Ask the minimum (each field ~−10% completion): first gate = email; second gate = name + company size + role. Progressive profiling across sessions.

## SEO
Landing page: `H1: [Tool] — [what it does]`; subhead (who + problem); tool above fold; how-it-works; why-[audience]-use-it; related questions; FAQ. Keyword in H1, slug, meta title, first 100 words, ≥2 subheadings. Add `SoftwareApplication` schema with `offers.price: "0"`. Plan the outreach list (who writes "best free tools for X") before launch.

## Measurement (from day one)
Tool usage (GA4) · lead conversion (CRM + events) · organic traffic (GSC) · referring domains (Ahrefs/GSC) · email→paid (CRM attribution) · bounce/time-on-page. 90-day targets: 500+ organic sessions/mo, 5-15% lead conversion, 10+ organic backlinks.

## Proactive flags
Account required before use → redesign gate (kills SEO + virality). No shareable output → missed virality. No keyword validation → 3h research beats 3 weeks building. Established free competitor → "10x better or don't build it." Single input→single output → low SEO/link value. No maintenance plan → free tools die when an API/logic goes stale.

Build decisions are binary — "build it" or "don't build it" with a clear reason.
