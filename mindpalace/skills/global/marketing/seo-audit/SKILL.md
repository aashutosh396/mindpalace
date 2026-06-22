---
name: SEO Audit
description: Use when auditing, reviewing, or diagnosing SEO issues on a site — walks technical (crawl/indexation/speed/CWV), on-page (titles/headings/links/keywords), and content (intent/E-E-A-T/thin pages) layers and delivers a prioritized Issue/Impact/Evidence/Fix/Priority action plan.
tags: [seo-audit, technical-seo, on-page-seo, core-web-vitals, eeat, indexation, meta-tags, seo-health-check, ranking]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/seo-audit
---

# SEO Audit

Identify SEO issues and give actionable fixes. (For building pages at scale, use programmatic-seo; for structural redesign, use site-architecture.)

## Initial assessment
Site context (type, primary SEO goal, priority keywords) · current state (known issues, traffic level, recent changes/migrations) · scope (full site vs pages; technical+on-page vs one area; Search Console access).

## Audit framework — three layers
1. **Technical** — crawlability, indexation, speed, Core Web Vitals.
2. **On-page** — titles, meta, headings, internal links, keyword targeting.
3. **Content** — search-intent match, E-E-A-T, thin/duplicate pages.

## Core Web Vitals thresholds (75th percentile of real-user data)
| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | ≤2.5s | 2.5-4.0s | >4.0s |
| INP | ≤200ms | 200-500ms | >500ms |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |

## Finding format (use consistently)
**Issue** (what's wrong) · **Impact** (High/Medium/Low) · **Evidence** (how you found it) · **Fix** (specific recommendation) · **Priority** (1-5).

## Report structure
1. **Executive summary** — overall health (lead with a weighted health score + weakest categories), top 3-5 priority issues, quick wins.
2. **Technical findings** (Issue/Impact/Evidence/Fix/Priority).
3. **On-page findings.**
4. **Content findings.**
5. **Prioritized action plan** — Critical (blocking indexation/ranking) → High-impact → Quick wins → Long-term.

## Communication standard
Lead with the exec summary (≤5 bullets) · keep quick wins separate from high-effort items · never present a recommendation without evidence/rationale · write for a technically-aware non-SEO-specialist.

## Proactive triggers
Traffic drop mentioned → scope an audit · site migration/redesign → pre/post-migration audit needs · "why isn't my page ranking?" → on-page + intent checklist before external factors · content-strategy discussion with keyword gaps → suggest audit · new launch → technical pre-launch checklist.

## Tools referenced
Free: Search Console (essential), PageSpeed Insights, Bing Webmaster Tools, Rich Results Test, Mobile-Friendly Test, Schema Validator. Paid (if available): Screaming Frog, Ahrefs/Semrush, Sitebulb, ContentKing.

References worth keeping: full audit framework + remediation patterns, CWV triage rules, E-E-A-T checklist, schema types by content type.
