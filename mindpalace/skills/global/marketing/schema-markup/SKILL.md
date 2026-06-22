---
name: Schema Markup (Structured Data)
description: Use when implementing, auditing, or validating structured data — schema.org / JSON-LD for rich results, FAQ/Product/HowTo schema, GSC structured-data errors, or AI-search citation visibility.
tags: [schema, structured-data, json-ld, schema.org, rich-results, rich-snippets, faq-schema, product-schema, seo, ai-search]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/schema-markup
---

Implement, audit, and validate JSON-LD schema that earns rich results and makes content legible to AI search systems. (For full SEO use seo-audit; for architecture use site-architecture.)

## Three modes
- **Audit** — extract existing JSON-LD, check required fields vs schema-types guide, cross-ref GSC Enhancements; deliver: present / broken / missing + priority.
- **Implement** — pick page type → right schema → populate with real content → advise placement → deliver copy-paste-ready JSON-LD.
- **Validate & fix** — test at rich-results.google.com + validator.schema.org, map errors to fields, deliver corrected JSON-LD + why each fix works.

## Schema type selection
| Page | Primary | Supporting |
|---|---|---|
| Homepage | Organization | WebSite (SearchAction) |
| Blog/article | Article | BreadcrumbList, Person (author) |
| How-to | HowTo | Article, BreadcrumbList |
| FAQ | FAQPage | — |
| Product | Product | Offer, AggregateRating, BreadcrumbList |
| Local business | LocalBusiness | OpeningHoursSpecification, GeoCoordinates |
| Video | VideoObject | Article (if embedded) |
| Category/hub | CollectionPage | BreadcrumbList |
| Event | Event | Organization, Place |

**Rules:** add BreadcrumbList to any non-homepage with visible breadcrumbs; Article+BreadcrumbList+Person is the common blog triple; never add Product to a page that doesn't sell one (Google penalizes misuse).

## Implementation
JSON-LD only (Microdata/RDFa are legacy). Place `<script type="application/ld+json">` in `<head>`; multiple blocks fine. Site-wide: Organization in template header + WebSite SearchAction on homepage. Per-page: content schema + BreadcrumbList. CMS: WP (Yoast/Rank Math handle Article/Org; add HowTo/FAQ via blocks), Shopify (Product auto; add Org/Article), custom (generate server-side from real fields).

## Common mistakes (the ones that kill rich results)
Missing `@context` → won't parse. Missing required fields → no rich result. Empty/generic `name`. Relative `image` path → must be absolute. Markup ≠ visible content → policy violation. Nesting Product inside Article. Deprecated properties. Wrong date format → use ISO 8601. Product without `offers` → no product rich result.

## Schema & AI search
FAQPage schema increases citation likelihood (LLMs love structured Q&A). Article with `author` + `datePublished` signals freshness/authority. Organization with `sameAs` connects your entity across the web. Actions: add FAQPage to any Q&A page (even 3 Qs), add author `sameAs` to real profiles, add Org `sameAs` to socials + Wikidata, keep `datePublished`/`dateModified` accurate.

## Validate (use all before publishing)
Google Rich Results Test (eligibility, errors vs warnings) · validator.schema.org (full spec) · local extractor scoring completeness 0-100 · GSC Enhancements (real-world errors + rich-result performance, updates 1-2wk after deploy).

## Proactive flags
FAQ content without FAQPage schema · Article missing required `image` · schema injected via GTM (often not indexed — recommend server-side) · `dateModified` < `datePublished` (impossible) · conflicting `@type` on one entity.
