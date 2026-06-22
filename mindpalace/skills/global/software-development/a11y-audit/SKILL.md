---
name: Accessibility (a11y) Audit
description: Use when auditing or fixing web accessibility — scans for WCAG 2.2 A/AA violations, classifies severity, generates framework-specific before/after fixes (React/Vue/Angular/Svelte/HTML), checks color contrast, and verifies no regressions.
tags: [accessibility, a11y, wcag, contrast, aria, keyboard-navigation, screen-reader, audit, react]
source: alirezarezvani/claude-skills
derived_from: engineering-team/a11y-audit
---

# Accessibility (a11y) Audit

Three-phase WCAG 2.2 Level A & AA pipeline: **Scan → Fix → Verify**. Auto-detects framework (React/Next/Vue/Angular/Svelte/HTML); produces exact before/after fixes.

## Phase 1 — Scan
Walk the source tree, detect framework, apply WCAG 2.2 A+AA rule set. Categorize each violation:
| Severity | Definition | SLA |
|---|---|---|
| Critical | Blocks an entire user group (missing alt, no keyboard nav) | before release |
| Major | Degrades experience (low contrast, missing form label) | current sprint |
| Minor | Friction (redundant ARIA, bad heading order) | next 2 sprints |

## Phase 2 — Fix (before/after, per framework)
Worked React example fixes: `<img>` missing `alt` (1.1.1); `<div onClick>` not keyboard-accessible → use `<a>`/`<button>` (2.1.1); colors failing 4.5:1 contrast (1.4.3) → darken to AA-passing values; interactive element missing accessible name (4.1.2) → add `aria-label`.

## Phase 3 — Verify
Re-run scan against a baseline JSON; confirm fixes resolved and no new regressions. CI mode: non-zero exit on Critical issues.

## Contrast targets
AA: 4.5:1 normal text, 3:1 large text. AAA: 7:1. Suggest accessible alternatives for failures.

## Common pitfalls → correct approach
- `role="button"` on `<div>` → native `<button>` (free keyboard handling)
- `aria-label` on non-interactive elements → `aria-labelledby` to visible text
- `display:none` to hide from SR → `.sr-only` class
- color alone to convey meaning → add icon/text/pattern
- placeholder as only label → visible `<label>`
- `outline:none` without replacement → `:focus-visible` indicator
- skipped heading levels (h1→h3) → sequential
- `onClick` without `onKeyDown` → keyboard support or native element
- ignoring `prefers-reduced-motion` → wrap animations in `@media (prefers-reduced-motion: no-preference)`

## Integrate into CI/CD (GitHub Actions, GitLab CI, pre-commit) to prevent regressions. Output stakeholder reports with pass/fail summaries per success criterion.

Resources: WCAG 2.2 spec, WAI-ARIA Authoring Practices 1.2, axe-core rules, eslint-plugin-jsx-a11y.
