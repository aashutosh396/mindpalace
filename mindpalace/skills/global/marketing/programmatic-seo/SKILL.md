---
name: Programmatic SEO
description: Use when creating SEO-driven pages at scale from templates + data — choosing a playbook (locations, comparisons, integrations, glossary, etc.), validating demand and data defensibility, designing templates that avoid thin-content penalties, and planning internal linking + indexation.
tags: [programmatic-seo, pseo, template-pages, pages-at-scale, location-pages, comparison-pages, internal-linking, thin-content, indexation]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/programmatic-seo
---

# Programmatic SEO

Build SEO-optimized pages at scale that rank, provide value, and avoid thin-content penalties.

## Core principles
1. **Unique value per page** — not just swapped variables.
2. **Proprietary data wins.** Defensibility hierarchy: proprietary > product-derived > user-generated > licensed > public (weakest).
3. **Clean URLs** — subfolders not subdomains (`site.com/templates/resume/` not `templates.site.com/`).
4. **Genuine intent match.**
5. **Quality over quantity** — 100 great pages beat 10,000 thin ones.
6. **Avoid Google penalties** — no doorway pages, keyword stuffing, or duplicate content.

## The 12 playbooks
Templates ("[type] template") · Curation ("best [category]") · Conversions ("[X] to [Y]") · Comparisons ("[X] vs [Y]") · Examples · Locations ("[service] in [city]") · Personas ("[product] for [audience]") · Integrations ("[A] [B] integration") · Glossary ("what is [term]") · Translations · Directory · Profiles. Layerable (e.g., "best coworking spaces in San Diego").

**Choosing:** proprietary data → Directories/Profiles; integrations → Integrations; design product → Templates/Examples; multi-segment → Personas; local → Locations; tool/utility → Conversions; expertise → Glossary/Curation; competitor landscape → Comparisons.

## Implementation framework
1. **Keyword pattern research** — identify repeating structure + variables + unique combinations; validate aggregate volume, head-vs-tail distribution, trend.
2. **Data requirements** — what populates each page; first-party/scraped/licensed/public; update cadence.
3. **URL pattern generation** — expand the template (e.g., `{tool}-vs-{competitor}-comparison`), count pages, flag slug problems. **If expansion exceeds your unique data, cut variables — don't ship thin pages.**
4. **Template design** — header w/ target keyword, unique intro (not just swapped vars), data-driven sections, related-page links, intent-appropriate CTA. Conditional content + original insight per page.
5. **Internal linking** — hub-and-spoke: hub category page, spoke pages, cross-links between related spokes. No orphan pages; XML sitemap; breadcrumbs with schema.
6. **Indexation** — prioritize high-volume patterns; noindex very thin variations; manage crawl budget; separate sitemaps by page type.

## Quality gates
Pre-launch: unique value/page, answers intent, unique titles/meta, proper headings, schema, acceptable speed, connected to architecture, no orphans, crawlable. Post-launch monitor: indexation rate, rankings, traffic, engagement, conversion. Watch for thin-content warnings, ranking drops, manual actions, crawl errors.

## Common mistakes
Thin content (swapping city names in identical copy) · keyword cannibalization · over-generation (no demand) · poor data quality · pages for Google not users. Call out thin-content risk explicitly when the data source is public/scraped.
