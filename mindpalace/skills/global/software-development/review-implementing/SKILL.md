---
name: review-implementing
description: "Use when implementing code review feedback — user pastes reviewer comments, PR review notes, or says 'address these comments', 'implement the feedback', 'apply review suggestions', 'fix the review notes' — to systematically parse, track, and resolve each requested change."
version: 1.0.0
license: MIT
tags: [code-review, pr-feedback, review-comments, todowrite, refactoring, testing, workflow, implementation]
source: https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/review-implementing
derived_from: awesomeclaude
---

# Review Feedback Implementation

Systematically process and implement changes from code review feedback so nothing
gets dropped and each reviewer comment is verifiably addressed.

## When to use

- User provides reviewer comments or PR review notes
- User says "address these comments" / "implement feedback" / "apply review suggestions"
- User shares a list of changes requested by reviewers
- Any time you must turn unstructured review prose into concrete code changes

## Workflow

### 1. Parse reviewer notes into discrete items
- Split numbered lists (1., 2., …) and bullet points into individual change requests
- Extract each distinct ask; clarify ambiguous items BEFORE starting work
- Conflicting feedback → ask the user to resolve, explaining the conflict clearly

### 2. Build a todo list (TodoWrite)
- Each feedback item → one or more actionable, specific, measurable todos
- Break complex feedback into smaller tasks
- Exactly ONE todo `in_progress` at a time; mark the first before starting

### 3. Implement each todo
- Locate code: Grep for functions/classes, Glob for files, Read current impl
- Edit existing code; Write new files only when genuinely needed
- Follow project conventions (CLAUDE.md), preserve existing behavior unless the
  change is intentionally behavioral
- Verify: syntax, run relevant tests, confirm the change matches reviewer intent
- Mark the todo `completed` immediately — do NOT batch completions

### 4. Handle feedback by type
- **Code changes**: Edit; keep style + type-hint conventions consistent
- **New features**: add tests + docs alongside the feature
- **Docs**: update docstrings / markdown concisely in project style
- **Tests**: write as functions (not classes), descriptive names, pytest conventions
- **Refactoring**: preserve functionality, run tests to catch regressions

### 5. Validate
- Run affected tests
- Lint (e.g. `uv run ruff check` for Python projects)
- Confirm no existing functionality broke

### 6. Communicate
- Keep the todo list updated in real time
- Ask for clarification on unclear feedback
- Report blockers; summarize all changes at completion

## Edge cases / gotchas
- **Breaking changes required** → notify the user and discuss impact before implementing
- **Tests fail after a change** → fix before marking the todo complete; don't leave red
- **Referenced code doesn't exist** → ask the user, verify understanding before proceeding
- **Conflicting feedback** → surface and resolve with the user, never guess
- Use conventional commits if creating commits afterward (only when the user asks)
