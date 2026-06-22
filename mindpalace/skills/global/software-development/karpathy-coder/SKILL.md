---
name: Karpathy Coder — Coding Discipline
description: Use when writing, reviewing, or committing code to avoid LLM over-coding — surface assumptions before coding, keep it simple, make surgical changes, and define verifiable success criteria.
tags: [code-quality, simplicity, surgical-changes, assumptions, success-criteria, karpathy, anti-overengineering, review, discipline]
source: alirezarezvani/claude-skills
derived_from: engineering/karpathy-coder
---

# Karpathy Coder — Coding Discipline

Counters the documented LLM coding pitfalls: making wrong assumptions silently, overcomplicating code/APIs, not cleaning up, and looping without clear goals.

## The four principles

### 1. Think before coding
Don't assume. Don't hide confusion. Surface tradeoffs.
- State assumptions explicitly; if uncertain, ask.
- Multiple interpretations exist → present them, don't pick silently.
- A simpler approach exists → say so; push back when warranted.
- Something unclear → stop, name what's confusing, ask.

### 2. Simplicity first
Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility"/"configurability" that wasn't requested.
- No error handling for impossible scenarios.
- Wrote 200 lines that could be 50? Rewrite it.
- **Test:** would a senior engineer call this overcomplicated? If yes, simplify.

### 3. Surgical changes
Touch only what you must. Clean up only your own mess.
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style even if you'd do it differently.
- Notice unrelated dead code → mention it, don't delete it.
- Remove imports/vars/functions YOUR changes made unused; don't remove pre-existing dead code unless asked.
- **Test:** every changed line traces directly to the user's request.

### 4. Goal-driven execution
Define success criteria, then loop until verified.

| Instead of... | Transform to... |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

For multi-step tasks, state a brief plan with a verify check per step:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

## When to relax
Bias is caution over speed. For trivial tasks (typo fixes, obvious one-liners) use judgment. The principles matter most on: non-trivial implementations (>20 lines changed), code you don't fully understand, multi-step tasks with unclear requirements, anything reviewed by humans.
