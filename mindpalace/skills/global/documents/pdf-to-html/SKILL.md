---
name: PDF to Readable HTML (with optional translation)
description: Use when someone wants to read a PDF as a web page or clean document, convert a PDF to a styled self-contained HTML, or translate a PDF into another language while keeping its images/tables/charts intact.
tags: [pdf, html, convert, translate, pymupdf, readable, reflow, document, figures]
source: daymade/claude-code-skills
derived_from: pdf-to-html
---

Turn a PDF into one self-contained, readable HTML file — images, tables, charts, and reading order preserved — and optionally translate it while keeping every figure in place.

Pipeline: **extract → look → (translate) → build → verify**. The "look" and "verify" steps are where fidelity comes from: a PDF is a layout, not a text stream — read the rendered pages before building and the rendered HTML before delivering. Run inline (translation orchestrates a workflow; a subagent can't spawn one).

## When NOT to use
- Scanned/image-only PDFs (no text layer) → OCR first (e.g. `ocrmypdf`).
- Complex grid tables → cell text preserved but grid may flatten; use a Markdown converter (pandoc rebuilds real tables) if grid structure is essential.
- Pixel-perfect facsimile → output is a clean reflow, not a 1:1 copy.
- Rewriting/summarizing → it translates+re-lays-out only; fidelity is the point.

## Dependencies
`uv`, Google Chrome/Chromium. Python deps via `uv run --with`: PyMuPDF, Pillow, numpy.

## Workflow (checklist)
```
- [ ] 1. Extract structure + render pages
- [ ] 2. Read pages/*.png — SEE layout, content vs decorative images
- [ ] 3. (only if translating) run translation workflow
- [ ] 4. Build single-file HTML
- [ ] 5. Verify visually (Read every segment)
- [ ] 6. Deliver the .html
```

1. **Extract:** `uv run --with pymupdf python scripts/extract_pdf.py input.pdf` → `input-build/` with `structure.json` (text blocks + font sizes, image blocks flagged `decorative`), `images/`, `pages/` (one PNG/page).
2. **Look:** Read `pages/*.png` — confirm content vs decoration images, spot tables/charts, understand the doc. Not optional.
3. **Translate (optional):** only if asked. A Dynamic Workflow translates pages in parallel, captions data charts, reconciles terminology → produces `units.json` + `caps.json`. Never hand-translate inline beyond a page.
4. **Build:** `uv run --with Pillow python scripts/build_html.py input-build/structure.json --out output.html` (add `--translation units.json --captions caps.json --lang zh-CN` for translated). Data-driven: infers heading levels from font size, drops decorative images, inlines content images as compressed base64 → one portable file. Edit the short script per-document for unusual layouts.
5. **Verify (mandatory):** `uv run --with Pillow --with numpy python scripts/verify_render.py output.html`, then Read every `seg-*.png` — fonts render (no tofu), no clipped tables/figures, all images present. Correct text ≠ correct render. Count figures with `grep -o '<figure>' output.html | wc -l` (NOT `grep -c`).
6. **Deliver:** the single `.html` opens with a double-click; nothing can go missing.

## Fidelity (read before translating)
The deliverable looks authoritative, so wrong content is worse than ugly content. **Never give a real person an inferred translated name; copy every number/proper-noun verbatim.**
