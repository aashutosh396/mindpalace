---
name: UI Designer (design-system extraction)
description: Use when a user provides UI screenshots/mockups and wants a design system extracted plus implementation-ready UI prompts — analyzes visual patterns, generates design-system docs + PRD, composes a final React/Tailwind prompt.
tags: [ui-design, design-system, mockup-analysis, color-palette, typography, prd, react, tailwind, ui-prompt]
source: daymade/claude-code-skills
derived_from: ui-designer
---

# UI Designer

Extract a design system from reference UI images, then produce implementation-ready UI prompts. Multi-step: analyze → design-system doc → PRD → final prompt → implement.

## When
User has UI screenshots/mockups; needs color/typography/spacing extracted; wants design-system docs; building MVP UI matching a reference; multiple consistent variations.

## Workflow
1. **Gather inputs**: reference images dir, project idea file, optional existing PRD.
2. **Extract design system** (Task tool + general-purpose subagent, attach images, use `assets/design-system.md` template): color palette (primary/secondary/accent/functional/backgrounds), typography (families/sizes/weights/line-heights), component styles (buttons/cards/inputs/icons), spacing (4-48dp), animations, dark-mode variants. Use specific values (hex, px), not generic descriptions. Save to `documents/designs/{dir}_design_system.md`.
3. **Generate PRD** (if none): Task subagent + `assets/app-overview-generator.md` — elevator pitch, problem, audience, USP, features w/ user stories, UX/UI per screen. Refine interactively with user.
4. **Compose final prompt**: combine design system + PRD via `assets/vibe-design-template.md` (substitute design guide + PRD). Result = aesthetic principles + project color/typography + features + tasks (multiple variations, component structure). Save to `documents/ux-design/{name}_design_prompt_{timestamp}.md`.
5. **Verify React env**: `find . -name package.json -exec grep -l react {} \;`; if none, guide create-react-app + tailwind + lucide-react.
6. **Implement UI**: use final prompt — multiple variations (3 mobile, 2 web), separate components `[solution]/pages/[page].jsx`, aggregate in a showcase page.

## Best practices
Read all images before analysis; find patterns across screens; capture explicit (colors/fonts) + implicit (spacing/hierarchy); include hover/disabled states + dark mode. Engage user interactively on PRD ambiguity; keep MVP scope realistic. Save with descriptive/timestamped filenames in `documents/`; preserve intermediate outputs for iteration. High-freedom workflow — adapt steps; templates structure but encourage real analysis.
