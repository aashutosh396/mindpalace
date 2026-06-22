---
name: Mermaid Diagram to PNG
description: Use when you need to extract Mermaid diagrams from markdown and render them to high-quality PNG images — converts embedded mermaid code blocks into numbered, smartly-sized image files.
tags: [mermaid, diagram, png, markdown, render, mmdc, visualization, export]
source: daymade/claude-code-skills
derived_from: mermaid-tools
---

Extract Mermaid code blocks from a markdown file and generate high-resolution PNGs.

## Prerequisites
Verify before running:
- `mmdc --version` (mermaid-cli)
- `google-chrome-stable --version` (Chrome/Chromium for Puppeteer)
- `python3 --version`

## Core workflow
Run the bundled orchestrator from its own scripts dir (so it locates `extract_diagrams.py` + `puppeteer-config.json`):

```bash
cd "${CLAUDE_SKILL_DIR}/scripts"
./extract-and-generate.sh "<markdown_file>" "<output_directory>"
```
`<output_directory>` optional, defaults to `<markdown_dir>/diagrams`.

The script: extracts all mermaid blocks → numbers them sequentially (01, 02…) in document order → writes a `.mmd` + `.png` per diagram → validates each PNG.

## Custom dimensions / scaling
Override via env vars (`MERMAID_WIDTH` default 1200, `MERMAID_HEIGHT` default 800, `MERMAID_SCALE` default 2):

```bash
# presentation-grade
MERMAID_WIDTH=2400 MERMAID_HEIGHT=1800 MERMAID_SCALE=4 ./extract-and-generate.sh "file.md" "out/"
# print quality
MERMAID_SCALE=5 ./extract-and-generate.sh "file.md" "out/"
```

## Smart sizing (auto, from filename/diagram type)
- Timeline/Gantt → 2400×400 (wide, short)
- Architecture/System/Caching → 2400×1600
- Monitoring/Workflow/Sequence/API → 2400×800
- Default → 1200×800

## Troubleshooting
- Permission denied → `chmod +x extract-and-generate.sh`
- Low quality → bump `MERMAID_SCALE=3`
- Chrome/Puppeteer errors → verify all (WSL2) Chrome deps installed
- Always `cd` into scripts/ first; running elsewhere fails on missing deps.
