---
name: md-document (Long-form markdown → HTML)
description: Use when converting a long-form markdown spec / RFC / report / plan / explainer (≥100 lines) into a single-file, lightly-interactive HTML document with sticky TOC, scrollspy, search filter, code-copy buttons, and brand tokens. Refuses below 100 lines or without design-system onboarding.
tags: [markdown, html, documentation, single-file, toc, scrollspy, search, code-copy, rfc, spec, report]
source: alirezarezvani/claude-skills
derived_from: markdown-html/skills/md-document
---

# md-document — Long-form markdown → HTML

The 90%-case converter (specs, plans, RFCs, reports, explainers). Pipeline: **parse markdown → render HTML → inject interactivity**.

1. **markdown_parser** — CommonMark subset → section AST.
2. **html_renderer** — AST + design-system config → single-file HTML.
3. **interactivity_injector** — vanilla-JS payload (search / copycode / smoothscroll / scrollspy), idempotent (marker check).

## What gets rendered

- Headings H1-H6 (every H2+ gets an anchor id + TOC entry; H1 becomes `<title>`, excluded from TOC)
- Paragraphs with inline **bold** / *italic* / `code` / links / images
- Fenced code blocks with Prism.js highlighting on demand
- GFM tables (per-column alignment)
- GFM callouts `> [!NOTE]/[!TIP]/[!IMPORTANT]/[!WARNING]/[!CAUTION]`
- Blockquotes, single-level ordered/unordered lists, horizontal rules

Out of scope: nested lists, HTML inlines, footnotes, definition lists, task-list checkboxes, reference-style links.

## Interactive features (all ~1 KB each)

Search filter on H2 sections (Esc clears) · code-copy buttons (clipboard + execCommand fallback) · smooth-scroll on TOC links · scrollspy via IntersectionObserver (sets `aria-current="location"` on the matching TOC entry). TOC behavior follows config: sticky-sidebar / collapsible-top / inline / none.

## Hard rules

1. Refuse input < 100 lines (markdown wins below the threshold).
2. Refuse without onboarding (surface the design-system wizard).
3. Single-file output — all CSS+JS inline; only externals are `fonts.googleapis.com` + Prism CDN. Anything else is a regression.
4. **Customization must change behavior** — `design_style=editorial` → 720px-wide, 1.75 line-height; `playful` → rounded callouts + shadow; `technical` → dense, 0.875rem code. Smoke-tested, not decorative.
5. WCAG AA tokens — body text ≥4.5:1, links walked to 4.5:1.
6. Idempotent injection; re-rendering with a different design_style works cleanly.

## Forcing questions

1. What's the document for — skim, decide, or deep-read? (Name it; density follows.)
2. Sticky-sidebar TOC or collapsible-top? (Sticky for >800 words / 4+ H2s; collapsible for short mobile-first.)
3. All four interactive features or a subset? (All four — cheap.)
4. Code theme — light, dark, or auto? (Auto follows OS prefers-color-scheme.)
5. Clear H1 title? (Yes — becomes the page title, excluded from TOC.)

Distinct from md-review (diff + margin annotations), md-slides (split into slides), landing (generates from scratch). Output: `{output_dir}/doc-{slug}.html`.

Empirical: ~150-line markdown → ~11 KB HTML (15 KB with JS); ~470 lines → ~17/23 KB — vs 200 KB+ for Notion/Confluence exports.
