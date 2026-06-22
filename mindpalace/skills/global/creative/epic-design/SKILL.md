---
name: Epic Cinematic Web Design (2.5D)
description: Use for any cinematic/premium web design task — scroll storytelling, parallax depth, text animations, sticky/overlap sections, floating products, clip-path reveals. Apple-style/Awwwards aesthetic with flat assets + CSS/JS (no WebGL).
tags: [web-design, scrollytelling, parallax, gsap, animation, 2.5d, cinematic, depth-layers, clip-path, accessibility]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/epic-design
---

# Epic Cinematic Web Design (2.5D)

Build immersive sites that feel premium and alive — flat PNG/static assets + CSS + JS, no WebGL. Never build a flat static page when this is active: every page needs depth/layers responding to scroll, text entering/exiting with intention, cinematic section transitions.

## Step 1 — Brief + Asset Inspection
Extract: product/content, mood (dark-cinematic / bright / minimal-luxury), section count. **Inspect every image:** format (JPEG has no alpha), background status. **Judge whether bg needs removing** — REMOVE for isolated products/characters/logos/floating depth-2/3 assets; KEEP for screenshots, section backgrounds, artwork, mockups, depth-0 fills. Never auto-remove; inform user per asset and confirm.

**Compositional hierarchy** (assets are NOT all same size): one HERO (50-80vw, depth-3); companions 15-25% of hero (depth-2, hugging edges via `calc()`); accents/particles 1-5vw (depth-5); background fills full section (depth-0). When hero exits on scroll, companions scatter outward.

## Step 2 — Choose Techniques (Decision Engine)
Match intent:
- Product launch → inter-section floating product + perspective zoom + split converge + DJI scale-in.
- Hero big title → 6-layer parallax + pinned sticky + bleed typography.
- Apple-style → scrub timeline + word-by-word scroll lighting + character cylinder.
- Cards → cascading card stack + skew/elastic bounce.
- Scroll behaviors: "stays in place"→`pin:true`+scrub; "rises from section"→floating product+clip-path birth; "born from top"→top-down clip birth; "curtain"→panel roll-up; "circle opens"→iris expand.

## Step 3 — Layer Every Element (non-negotiable)
```
DEPTH 0 → background  | parallax 0.10x | blur 8px | scale 0.70
DEPTH 1 → glow/atmos  | 0.25x | 4px | 0.85
DEPTH 2 → mid decor   | 0.50x | 0px | 1.00
DEPTH 3 → main object | 0.80x | 0px | 1.05
DEPTH 4 → UI/text     | 1.00x | 0px | 1.00
DEPTH 5 → foreground  | 1.20x | 0px | 1.10
```
Apply `data-depth="3"` + matching `.depth-3` CSS.

## Step 4 — Accessibility & Performance (always)
`@media (prefers-reduced-motion: reduce)` kills animation. Only animate `transform/opacity/filter/clip-path` — never width/height/top/left. `will-change: transform` only while animating, remove after. `content-visibility: auto` off-screen. IntersectionObserver to animate in-viewport only. `matchMedia('(pointer: coarse)')` → reduce effects on touch.

## Step 5 — Code Structure
Section wrapper with 3+ depth layers minimum; decorative layers `aria-hidden="true"`; hero `<img>` in depth-3, text in depth-4.

## Quick Rules (non-negotiable)
Run asset inspection before coding · judge bg removal per asset · ≥3 depth layers/section · ≥1 animation/text element · `prefers-reduced-motion` fallback · GPU-safe props only · products depth-3, backgrounds depth-0 blurred · float loops (6-14s) on heroes · decorative = aria-hidden · mobile reduced via pointer:coarse · remove will-change after.

## Output
Single self-contained HTML (inline CSS+JS), GSAP via jsDelivr CDN, comments per technique, note listing techniques applied. Confidence tag: green verified / yellow experimental / red limited browser support.
