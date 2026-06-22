---
name: md-slides (Markdown deck → HTML presentation)
description: Use when converting a markdown deck (slides split by `---` HR or `# ` H1, optional `<!-- notes: -->` blocks) into a single-file HTML presentation with keyboard nav, presenter mode, URL-hash deep links, and print-to-PDF. Refuses 1-slide decks or input with no clear boundaries.
tags: [markdown, html, slides, deck, presenter-mode, keyboard-nav, print-to-pdf, single-file, presentation]
source: alirezarezvani/claude-skills
derived_from: markdown-html/skills/md-slides
---

# md-slides — Markdown deck → single-file HTML presentation

Reads a markdown deck (HR or H1 boundaries, optional presenter notes), emits a single-file HTML presentation that runs in any browser. Pipeline: **split slides → parse presenter notes → render deck HTML**.

1. **slide_splitter** — split on `---` HR or `# ` H1 (auto: HR wins ≥3, else H1 ≥5). First heading per slide = title.
2. **presenter_notes_parser** — extract `<!-- notes: ... -->` (also `speaker-notes:`/`presenter:`) per slide, strip from body, track coverage %.
3. **deck_html_renderer** — single-file HTML deck.

## What ships in the HTML

- All slides as `<section class="slide">`, one visible at a time (JS-controlled).
- **Keyboard nav** — `→`/`Space`/`PgDn` advance; `←`/`PgUp` previous; `Home`/`End` jump; `P` presenter mode; `Esc` exits presenter.
- **URL-hash deep linking** — `#3` jumps to slide 3; browser back/forward walks slides; share `deck.html#5`.
- **Progress bar** (3px top) + **slide counter** (bottom-right "3 / 12").
- **Presenter mode** (P) — split view: current slide left (60%), panel right (clock + speaker notes + next-slide preview).
- **Print stylesheet** — `@media print { section { display:block; page-break-after:always } }` → `Cmd+P` = one slide per page PDF.
- `prefers-reduced-motion` honored; 12 brand CSS custom properties from design-system; reuses md-document's markdown parser for slide bodies.

## Hard rules

1. Refuse no-boundary input (auto needs ≥3 HR or ≥5 H1) → route to md-document.
2. Refuse 1-slide decks (it's a poster).
3. Refuse input < 100 lines (Shihipar threshold).
4. Refuse without design-system onboarding.
5. `--strict-notes` refuses < 50% notes coverage (not set up for presenter mode).
6. Soft-warn slides > 40 source lines (signal-to-noise; renders anyway).
7. Single-file output — all CSS+JS inline; only external is Google Fonts CSS; Prism.js opt-in via `--syntax`.
8. Vanilla JS only, no framework runtime.

## Forcing questions

1. Is this actually a deck or a long document? (If you can't draw clear boundaries, it's not a deck.)
2. HR (`---`) or H1 boundaries? (HR for typical decks; H1 for outline-driven.)
3. Presented live or self-paced? (Live → need presenter notes.)
4. Any slide over 40 source lines? (Split it — attention drops past ~6 bullets / 200 words.)
5. Is `--syntax` needed? (Only for substantial code blocks; default off.)

Distinct from md-document (one continuous doc), md-review (diff hunks), and Keynote/PowerPoint (graphic-design tools). Output: `{output_dir}/deck-{slug}.html`.
