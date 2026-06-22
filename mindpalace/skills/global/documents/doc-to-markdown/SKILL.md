---
name: Document to Markdown Converter
description: Use when converting DOCX/PDF/PPTX/XLSX to high-quality Markdown — orchestrates pandoc/pymupdf/markitdown plus automatic DOCX post-processing (tables, image paths, CJK bold spacing, code blocks).
tags: [markdown, docx, pdf, pptx, convert, pandoc, markitdown, pymupdf, document, cjk]
source: daymade/claude-code-skills
derived_from: doc-to-markdown
---

Convert documents to high-quality Markdown via multi-tool orchestration. Architecture: **pandoc (best-in-class extraction) + 8 post-processing fixes**.

## Quick start
```bash
# DOCX → Markdown (zero manual fixes)
uv run --with pymupdf4llm --with markitdown scripts/convert.py document.docx -o output.md --assets-dir ./media
# PDF → Markdown
uv run --with pymupdf4llm --with markitdown scripts/convert.py document.pdf -o output.md
```

## Modes & tool selection
- **Quick** (default): fast, good for drafts/simple docs.
- **Heavy**: slower, best for final/complex — runs multiple tools in parallel, parses each output into segments, scores them, merges the best per segment.

| Format | Quick | Heavy |
|--------|-------|-------|
| PDF | pymupdf4llm | pymupdf4llm + markitdown |
| DOCX | pandoc + post-processing | pandoc + markitdown |
| PPTX | markitdown | markitdown + pandoc |
| XLSX | markitdown | markitdown |

Merge criteria: tables (more rows/cols, proper header sep), images (alt text + local paths), headings (proper hierarchy), lists (more items, nested preserved), paragraphs (completeness).

## DOCX post-processing (automatic, 8 fixes)
Grid tables → blockquote/pipe table; simple tables → pipe table w/ captions; nested image paths (`media/media/`) → flattened relative; pandoc attributes (`{width=...}`) removed; **CJK bold spacing** (add space around `**` for CJK spans so renderers recognize bold); indented dashed code → fenced + language detect; escaped brackets `\[...\]` → `[...]`; double-bracket links → single.

## Image extraction
```bash
uv run --with pymupdf scripts/extract_pdf_images.py document.pdf -o ./extracted-images
uv run --with pymupdf scripts/extract_pdf_images.py document.pdf --markdown refs.md
```

## Quality validation
```bash
uv run --with pymupdf scripts/validate_output.py document.pdf output.md --report report.html
```
Thresholds: text retention >95% pass / <85% fail; table & image retention 100% pass.

## Common issues
- "No conversion tools available" → `pip install pymupdf4llm; uv tool install "markitdown[pdf]"; brew install pandoc`.
- FontBBox warnings → harmless.
- Images missing / tables broken → use Heavy Mode (selects most complete version) or extract/validate separately.
