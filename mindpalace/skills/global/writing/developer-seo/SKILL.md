---
name: developer-seo
description: Use when doing SEO for developer tools, ranking for technical queries, error-message content strategy, competing with official docs in search, technical keyword research, or developer content SEO.
version: 1.0.0
license: MIT
tags: [seo, developer-marketing, content, technical-content, keyword-research, error-messages, documentation]
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/developer-seo
derived_from: awesomeclaude
---

# Developer SEO

Developer SEO differs from traditional SEO. Developers search with precise technical intent (error messages, API questions, "how to X in Y" queries), bounce from thin content, and respect sites that actually solve problems. Your real competition is Stack Overflow, official docs, and GitHub issues.

## How developers search

Query patterns: verbatim error messages, "how to [action] in [lang]", "[A] vs [B]", "[concept] tutorial", "[library] [function] example".

Intent categories: troubleshooting, learning, evaluating, implementing, reference. Match the page to the intent.

## Keyword research

Find high-intent technical long-tail keywords:
1. Mine support tickets, Discord/Slack, GitHub issues for exact phrasing.
2. Mine Stack Overflow for question wording and unsatisfied threads.
3. Google Search Console — queries you rank 5-20 for, question queries, error-message queries hitting your site.
4. Competitor content gaps — questions their docs never answer.

## Error-message SEO

Errors are SEO gold (devs copy-paste them). Create dedicated pages: exact error text in title/H1, full error early in body, the actual fix (not generic troubleshooting), why it happens, related errors.

Structure: Title `[Exact Error] - How to Fix` → The Error → Quick Fix → Why This Happens → Other Solutions → Related Errors.

## Competing with official docs

Docs have authority but weak spots: no "why", missing real-world examples, no troubleshooting, outdated, no comparisons. Your openings: hand-holding getting-started guides, "X vs Y" comparisons, migration guides, real implementation examples, gotchas.

## Content formats that rank

- **How-to guides**: Prerequisites → TL;DR snippet → step-by-step with output → complete example → common issues → next steps.
- **Comparison content** ("[A] vs [B]"): be genuinely objective, include code comparisons, cover where each wins, admit your limitations.
- **Tutorial series**: build topical authority via pillar + supporting content, interlinked.

## Technical SEO for dev sites

- Code: semantic HTML (`<code>`, `<pre>`), real text not images, language hints, working examples.
- Speed: minimize JS on docs, render without JS where possible, optimize for conference Wi-Fi and ad blockers.
- Architecture: clear hierarchy, breadcrumbs, consistent URLs, canonical tags for versioned docs, XML sitemaps.

## Authority

Quality technical backlinks beat quantity: GitHub READMEs, technical blog citations, Stack Overflow answer links, newsletter mentions, talk resource lists. Avoid generic guest posting, link exchanges, directory spam.

Freshness matters — review major guides quarterly, show "last updated" dates, redirect obsolete content.

## Metrics

Track: organic traffic to docs/guides, rankings for target queries, time on tutorial pages, Search Console impressions for error queries, GitHub referrals. Interpret carefully: bounce rate (leaving fast = found answer = success), pages/session, conversion (long attribution windows).

## Common mistakes

Writing for engines not developers; ignoring search intent; thin content; outdated examples; no unique value beyond official docs.

## Tools

Google Search Console (rankings, query discovery); Ahrefs/Semrush (keywords, competitors); Screaming Frog (technical audits); Algolia (on-site search analytics); developer-listening tools to find content opportunities.
