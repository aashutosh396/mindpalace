---
name: devrel-content
description: Use when writing technical content for developers — blog posts, tutorials, documentation, comparisons, thought leadership, dev blog, technical writing, or content for developers.
version: 1.0.0
license: MIT
tags: [devrel, content, technical-writing, blog, tutorials, code-examples, developer-marketing, seo]
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/devrel-content
derived_from: awesomeclaude
---

# DevRel Content

Create technical content developers actually read: posts, tutorials, docs, and thought leadership that build trust and drive adoption. Know your audience first (role, seniority, stack, pain points, verbatim language, tone).

## Phase 1 — Research & validate

Before writing, confirm the topic is worth it:
- **Search intent**: what already ranks, what's missing.
- **Community signals**: Reddit/HN/Stack Overflow — are devs asking?
- **Competitor gaps**: what haven't they covered.
- **Internal data**: support tickets, Discord, GitHub issues.
- **Keyword research**: search volume for technical terms.

Don't write if: only you care, 10 identical articles exist, topic too broad ("Intro to JavaScript"), or too narrow (no volume, no interest).

## Phase 2 — Pick the format

| Type | Best for | Structure |
|---|---|---|
| Tutorial | Teaching a skill | Step-by-step, code-heavy |
| Guide | Comprehensive topic | Sections, reference |
| Comparison | Decisions | Table, pros/cons |
| Announcement | Launches | News lead, what/why/how |
| Thought leadership | Authority | Opinion, predictions |
| Case study | Social proof | Problem → Solution → Results |
| Troubleshooting | Specific errors | Error → Cause → Fix |

## Phase 3 — Outline

Title (promises specific value) → Hook (problem + credibility + promise, 2-3 sentences) → optional context → the meat (sections each with explanation + code + pitfall/tip) → putting it together (complete working code) → what's next (deeper links + CTA).

## Code examples are the content

The copy-paste test — every snippet must: run without modification, include imports, show output, handle errors, use real values (no foo/bar). Show install command, the file, run command, and expected output. Use the right code-fence language and idiom per language (npm/pip/go get/cargo; `process.env`/`os.environ`/`os.Getenv`).

## Technical accuracy checklist

Copy-paste and run every snippet; versions current; click every link; run every CLI command; screenshots current; no deprecated APIs; no hardcoded secrets; have an engineer peer-review.

## SEO for dev content

Dev search patterns: error messages, "how to", "[A] vs [B] [year]", "best practices", "alternatives to X", "X with Y". Optimize title (keyword + framework + year), meta (~150 chars, specific outcome), H1 matches title, scannable keyword H2s, syntax-highlighted code (helps snippets), internal + external (official docs) links, keyword URL slug.

Example title upgrade: "Using Our API" → "How to Authenticate with the YourProduct API (Node.js)".

## Quality signals

Do: show don't tell (code over prose), address the "why", acknowledge tradeoffs, link sources, include dates/versions, progressive disclosure, real production examples.

Don't: walls of text, marketing speak ("best-in-class", "seamless"), assume knowledge, ship outdated content, bury the lede, omit code.

## Measure

Track page views, time on page, scroll depth, bounce, rankings, backlinks, social shares (HN/Twitter/Reddit), conversion events. Map the path: search/social → post → docs/quickstart → sign up → activation.

## Tools

Octolens/listening tools (where content gets shared); Grammarly/Hemingway (readability); Carbon/Ray.so (code screenshots); Excalidraw (diagrams); Loom (walkthroughs); Ahrefs/Semrush + Search Console (SEO).
