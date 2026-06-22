---
name: Landing Page Generator
description: Use when creating a high-converting landing/marketing page — generates Next.js/React TSX + Tailwind sections (hero, features, pricing, FAQ, testimonials, CTA) with proven copy frameworks, SEO meta, and Core Web Vitals targets.
tags: [landing-page, marketing-page, conversion, tsx, tailwind, copywriting, pas, aida, seo, hero-section]
source: alirezarezvani/claude-skills
derived_from: product-team/landing-page-generator
---

# Landing Page Generator

Generate high-converting landing pages as complete Next.js/React TSX + Tailwind components. Real converting copy, not lorem ipsum. Targets: LCP <1s · CLS <0.1 · FID/INP <100ms.

## Workflow (in order)

1. **Gather inputs** — product, tagline, audience, pain point, key benefit, pricing tiers, design style, copy framework. Ask only for missing fields.
2. **Analyze brand voice** (if existing copy exists) → map to style + framework: formal+professional → enterprise/AIDA; casual+friendly → bold-startup/BAB; professional+authoritative → dark-saas/PAS; casual+conversational → clean-minimal/BAB.
3. **Select design style** (below).
4. **Apply copy framework** to all headlines/body before generating.
5. **Generate sections in order** — Hero → Features → Pricing → FAQ → Testimonials → CTA → Footer. Skip irrelevant sections.
6. **Validate against SEO checklist** — fix gaps inline.
7. **Output** copy-paste-ready TSX with all Tailwind classes, SEO meta, structured data.

## Design Styles (Tailwind class sets)

| Style | Background | Accent | Cards | CTA |
|---|---|---|---|---|
| Dark SaaS | `bg-gray-950 text-white` | violet-500 | `bg-gray-900 border-gray-800` | `bg-violet-600 hover:bg-violet-500` |
| Clean Minimal | `bg-white text-gray-900` | blue-600 | `bg-gray-50 border-gray-200 rounded-2xl` | `bg-blue-600 hover:bg-blue-700` |
| Bold Startup | `bg-white text-gray-900` | orange-500 | `shadow-xl rounded-3xl` | `bg-orange-500 hover:bg-orange-600` |
| Enterprise | `bg-slate-50 text-slate-900` | slate-700 | `bg-white border-slate-200 shadow-sm` | `bg-slate-900 hover:bg-slate-800` |

Bold Startup headings: add `font-black tracking-tight`.

## Copy Frameworks

- **PAS** (Problem → Agitate → Solution) — H1 = painful state; sub = cost of inaction; CTA = what you offer.
- **AIDA** (Attention → Interest → Desire → Action) — bold statement → interesting fact → proof points → clear action.
- **BAB** (Before → After → Bridge) — H1 = "[before] → [after]"; sub = "here's how [product] bridges the gap"; features = the bridge.

## Section Patterns

- **Hero** — centered/split/gradient/video-bg/minimal. Badge + H1 (gradient clip-text accent) + sub + primary/ghost CTA pair + trust line ("No credit card required").
- **Features** — alternating: map `{title, description, image, badge}`, toggle `i%2===1 ? "lg:flex-row-reverse" : ""`, `<Image>` with explicit w/h.
- **Pricing** — map `{name, price, features[], cta, highlighted}`; highlighted gets `border-2 border-violet-500 ring-4 ring-violet-500/20`; `grid lg:grid-cols-3`; null price = "Custom".
- **FAQ** — inject `FAQPage` JSON-LD; shadcn `<Accordion type="single" collapsible>`.
- **Testimonials/CTA/Footer** — grid or single-quote; full-width CTA banner with trust signals below; footer `border-t`.

## SEO Checklist (verify before output)

`<title>` keyword+brand 50-60 chars · meta description benefit+CTA 150-160 · OG image 1200×630 · single H1 with keyword · structured data (FAQPage/Product/Organization) · canonical URL · alt text on all images · robots.txt + sitemap · CWV targets · mobile viewport meta · internal links to pricing/docs.

## Performance Techniques

LCP: `priority` on hero `<Image>`. CLS: explicit w/h on all images. INP: defer non-critical JS, `loading="lazy"`. TTFB: ISR/static generation. Bundle: audit with `@next/bundle-analyzer`.

## Pitfalls

Hero image not preloaded; missing mobile breakpoints (design mobile-first with `sm:`); vague CTA ("Start free trial" beats "Sign up"); pricing missing trust signals; no above-the-fold CTA on 375px mobile.
