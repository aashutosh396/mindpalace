---
name: Markdown-HTML Design System (brand onboarding)
description: Use before any markdown→HTML conversion to capture brand identity once — a 10-question wizard validates body/link contrast against WCAG AA, derives a 12-token CSS-custom-property palette, and stores config that every converter (md-document/md-review/md-slides) consumes.
tags: [design-system, brand-palette, wcag, onboarding, customization, css-variables, typography, markdown-html, contrast]
source: alirezarezvani/claude-skills
derived_from: markdown-html/skills/design-system
---

# Design System — Onboarding + Shared Brand Tokens

The shared brand owner for the markdown→HTML toolchain. Run onboarding once; every converter reads the resulting config and applies the same 12 CSS custom properties. Without it, conversions render unbranded.

Three tools: `onboard.py` (interactive + `--defaults`/`--set`/`--show`/`--reset`/`--scope`), `config_loader.py` (project > global > defaults precedence; `MARKDOWN_HTML_NO_CONFIG=1` bypass), `brand_palette_validator.py` (WCAG-AA checker + HSL deriver).

## Onboarding question set (10)

| # | Key | Validator | Default |
|---|---|---|---|
| 1 | `default_output_dir` | writable parent | `./markdown-html-out/` |
| 2 | `brand.primary` | HEX `#[0-9a-fA-F]{6}` | `#0A1628` |
| 3 | `brand.accent` | HEX or blank (auto-derive) | derive from primary |
| 4 | `typography.heading_font` | Google Font (12 safe defaults) | `Inter` |
| 5 | `typography.body_font` | Google Font | `Inter` |
| 6 | `design_style` | editorial / technical / minimal / playful | `technical` |
| 7 | `code_theme` | light / dark / auto | `auto` |
| 8 | `toc.behavior` | sticky-sidebar / collapsible-top / inline / none | `sticky-sidebar` |
| 9 | `company_name` | string | `""` |
| 10 | `logo_url` | URL or empty | `""` |

## Hard rules

1. **WCAG AA contrast must pass** — body text on bg ≥4.5:1, link on bg ≥4.5:1. Fail → refuse to save (exit 4); pick a darker primary, blank bg/text to auto-derive, or override text directly.
2. **Output dir must be writable** (walk up to find existing ancestor + `os.W_OK`) — else exit 3.
3. **Customization must change behavior, not decorate** — every converter renders differently when design_style / brand.primary / code_theme / toc.behavior changes.
4. **Precedence fixed** — project > global > defaults; deep-merge preserves nested keys.
5. **Bypass env** `MARKDOWN_HTML_NO_CONFIG=1` is for headless CI/test only — never set silently for an interactive user.

## Derived 12-token palette

`--md-bg` (primary if dark, near-neutral if vibrant) · `--md-surface` (bg ±4-6% L) · `--md-border` (bg ±8-12% L) · `--md-text` (off-white on dark, near-black on light) · `--md-text-muted` (rgba text .68) · `--md-accent` · `--md-accent-soft` (rgba accent .14) · `--md-code-bg` · `--md-link` (walked to 4.5:1) · `--md-link-hover` · `--md-success` (green, L-matched) · `--md-warn` (amber, L-matched). Every converter inlines these into a `:root {}` block.

## Worked commands

```
onboard.py                                   # interactive 10-question
onboard.py --defaults                        # zero-touch (CI/first test)
onboard.py --set brand.primary=#FF6B35 --set design_style=editorial
onboard.py --scope project --set design_style=minimal   # per-repo override
onboard.py --reset && onboard.py             # reset + re-onboard
config_loader.py --show | --status           # inspect effective config
brand_palette_validator.py --primary "#FF6B35" --accent "#00D4AA"  # spot-check WCAG
```

## Non-goals

Not a full design-token system (12 tokens, not 100) · Google Fonts only (no custom-font hosting) · single-mode layout palette (`code_theme:auto` handles syntax dark/light) · not an a11y audit suite (enforces contrast only) · injects into fresh HTML, doesn't transform existing CSS.

Output: `~/.config/markdown-html/design-system.json` (global) or `./.markdown-html/design-system.json` (project).
