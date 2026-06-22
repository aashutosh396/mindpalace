---
name: md-review (Code review markdown → 2-col HTML)
description: Use when converting a markdown PR writeup or code review (```diff blocks + severity callouts `> [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]`) into a single-file 2-column HTML review — diff left, severity-tagged annotation cards right, top jump-nav, mandatory named reviewer. Refuses without a reviewer or with no diff hunks.
tags: [markdown, html, code-review, diff, severity, annotations, single-file, pr-writeup, wcag, jump-nav]
source: alirezarezvani/claude-skills
derived_from: markdown-html/skills/md-review
---

# md-review — Code-review markdown → 2-column HTML

Takes a markdown PR writeup with diff blocks + severity callouts, produces a single-file HTML review. Pipeline: **parse diff hunks → extract annotations → render 2-col HTML**.

1. **diff_parser** — scan ```diff fenced blocks, parse unified diff (`--- a/file`, `+++ b/file`, `@@ -10,7 +10,8 @@`, ` `/`+`/`-` lines), assign per-line old/new numbers, preserve hunk headers. `--infer-diff` for unfenced blocks.
2. **annotation_extractor** — extract GFM severity callouts (`> [!BLOCKER]`) + inline markers (`nit:`, `blocker:`). Default convention BLOCKER/MAJOR/MINOR/NIT (Google Code Review Developer Guide); override via `--severity-convention "critical,important,suggestion,nit"` (position 0 = most severe). Attach each to the nearest preceding hunk; unanchored → general-comments section. Capture `LGTM`/`approved` separately.
3. **review_html_renderer** — single-file 2-col HTML.

## What gets rendered

- **Top jump-nav** — every annotation with severity badge + 80-char preview + jump link; severity counts in heading ("3 BLOCKER · 2 MAJOR · 1 NIT").
- **2-col hunk rows** — diff left (per-line old/new numbers, +/− marks, addition/deletion bg tint from design-system tokens), annotation cards right (color + icon + aria-label per WCAG 1.4.1).
- **Approval bar** — surfaces when LGTM markers present and no findings.
- **General comments** — unanchored annotations at the bottom.
- **Reviewer footer** — mandatory.
- Collapses to stacked on viewports < 900px.

## Hard rules

1. **`--reviewer` is mandatory** (a code review must name a human) — refuse with exit 3 otherwise.
2. **Refuse if no hunks** (`--- a/file` + `@@`) — exit 4, recommend md-document.
3. Refuse input < 100 lines (Shihipar threshold).
4. Refuse without design-system onboarding.
5. **Severity never color-only** — each badge ships color + icon + aria-label + text (WCAG 1.4.1 at renderer level).
6. Single-file output — all CSS inline; only external is Google Fonts CSS. No Prism (diff coloring conflicts with syntax highlighting).

## Forcing questions

1. Who is the named reviewer? (The person signing off.)
2. Which severity convention — default or custom? (Default unless documented alternative.)
3. Annotations anchored to hunks or general? (Anchor everything you can.)
4. What's the PR title for `<title>` + header? (The actual PR/commit title.)
5. Ship LGTM markers as the approval bar? (Yes if no severity annotations.)

Distinct from md-document (prose/tables/callouts), md-slides (split into slides), GitHub PR comments (a thread vs single-author snapshot). Output: `{output_dir}/review-{slug}.html`.
