---
name: Fact Checker
description: Use when asked to fact-check, verify claims, validate accuracy, or update outdated information in a document — verifies factual claims against authoritative web sources and proposes corrections with user approval.
tags: [fact-check, verification, claims, accuracy, sources, citations, web-search, corrections, outdated]
source: daymade/claude-code-skills
derived_from: fact-checker
---

# Fact Checker

Verify factual claims and propose corrections backed by authoritative sources. Apply changes ONLY after user approval.

## Workflow
```
- [ ] 1. Identify factual claims
- [ ] 2. Search authoritative sources
- [ ] 3. Compare claims against sources
- [ ] 4. Generate correction report
- [ ] 5. Apply corrections with user approval
```

### 1. Identify claims
Target: technical specs (context windows, pricing, features), version numbers/release dates, statistics/metrics, API capabilities/limits, benchmark scores.
Skip: opinions, recommendations, explanatory prose, tutorial instructions, architecture discussion.

### 2. Search authoritative sources
- AI models: official announcements (anthropic.com/news, openai.com, blog.google), API docs (platform.claude.com/docs, platform.openai.com/docs), release notes.
- Libraries: official docs, GitHub releases/README, registries (npm, PyPI, crates.io).
- General: academic papers, government stats, standards bodies.
- Query strategy: model name + spec, include current year, cross-check multiple sources.

### 3. Compare (table)
| Claim in doc | Source info | Status | Authoritative source |
Status codes: ✅ accurate · ❌ incorrect · ⚠️ outdated · ❓ unverifiable.

### 4. Correction report
For each issue: location (file:line), current claim, correction, source URL, rationale. Include summary counts (checked / accurate / issues).

### 5. Apply with approval
Show report → wait for explicit "apply these corrections?" → only then Edit. After: verify edits landed, summarize, remind to commit.

## Search best practices
- Good queries are specific + current ("Claude Opus 4.5 context window 2026"); avoid vague ("Claude context").
- Source priority: official product pages > API docs > official blog > GitHub releases. Use third-party aggregators only to cross-check; avoid outdated docs, uncited wikis, rumors.
- Conflicts: prefer most recent official doc, note discrepancy, present both. No source found: mark ❓, suggest qualified phrasing ("approximately", "reported as", "as of <date>").

## Special care
- Time-sensitive: always add temporal context ("as of Jan 2026", "released Sept 2025"); avoid "latest"/"current".
- Numerical precision: match the source ("200K tokens" exact; "1M tokens (approximately)" when source is approximate).
- Include citations/links in corrections.

## Limits
Cannot verify subjective opinions, access paywalled sources, settle disputed claims, or predict future specs. For those: note the limitation, suggest qualification language, recommend expert consultation.
