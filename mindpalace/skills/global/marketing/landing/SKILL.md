---
name: Landing Page Generator (single-file HTML)
description: Use when the user wants a polished single-page HTML landing page ("create/build a landing page", "one-pager", "sales page", "promotional page") — runs a 4-question intake to lock positioning, then emits one self-contained HTML file with GSAP animations, mouse parallax, and brand-overridable colors.
tags: [landing-page, html, gsap, animation, single-file, hero, brand-palette, web-design, one-pager, sales-page]
source: alirezarezvani/claude-skills
derived_from: marketing/landing/skills/landing
---

# Landing Page Generator

Generates ONE self-contained `.html` file: all CSS in `<style>`, all JS in `<script>`, only externals = Google Fonts + GSAP CDN. Write to disk (CLI) or as an HTML artifact (web).

## Phase 0 — Intake (4 forcing questions, one at a time, max 4)

1. **Product/service?** Name + 1-2 sentence elevator pitch (what it does + who for). Refuse mush — "app for productivity" yields boilerplate; push back once. If still vague, deliver with explicit "generic positioning" caveat.
2. **Audience register?** (1) Technical buyers, (2) Business buyers, (3) Consumers, (4) Internal. Dictates copy register, jargon, social proof, CTA framing.
3. **Brand overrides?** primary HEX, accent HEX, optional bg HEX — or "default" (dark navy + teal + Inter). If only primary given, derive accent algorithmically (lighten 15% for accent, darken 8% for navy-mid, rgba 0.12 for glow).
4. **Tone?** (1) Professional, (2) Playful, (3) Authoritative, (4) Minimal. Recommended default: professional for technical/business, playful for consumer, minimal for design-led.

Stop after Q4; commit and generate in one pass. No outlining first.

## Content extraction (with fallback)

From the pitch derive: hero headline (8-12 words), hero subtext (1-2 sentences), 3-6 feature bullets, CTA text, closing copy. If input is sparse, invent compelling content from product-name semantics + audience register; flag inferred content with `<!-- inferred: ... -->`. Don't stall.

## Default palette

```css
:root{ --navy:#0A1628; --navy-mid:#0D1F38; --teal:#00D4AA;
  --teal-glow:rgba(0,212,170,.12); --amber:#F5A623; --off-white:#F7F7F2;
  --text-muted:rgba(247,247,242,.68); --card-bg:rgba(0,212,170,.06);
  --card-border:rgba(0,212,170,.15); }
```

Typography: Inter; weights 400 body / 500 eyebrow / 600 links / 700 subtitle / 800 H1+H2. Sizes: Hero H1 68-82px, Section H2 52-62px, card titles 22px, body 17-19px, eyebrow 13px uppercase letter-spaced, CTA 18px.

## Required sections

1. **Hero** — `min-height:100vh`, flex-centered; optional eyebrow, H1, subtitle, `.btn-primary`, animated scroll chevron. Depth layers for mouse parallax: `.hero-shapes-back` (large blurred low-opacity), `.hero-shapes-mid` (sharper higher-opacity), content layer.
2. **Features** — `repeat(3,1fr)` grid → 2-col at 900px → 1-col at 580px. Each card: SVG icon (28px, stroke=accent, no fill), title (22px/700), description (15-16px muted). Hover: `translateY(-6px)` + border brighten + 0.3s ease. Max 6 features.
3. **Closing CTA** — full-width `var(--navy-mid)`, `padding:120px 24px`, centered headline (52-62px/800) + subtext + CTA with radial-gradient glow.

## 5 animation patterns

1. **Hero entrance** — GSAP timeline; MUST `gsap.set([...], {opacity:0, y:30})` FIRST (FOUC prevention), then stagger `.eyebrow → h1 → subtitle → btn → scroll` with `power3.out`.
2. **Mouse parallax** — on `.hero` mousemove, `gsap.to` back shapes (×45/×22), mid (×22/×11), content (×8/×5), duration 0.8.
3. **Scroll-triggered cards** — `gsap.set(.feature-card,{opacity:0,y:55,rotateX:18})` + `ScrollTrigger.batch` start "top 80%", stagger 0.11.
4. **Floating shapes** — CSS `@keyframes` (cheaper than GSAP for indefinite motion), e.g. `floatA 12s ease-in-out infinite`.
5. **Scroll indicator** — CSS `@keyframes bounce` 2s infinite.

CDN: Google Fonts Inter + `gsap.min.js` + `ScrollTrigger.min.js` (cdnjs). NO other external CSS/JS.

## Output + validation

Path `${OUTPUT_DIR:-./landing-pages/}/<product-name-kebab>.html`. Viewport meta required. Post-generation checks: 3 sections present (`.hero`/`.features`/`.closing-cta`), CDN deps present, `gsap.set()` initial states precede any `gsap.timeline`/`gsap.to`, breakpoints at 900px+580px, no external stylesheet besides Google Fonts, no external script besides GSAP. If a check fails, regenerate ONLY the failing sections in one targeted pass.

## Anti-patterns

Hardcoded absolute output paths; outlining before writing; external CSS/JS files; skipping `gsap.set()` (FOUC); >6 features; brand-specific content baked into the skill.
