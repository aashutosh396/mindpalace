---
name: revealjs
description: "Use when the user asks to create slides, a presentation, a deck, a slideshow, a pitch deck, or reveal.js HTML slides — generates polished reveal.js presentations (HTML + CSS, no build step) with themes, multi-column layouts, charts, and speaker notes."
version: 1.0.0
license: MIT
tags: [revealjs, presentation, slides, deck, slideshow, html, css, charts, pitch-deck]
source: https://github.com/ryanbbrown/revealjs-skill/tree/main
derived_from: awesomeclaude
prerequisites:
  commands: [node, npx]
---

# Reveal.js Presentations

Create HTML presentations using reveal.js (loaded from CDN). No build step — open the HTML in a browser. Output is two files: an HTML file (slides) and a CSS file (theme/layout).

Helper scripts and reference docs live in the source repo under `skills/revealjs/` (`scripts/`, `references/`). Fetch them from the source URL when needed rather than reproducing here. Key scripts: `create-presentation.js`, `check-overflow.js`, `edit-html.js`; references: `advanced-features.md`, `charts.md`, `base-styles.css`.

## When to use

User wants slides / a deck / a presentation / a slideshow / a pitch deck, especially when they want a self-contained HTML file (no PowerPoint/Keynote, no build tooling).

## Design principles (do this BEFORE writing code)

- Analyze the content: subject, tone, industry, mood. Check for any company/brand mention and use their identity/colors.
- State your content-informed design approach (palette + fonts + layout intent) before generating.
- Pick 3–5 colors that genuinely match the topic (dominant + supporting + accent). Be adventurous; avoid autopilot (healthcare ≠ always green). Ensure strong text/background contrast.
- **Always use `pt` for font sizes** (slides are fixed-size; never `em`/`rem`/`px` for fonts). Only `--base-font-size` stays in px.
- Use web-safe fonts or Google Fonts via `@import` in CSS.
- Vary layouts across slides (columns, stacked, cards, blockquotes) — don't repeat the same pattern on consecutive slides. Keep text scannable (short bullets, one idea per slide). When a slide is light on content, scale text up to fill space.

## Workflow

### 1. Plan structure
Decide slide count, which are section dividers, and where vertical stacks (drill-down) help.

### 2. Generate scaffold
```bash
node <path-to-skill>/scripts/create-presentation.js --structure 1,1,d,3,1,d,1 --title "My Presentation" --output presentation.html
```
Options:
- `--slides N` — N horizontal slides (simple mode)
- `--structure <list>` — comma-separated: `1` = single slide, `N>1` = vertical stack of N, `d` = section divider
- `--output <file>`, `--title <text>`, `--styles <file>` (default `styles.css`)

The scaffold also copies `base-styles.css` to the presentation dir as `styles.css`, and includes Font Awesome + the Chart.js plugin.

### 3. Customize CSS
Edit the CSS variables in `styles.css` — set `--background-color` first, then fonts and colors. For dark backgrounds set `--text-color`/`--muted-color` to light values. Google Fonts via `@import` at top.

Key vars: `--background-color`, `--heading-font`, `--body-font`, `--base-font-size` (px), `--text-size` (16pt, intentionally small), `--h1/h2/h3-size`, `--primary-color`, `--secondary-color`, `--text-color`, `--muted-color`.

Text-size utilities to fill light slides: `.text-lg/.text-xl/.text-2xl/.text-3xl/.text-4xl`, `.text-muted`, `.text-center`. If a visual pattern repeats 3+ times (stat boxes, feature cards, timeline steps, bio cards), make it a CSS class instead of repeating inline styles.

### 4. Fill in HTML content — incrementally with Edit
Use the **Edit tool one/few slides at a time**, targeting the unique placeholder text the scaffold generates per slide. Do NOT rewrite the whole file with Write — it's more error-prone and token-heavy.

Patterns:
- Every `<section>` gets a unique `id`.
- Wrap main content in `<div class="content">` (flexbox fills vertical space). Use `class="section-divider"` for centered title slides, `<div class="footnote">` for attribution.
- Multi-column: use **inline CSS grid** (per-slide ratios vary), e.g. `style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 30px;"`. Do NOT make `.grid-2` utility classes.
- **All visible text must live in `<p>`, `<li>`, or `<h1>`–`<h6>`** so it inherits base styles. Use `<div>`/`<span>` only as layout containers, never for raw text.

### 5. Check overflow
```bash
node scripts/check-overflow.js presentation.html
```
Catches vertical/horizontal overflow per slide. Reduce content or font size where flagged. (Requires Puppeteer.)

### 6. Visual review — EVERY slide
Capture screenshots of all slides and Read each one. The `?export` param disables chart animations for cleaner PDFs.
```bash
npx decktape reveal "presentation.html?export" output.pdf \
  --screenshots --screenshots-directory "screenshots/$(date +%Y%m%d_%H%M%S)"
```
Re-capture specific slides after fixes with `--slides 2,5,7-9`. Look for: wrong color inheritance inside styled containers (light text on light container), bullet contrast on container backgrounds, missing Font Awesome icons (empty squares), overflow edge cases, unexpected text wrap (common in columns).

### 7. Suggest browser editing (mention at the end)
```bash
node <path-to-skill>/scripts/edit-html.js <presentation-dir>/presentation.html
```
Opens a local server; click any text to edit inline, Save writes back to file. Good for wordsmithing without touching HTML.

## Charts — read references/charts.md FIRST
Before adding ANY chart, read `references/charts.md` from the source. Charts need a flexbox container and `maintainAspectRatio: false` or they overflow:
```html
<section style="display: flex; flex-direction: column; height: 100%;">
  <h2>Chart Title</h2>
  <div style="flex: 1; position: relative; min-height: 0;">
    <canvas data-chart="bar">
    <!-- { "data": {...}, "options": { "maintainAspectRatio": false } } -->
    </canvas>
  </div>
</section>
```
charts.md covers layout patterns (full/half/quarter/unequal), all chart types (bar/line/pie/doughnut/scatter), styling, and a simpler CSV data format.

## Useful extras
- Built-in reveal.js classes: `r-fit-text`, `r-stretch`, `r-stack`.
- `Reveal.initialize({...})` options: `controls`, `progress`, `slideNumber`, `hash`, `transition` (none/fade/slide/convex/concave/zoom), `center` (default `false` = top-align; set `true` for minimal/creative decks), `autoSlide`, `loop`.
- Fragments, speaker notes, custom backgrounds, auto-animate, transitions: see `references/advanced-features.md`.

## Gotchas
- Font sizes in `pt`, never px/em/rem (except `--base-font-size`).
- Raw text outside `<p>/<li>/<hN>` renders at wrong size — wrap it.
- Don't generate the full HTML in one Write; Edit slide-by-slide.
- Always visually review every slide; the overflow script misses color/wrap/icon issues.
- Dependencies: Node.js, Puppeteer (overflow check), Decktape via npx (screenshots).
