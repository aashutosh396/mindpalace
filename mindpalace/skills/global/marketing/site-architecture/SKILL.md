---
name: Site Architecture & Internal Linking
description: Use when auditing, redesigning, or planning a website's structure, URL hierarchy, navigation, or internal linking — covers flat-vs-layered URLs, navigation zones, silo/hub-and-spoke topic clusters, orphan-page fixing, and anchor-text strategy.
tags: [site-architecture, url-structure, internal-links, navigation, breadcrumbs, topic-clusters, hub-and-spoke, orphan-pages, information-architecture, silo]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/site-architecture
---

# Site Architecture & Internal Linking

Design structure that's easy to navigate, easy to crawl, and builds topical authority through intelligent internal linking.

## Three modes
- **Audit** — analyze sitemap.xml (depth distribution, URL patterns, orphans, duplicate paths), evaluate navigation, rank problems by SEO impact, deliver prioritized fixes.
- **Plan new structure** — map goals→sections, design URL hierarchy, define content silos, plan navigation zones, deliver a text-tree site map + URL spec.
- **Internal linking** — identify hubs, map spokes, find orphans, audit anchor text, deliver a linking plan with anchor guidance.

## URL structure
Core rule: URLs are for humans first. Get it right once — changes need redirects and lose equity.
| Depth | Example | Use |
|---|---|---|
| Flat | `/blog/cold-email-tips` | posts, standalone pages |
| Two levels | `/blog/email-marketing/cold-email-tips` | when the category is itself a ranking page |
| Three | `/solutions/marketing/email-automation` | product families |
| 4+ | ❌ | dilutes crawl equity |

Rule of thumb: if the category URL isn't a real page you want to rank, don't create the directory — flat is usually better. Construction: hyphens not underscores; no redundant suffixes; no dynamic `?id=`; consistent trailing slash; include the primary keyword but don't stuff.

## Navigation zones
Primary nav (5-8 items max, each links to a rankable page) · Secondary (within a silo) · Breadcrumbs (upward equity + BreadcrumbList schema; every segment a real link) · Footer (high-value pages only) · Contextual in-content links (most powerful) · Sidebar. Add breadcrumbs to every non-homepage page.

## Silos & topical authority (hub-and-spoke)
Hub (pillar, broad topic) links to all spokes; each spoke links back to hub; spokes link to adjacent spokes when relevant; deep pages link up to spoke + hub. Build the cluster (content) BEFORE the links. 3-7 core topics for a focused site.

## Internal linking
Equity flows from homepage outward; closer pages get more. Anchor text: partial-match is the primary approach; exact-match sparingly (1-2x/page); avoid generic ("click here") and naked URLs. **Linking priority stack:** in-content > hub links > navigation > footer > sidebar.

**Orphan pages** (indexed, no inbound internal links): find by diffing all-indexed-URLs vs all-internal-links; fix by adding contextual links from relevant pages + hub pages — or question whether they should exist.

## Common mistakes → fix
Orphan pages → contextual links · URL change without redirect → always 301 · duplicate paths → canonical/merge · deep nesting → flatten · sitewide footer to every post → high-value only · category pages with no content → add a pillar · homepage linking nowhere → link to key hubs · dynamic param URLs → canonicalize/robots block.
