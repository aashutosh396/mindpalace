---
name: refactoring-ui
description: "Use when auditing or fixing web UI visual design — triggers: 'my UI looks off', 'fix the design', 'Tailwind styling', 'color palette', 'visual hierarchy', 'design system', 'spacing scale', 'component styling', dark mode themes, polishing UI before launch. Apply when generating frontend code or reviewing visual quality without a designer."
version: 1.0.0
license: MIT
tags: [ui-design, visual-hierarchy, spacing, typography, color, tailwind, design-system, frontend]
source: https://github.com/wondelai/skills/tree/main/refactoring-ui
derived_from: awesomeclaude
---

# Refactoring UI Design System

Practical, systematic UI design (Wathan & Schoger). Great UI is systems, not talent: constrained scales for spacing, type, color, and shadows produce professional results. Apply when generating frontend code, reviewing designs, or advising on visual improvements.

## Core Principle

**Design in grayscale first, add color last.** This forces real hierarchy through spacing, contrast, and typography instead of leaning on color. Start with too much white space and remove; leave details (icons, shadows, micro-interactions) until layout and hierarchy work.

## Scoring

Rate any UI 0-10 against the principles below. Always state the current score and the specific changes needed to reach 10/10.

## Seven Principles

### 1. Visual Hierarchy
Not everything can be important. Use three levers — size, weight, color — but combine, don't multiply (primary text = large OR bold OR dark, not all three).
- Labels are secondary: form labels, table headers, metadata should be smaller/lighter/uppercase-small.
- Button hierarchy: primary (filled), secondary (outlined/muted), tertiary (text only).
- Blur test: squint — if everything competes, increase primary/secondary contrast.

### 2. Spacing & Sizing
Use a constrained scale, never arbitrary px. Closer elements read as more related.
- Scale: 4, 8, 16, 24, 32, 48, 64px. (`p-1 p-2 p-4 p-6 p-8 p-12 p-16`)
- Start with too much white space, then remove — you'll never remove enough.
- Spacing between groups must exceed spacing within groups (`gap-2` related, `gap-6` separation).
- Constrain widths: text 45-75 chars (`max-w-prose` ~65ch), forms 300-500px. Full-width is rarely right.

### 3. Typography
Modular type scale, context-based line height, max two font families.
- Scale: 12, 14, 16, 20, 24, 30, 36px (~1.25 ratio).
- Headings tight (1.0-1.25); body relaxed (1.5-1.75); wider text needs more line height.
- Body weight ≥400; use 600-700 for emphasis only, not everything.
- `text-xs/sm/base/lg/xl`, `font-normal/medium/semibold/bold`, `leading-tight/normal/relaxed`.

### 4. Color
Systematic palette, 5-9 shades per color, design grayscale first.
- Each color: shades 50-900. Darkest is not pure black (`#111827`, not `#000`).
- Tint grays — pure grays look dead (cool: `#64748b`; warm: `#78716c`).
- HSL: lighter = raise lightness, drop saturation, hue toward 60°; darker = reverse.
- Contrast: 4.5:1 body, 3:1 large text. Use `text-gray-700`+ on white. Never color alone to convey meaning.
- Three text levels: `text-gray-900` / `gray-600` / `gray-400`.

### 5. Depth & Shadows
Shadow scale = elevation. Small (`shadow-sm`) for buttons, large (`shadow-lg/xl`) for dropdowns/modals.
- Good shadows have two parts: tight dark + larger soft. Shadow color is transparent dark, never opaque gray.
- Depth without shadows: lighter top border + darker bottom border, subtle gradients, overlap.
- Don't overuse — if everything floats, nothing has depth.

### 6. Images & Icons
Treat as design elements, not afterthoughts.
- Never stretch — `object-fit: cover` with fixed `aspect-ratio`, crop deliberately.
- Text over images needs a gradient overlay (`bg-gradient-to-t from-black/60`).
- Consistent icon sets, consistent stroke width. Sizes: `w-4` inline, `w-6` nav, `w-8` feature.
- Empty states: illustration + clear CTA, not bare text.

### 7. Layout & Composition
Don't center everything.
- Left-align by default; center only short headlines, heroes, single CTAs, empty states.
- Cards needn't contain everything — let images bleed to edges or overlap.
- Vary treatment in lists/feeds: feature some items, minimize others.
- `grid grid-cols-3 gap-6` feature grids; `max-w-4xl mx-auto` page containers.

## Common Mistakes → Fix
- "Looks amateur" → more white space, constrain widths.
- "Feels flat" → subtle shadows, border-bottom on sections.
- "Hard to read" → increase line-height, constrain width, boost contrast.
- "Everything looks the same" → vary size/weight/color (hierarchy).
- "Feels cluttered" → group related items, bigger gaps between groups.
- "Colors clash" → reduce saturation, more grays, limit to palette.
- Arbitrary values (13px, 17px) → stick to the spacing and type scales.

## Quick Diagnostic
Read hierarchy when squinting? Works in grayscale? Enough white space? Labels de-emphasized vs values? Spacing on a consistent scale? Text width constrained? Contrast WCAG-passing? Shadows match elevation? If any "no" → apply the matching principle above.
