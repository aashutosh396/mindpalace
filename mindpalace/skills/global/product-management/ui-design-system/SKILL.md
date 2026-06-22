---
name: UI Design System
description: Use when creating a design system, generating design tokens from a brand color, building typography/spacing scales, checking WCAG contrast, or preparing developer handoff — token generation and component architecture.
tags: [design-system, design-tokens, color-palette, typography-scale, wcag, css-variables, component-library, developer-handoff, ui]
source: alirezarezvani/claude-skills
derived_from: product-team/ui-design-system
---

# UI Design System

Generate design tokens, color palettes, type scales, component systems, and developer-handoff docs from a brand color.

## Workflow 1 — Generate Design Tokens

From brand primary (hex) + style (modern/classic/playful) emit categories: colors (primary/secondary/neutral/semantic/surface), typography (fontFamily/fontSize/fontWeight/lineHeight), spacing (8pt grid 0-64), borders (radius/width), shadows (none→2xl), animation (duration/easing), breakpoints (xs→2xl). Export CSS custom properties / SCSS / JSON (Figma Tokens Studio). **Validate accessibility** — WCAG AA (4.5:1 normal, 3:1 large), semantic colors have contrast colors defined.

### Color scale generation

50-400 hold brightness ~95%, climb saturation 30→62%; 500 = base/original; 600-900 darken brightness (×0.8/0.6/0.4/0.2) and push saturation to 100% (used for hover/active/text/headings).

### Type scale (1.25× ratio)

xs 10 · sm 13 · base 16 · lg 20 · xl 25 · 2xl 31 · 3xl 39 · 4xl 49 · 5xl 61 px.

### Style presets

Modern: Inter / Fira Code / 8px radius / layered subtle shadows. Classic: Helvetica / Courier / 4px / single-layer. Playful: Poppins / Source Code Pro / 16px / soft pronounced.

## Workflow 2 — Component System

Hierarchy (atomic): Atoms (Button/Input/Icon/Label/Badge) → Molecules (FormField/SearchBar/Card/ListItem) → Organisms (Header/Footer/DataTable/Modal) → Templates (DashboardLayout/AuthLayout). Map tokens to components. Variants: size (sm 32px / md 40px / lg 48px), color (primary/secondary/ghost). Document props interface, variants, states (hover/active/focus/disabled), accessibility.

## Workflow 3 — Responsive

Breakpoints: xs 0 / sm 480 / md 640 / lg 768 / xl 1024 / 2xl 1280px. Fluid typography via `clamp(min, preferred, max)` — e.g. `--fluid-h1: clamp(2rem, 1rem + 3.6vw, 4rem)`. Responsive spacing scales per breakpoint.

## Workflow 4 — Developer Handoff

Export tokens (CSS/SCSS/JSON), wire framework integration (React+CSS vars, Tailwind config from JSON, styled-components), sync Figma (Tokens Studio plugin). Checklist: token files added, build pipeline configured, theme imported, component library aligned, docs generated.

## WCAG Contrast

AA: 4.5:1 normal, 3:1 large. AAA: 7:1 normal, 4.5:1 large. Large = ≥18pt regular or ≥14pt bold.

## Validation Checklists

- **Tokens** — hex brand color, style matches project, all categories generated, semantic colors have contrast values.
- **Components** — all sizes, all variants, all states, only design tokens (no hardcoded values).
- **Accessibility** — contrast AA, visible focus indicators, touch targets ≥44×44px, semantic HTML.
