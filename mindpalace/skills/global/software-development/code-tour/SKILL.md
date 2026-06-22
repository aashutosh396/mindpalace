---
name: Code Tour Author
description: Use when asked to create a CodeTour walkthrough — onboarding tour, architecture tour, PR-review tour, RCA tour, or any persona-targeted step-by-step code walkthrough with real file/line anchors.
tags: [codetour, walkthrough, onboarding, code-tour, architecture-tour, pr-review, rca, contributor-guide, vscode]
source: alirezarezvani/claude-skills
derived_from: engineering/code-tour
---

# Code Tour Author

Create `.tour` JSON files (VS Code CodeTour extension) — persona-targeted, step-by-step walkthroughs that link to real files and line numbers. A great tour is a narrative told to a specific person about what matters and why. Only create `.tour` files; never modify source.

## Workflow

1. **Discover the repo** — in parallel: list root, read README, check configs. Identify language/framework/purpose, map folders 1-2 levels deep, find entry points. Every path in the tour must be real. <5 source files → make a quick-depth tour regardless of persona.

2. **Infer intent silently** (one message is enough):

| User says | Persona | Depth |
|---|---|---|
| "tour for this PR" | pr-reviewer | standard |
| "why did X break" / "RCA" | rca-investigator | standard |
| "onboarding" / "new joiner" | new-joiner | standard |
| "quick tour" / "vibe check" | vibecoder | quick |
| "architecture" | architect | deep |
| "security" / "auth review" | security-reviewer | standard |
| (no qualifier) | new-joiner | standard |

3. **Read actual files** — verify every path and line number. A tour pointing at the wrong line is worse than no tour.

4. **Write the tour** to `.tours/<persona>-<focus>.tour`:
```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Descriptive Title — Persona / Goal",
  "description": "Who this is for and what they'll understand after.",
  "ref": "<current-branch-or-commit>",
  "steps": []
}
```

**Step types:** Content (intro/closing, max 2) · Directory (orient to a module) · File+line (the workhorse) · Selection (highlight a block) · Pattern (regex for volatile files) · URI (link to PR/issue/doc).

**Step count:** quick 5-8 · standard 9-13 · deep 14-18.

**Description formula (SMIG):** Situation (what they look at) → Mechanism (how it works) → Implication (why it matters for this persona) → Gotcha (what a smart person gets wrong).

5. **Validate:** every file path repo-root-relative (no leading `/` or `./`) and confirmed to exist; every line verified; first step has a file/directory anchor; ≤2 content-only steps; `nextTour` matches another tour's title exactly.

## Narrative arc
Orientation (file/dir step, never content-only first) → high-level map (1-3 directory steps) → core path (file/line steps, the heart) → closing (what the reader can now *do*, not a recap).

## Anti-patterns
File listing instead of story · generic descriptions (name the pattern unique to *this* codebase) · guessed line numbers · too many steps for quick depth · hallucinated files · recap closings · content-only first step.
