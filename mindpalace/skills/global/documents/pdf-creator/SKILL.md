---
name: Markdown to PDF Creator (CJK-aware)
description: Use when converting Markdown to a professional PDF, generating printable/mobile-readable documents, or any markdown→PDF with proper Chinese font support — handles CJK typography and mandatory visual verification.
tags: [pdf, markdown, weasyprint, chrome, cjk, chinese-fonts, print, mobile, themes, convert]
source: daymade/claude-code-skills
derived_from: pdf-creator
---

Create professional PDFs from Markdown with CJK font support, a theme system, and mandatory visual self-check. Scope: **markdown → PDF only** (for .docx use a different tool).

## Quick start
```bash
uv run --with weasyprint scripts/md_to_pdf.py input.md output.pdf          # default (formal, A4)
uv run --with weasyprint scripts/md_to_pdf.py input.md --theme warm-terra  # training/course
uv run --with weasyprint scripts/md_to_pdf.py input.md --theme mobile      # phone/WeChat reading
uv run --with weasyprint scripts/batch_convert.py *.md --theme warm-terra --no-preview
python scripts/md_to_pdf.py --list-themes dummy.md
```

## Themes (themes/*.css)
- `default` — A4, Songti+Heiti SC, black/grey → legal/contracts/formal.
- `cjk-auto` — A4 → tables with uneven column content.
- `warm-terra` — A4, PingFang SC, terracotta → course outlines/workshops.
- `mobile` — 148×210mm, 15px, 1.9 line-height → phone reading.
Default rule: warm-terra for training, default for formal docs.

## Backend (auto-selected by content)
- **CJK content → Chrome** (weasyprint subset-embeds PingFang SC as CID Type 0C OpenType, which macOS Preview/Adobe fail to render → garbled on recipient devices).
- **Non-CJK → weasyprint** (faster, no browser).
Override with `--backend chrome|weasyprint`.

## Anti-pattern: do NOT hand-run pandoc + Chrome
Manual `pandoc → chrome --headless --print-to-pdf` fails silently: no CJK CSS → boxes; default Chrome header/footer appears; no post-render check; no theme system. Always use this skill.

## Visual self-check (MANDATORY)
After every run the script renders each page to PNG (via `pdftoppm`, into system temp dir) and prints `Previews: <path>/page-NN.png`. **Read each page-NN.png and verify against the markdown source.** Common silent failures: paragraphs collapsing (CommonMark soft-break), tables overflowing margins, missing CJK/emoji glyphs, code garbling, Chrome headers/footers. If wrong, fix the markdown (real `- ` lists, blank lines, restructured tables) and rerun — the script does NOT silently fix non-standard markdown. Disable with `--no-preview` for batch. Requires `pdftoppm` (`brew install poppler`).

## CJK typography (automatic, never edits user source)
- Layer 1 CSS patch: `table-layout: fixed`, `word-break: keep-all`, `th { white-space: nowrap }` — fixes ~80% of CJK cell-wrap anti-patterns.
- Layer 2 lint: post-render `pdftotext -layout` scan for single-char lines, broken bracket pairs, mid-thought punctuation orphans → warnings (not errors); author decides accept/shorten/restructure.

## Troubleshooting
Chinese as boxes → install Songti/PingFang SC. weasyprint import error → use `--backend chrome`. Inline mixed CJK+ASCII blanks in Preview → font chain prioritizes CID TrueType (Songti/Heiti) before OpenType (PingFang). Table col-1 mid-break → default theme neutralizes pandoc's `<colgroup>` width hint.
