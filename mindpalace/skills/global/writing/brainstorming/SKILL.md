---
name: brainstorming
description: "Use when starting any creative or build work — a new feature, component, app, utility, config change, or behavior change — and before writing code: turn a rough idea into an approved design spec through one-question-at-a-time dialogue. Triggers: 'I want to build', 'let's design', 'help me think through', 'brainstorm', 'spec this out', 'new feature/project'."
version: 1.0.0
license: MIT
tags: [brainstorming, design, spec, requirements, planning, discovery, ideation, scoping, architecture]
source: https://github.com/obra/superpowers/tree/main/skills/brainstorming
derived_from: awesomeclaude
---

# Brainstorming Ideas Into Designs

Turn ideas into fully-formed designs and specs through natural, collaborative dialogue — BEFORE any implementation.

## When to use

Use before any creative work: creating features, building components, adding functionality, or modifying behavior. EVERY project goes through this — a todo list, a one-function utility, a config change. "Simple" projects are where unexamined assumptions waste the most work. Designs can be short, but you must present one and get approval.

## Hard gate

Do NOT invoke any implementation skill, write code, scaffold a project, or take any implementation action until you have presented a design AND the user has approved it. The only skill you invoke after brainstorming is a plan-writing skill — never jump straight to building.

## Checklist (do in order)

1. **Explore project context** — check files, docs, recent commits before asking anything.
2. **Assess scope early** — if the request spans multiple independent subsystems (chat + billing + storage + analytics), flag it and help decompose into sub-projects first. Don't refine details of something that needs splitting. Each sub-project gets its own spec → plan → build cycle.
3. **Ask clarifying questions — one at a time.** Prefer multiple-choice; open-ended is fine. One question per message. Focus on purpose, constraints, success criteria.
4. **Propose 2-3 approaches** with trade-offs. Lead with your recommendation and the reasoning.
5. **Present the design in sections**, each scaled to its complexity (a few sentences if simple, up to ~200-300 words if nuanced). Cover architecture, components, data flow, error handling, testing. Ask after each section whether it looks right. Revise until the user approves.
6. **Write the design doc** to `docs/specs/YYYY-MM-DD-<topic>-design.md` (or the user's preferred spec location) and commit it.
7. **Spec self-review** (see below) — fix inline.
8. **User reviews the written spec** — wait for approval; loop back on requested changes.
9. **Transition to implementation** — invoke a plan-writing skill to create the implementation plan. Do NOT invoke frontend-design, mcp-builder, or any other implementation skill directly.

## Design principles

- **Isolation & clarity** — break the system into small units, each with one clear purpose and a well-defined interface, understandable and testable independently. For each unit you should be able to say: what it does, how to use it, what it depends on. If you can't change internals without breaking consumers, the boundaries need work. A file growing large is a signal it's doing too much.
- **In existing codebases** — explore current structure first and follow existing patterns. Include only targeted improvements that serve the current goal (e.g. an oversized file you're touching). Do NOT propose unrelated refactoring.
- **YAGNI ruthlessly** — strip unnecessary features from every design.
- **Incremental validation** — get approval section-by-section; be ready to go back and re-clarify.

## Spec self-review (after writing the doc, fresh eyes)

1. **Placeholders** — any TBD/TODO/incomplete/vague requirements? Fix them.
2. **Internal consistency** — do sections contradict? Does architecture match the feature descriptions?
3. **Scope** — focused enough for a single plan, or does it need decomposition?
4. **Ambiguity** — could a requirement be read two ways? Pick one, make it explicit.

Fix inline; no need to re-review.

## User review gate

After the self-review passes, tell the user the spec is written and committed, ask them to review it, and wait. If they request changes, make them and re-run the self-review. Only proceed once approved.

## Visual companion (optional, just-in-time)

The source ships an optional browser-based companion for showing mockups, diagrams, and side-by-side visual options during brainstorming.

- Do NOT offer it upfront. Offer only the first time a question would genuinely be clearer SHOWN than told (a real mockup/layout/diagram question — not merely a UI *topic*). Make the offer its own message, then wait.
- Even after acceptance, decide per question: use the browser only for content that IS visual (mockups, wireframes, layout comparisons, architecture diagrams); use the terminal for text content (requirements, conceptual choices, trade-off lists, scope decisions).

Helper guide (not copied here): `skills/brainstorming/visual-companion.md` in the source repo.

## Gotchas

- Skipping the design because it "looks trivial" is the most common failure — don't.
- Asking several questions in one message overwhelms the user; strictly one at a time.
- Don't treat a UI *topic* as automatically a visual question.
- Terminal state is the plan-writing skill, nothing else.
