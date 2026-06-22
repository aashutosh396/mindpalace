---
name: PPT / Slide Deck Creator
description: Use when asked to make, improve, or convert content into a presentation, pitch, slide deck, or keynote — produces a structured, persuasive deck with charts, speaker notes, and PPTX output.
tags: [presentation, slides, ppt, pptx, deck, pitch, keynote, charts, speaker-notes, marp]
source: daymade/claude-code-skills
derived_from: ppt-creator
---

Transform a topic or scattered materials into a presentation-ready deck. Missing info → apply safe defaults, don't block.

## Quick start
1. **Gather intent** (10 minimal questions; default if unanswered after 2 prompts): audience (general), objective (understand+accept), desired action (move to next step), duration/count (15-20min, 12-15 slides), tone (professional/clear/friendly), scope (topic +1 layer), must-include/taboos (none), data (none → placeholder+field list), brand (neutral theme), format (slides.md + optional PNG + PPTX).
2. **Structure the story (Pyramid Principle):** one conclusion → 3-5 top-level reasons → supporting evidence. Each slide = **one core idea**, with an **assertion-style heading** (a testable complete sentence, not a topic label).
3. **Evidence-first:** charts/tables/evidence blocks over paragraphs; 3-5 bullets max per slide; ≤70 words per slide.
4. **Choose charts** from a chart-selection dictionary (question type → chart). If user gives data, render PNGs; else placeholder + required-field list. Label axes/units/source.
5. **Style/accessibility:** 16:9, safe margins ≥48px; headings 34-40 / body 18-22 / footer 14-16; WCAG AA contrast (text ≥4.5:1, UI ≥3:1); alt text on charts/images.
6. **Speaker notes:** 45-60s per slide — opening → assertion → evidence → transition.

## Workflow stages
0. Archive input (original request, defaults used, assumptions).
1. Rewrite goal as "who takes what action when" (clear CTA).
2. Storyline via Pyramid Principle.
3. Outline: 12-15 slide skeleton, one assertion heading each.
4. Evidence & charts (render or placeholder).
5. Layout & accessibility; unify units/decimals.
6. Speaker notes.
7. **Self-check & score (RUBRIC, 100pts, ≥75 to ship):** goal clarity, story structure, slide assertions, evidence quality, chart fit, visual/accessibility, coherence/transitions, speakability, deliverables complete, robustness. If <75, fix weakest 3 items, re-score (max 2 iterations).
8. Package deliverables.
9. Append "5-step replace-your-data guide".

## Deliverables (to /output/)
- `slides.md` (Marp/Reveal-compatible: assertion headings + bullets/chart placeholders + notes)
- `assets/*.png` (charts, if data given)
- `notes.md` (full speaker notes + delivery outline)
- `refs.md` (citations/sources)
- `presentation.pptx` (if python-pptx available; else keep markdown + one-click-convert instructions — do NOT block delivery)

## Core principles
Conclusion first then evidence; one idea per slide; testable assertion headings; charts labeled with axes/units/source; AA contrast + alt text; consistent naming/reproducible paths; never scrape web without permission; if matplotlib/pandas unavailable, fall back to text + placeholder.
