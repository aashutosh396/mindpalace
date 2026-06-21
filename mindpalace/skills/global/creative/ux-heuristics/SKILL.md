---
name: ux-heuristics
description: "Use when evaluating or improving interface usability — triggers: 'usability audit', 'UX review', 'users are confused', 'heuristic evaluation', 'form usability', 'navigation problems', 'Nielsen heuristics', 'cognitive walkthrough', 'usability testing', improving form completion, evaluating information architecture and navigation."
version: 1.0.0
license: MIT
tags: [usability, ux-audit, nielsen-heuristics, navigation, forms, accessibility, dark-patterns, severity-rating]
source: https://github.com/wondelai/skills/tree/main/ux-heuristics
derived_from: awesomeclaude
---

# UX Heuristics Framework

Krug + Nielsen usability principles for auditing and improving UIs. Users don't read, they scan; they don't make optimal choices, they satisfice; they muddle through.

## Core Principle

**"Don't Make Me Think"** — every page should be self-evident. If something requires thinking, it's a usability problem. Design for scanning, satisficing, and muddling through.

## Scoring

Rate any interface 0-10 against the principles below. State the current score and specific fixes to reach 10/10.

## Krug's Laws
1. **Don't make me think.** Clear names beat clever names; plain language beats marketing-speak. If a label needs explanation, simplify it. CTAs = verb + noun ("Create account").
2. **Clicks don't matter — confidence does.** Users abandon when they lose confidence, not when they run out of clicks. Three painless obvious clicks beat one click that needs deliberation. Use step indicators ("Step 2 of 4").
3. **Get rid of half the words.** Cut happy-talk ("Welcome to our website!"), polite fluff, instructions nobody reads. "Enter your password to continue" not a sentence about proceeding to the next step.
4. **The Trunk Test.** Dropped on any random page, a user should instantly answer: what site? what page? major sections? my options? where am I? where's search? Persistent logo, descriptive page titles, breadcrumbs, findable search.

## Nielsen's 10 Heuristics
1. **Visibility of system status** — timely feedback; "Saving..." → "Saved"; no silent failures.
2. **Match real world** — users' language ("Sign in" not "Authenticate"), real metaphors, natural ordering.
3. **User control & freedom** — clear exits; undo beats "Are you sure?"; back must never break.
4. **Consistency & standards** — same word/style/behavior throughout; one term per concept; follow platform conventions.
5. **Error prevention** — constrained inputs (date pickers), autocomplete, sensible defaults, unsaved-changes warnings.
6. **Recognition over recall** — show options, don't make users remember; breadcrumbs, recent searches, pre-filled fields.
7. **Flexibility & efficiency** — shortcuts, bulk actions, command palette (Cmd+K), progressive disclosure for novice + expert.
8. **Aesthetic & minimalist** — every element earns its place; one primary CTA per page.
9. **Recognize/diagnose/recover from errors** — say what happened, why, and how to fix; plain language; never blame the user; preserve their input.
10. **Help & documentation** — searchable, task-focused, contextual (tooltips, inline hints).

## Severity Rating
0 Not a problem · 1 Cosmetic (fix if time) · 2 Minor (schedule) · 3 Major (fix soon) · 4 Catastrophic (fix now). Weigh frequency × impact × persistence.

## Common Mistakes → Fix
- Mystery-meat nav (icons only) → add text labels.
- Too many choices → reduce to ~7±2.
- No "you are here" → highlight current nav + breadcrumb.
- No inline validation → validate on blur with specific messages.
- Wall of text → headings, bullets, whitespace.
- Jargon labels → plain language, user-test.
- No loading indicators → spinner/progress/skeleton.
- Tiny tap targets → minimum 44×44px.
- Hover-only info → don't hide critical info behind hover.
- No undo → provide undo for non-destructive actions.
- Low contrast → WCAG AA (4.5:1).
- Broken back button → never hijack browser history.

## Heuristic Conflicts
Simplicity vs flexibility → progressive disclosure. Consistency vs context → consistent patterns, contextual prominence. Efficiency vs error prevention → prefer undo over confirmation dialogs. Discoverability vs minimalism → primary actions visible, secondary hidden.

## Dark Patterns (avoid)
Forced continuity (hard to cancel), roach motel (easy in, hard out), confirmshaming, hidden costs at checkout. These deliberately violate heuristics to manipulate — never use them.

## Method Selection
Heuristic evaluation (1-2h, before user testing) → user testing (real behavior) → A/B testing (statistical validation) → analytics review (ongoing patterns).
