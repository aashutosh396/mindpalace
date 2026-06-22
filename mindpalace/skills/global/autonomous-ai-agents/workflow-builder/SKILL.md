---
name: Workflow Builder
description: Use when authoring or scaffolding a Claude Code Workflow — deterministic multi-agent .js scripts in .claude/workflows/ that fan work out to fresh-context sub-agents (fan-out, pipeline, loop, judge-panel) for repeatable, resumable automation.
tags: [workflow, multi-agent, orchestration, fan-out, pipeline, sub-agents, claude-code, automation, deterministic, resumable]
source: alirezarezvani/claude-skills
derived_from: engineering/workflow-builder
---

# Workflow Builder

Author runnable workflow scripts for Claude Code's Workflow tool: deterministic multi-agent `.js` files that fan work out to fresh-context sub-agents under plain JavaScript control flow. Only leaf `agent()` calls spend tokens, so the main session stays clean and the run is resumable.

## ALWAYS start with intake (non-negotiable — never skip to code)

Ask this opening set:
- What repeatable, multi-step task do you want to automate?
- What is the one unit of work a single sub-agent does once?
- How many units — a known list, or discovered by looping?
- Do later steps need *all* prior results at once, or can each item flow on its own?
- Does any step need structured data back (a verdict, a list, scores)?
- Roughly how many tokens / how deep?

If the user is vague, do NOT stall — turn whatever you have into 1-2 concrete proposals via the intake recommender, then present them as "Here's what I'd build and why" (recommended topology + model picks + budget guard + one-line rationale per choice). Never make the user re-answer questions they half-answered.

**Confirm the shape** (topology + phases + parallel-vs-pipeline) before writing the file. That is the only approval gate.

## Is a workflow even the right tool?

| Scenario | Use |
|---|---|
| Single sub-agent, one task | plain Agent tool |
| Reusable procedure, Claude picks steps dynamically | a Skill |
| Many sub-agents, fixed topology, deterministic + resumable | **Workflow** |

Workflows earn their cost when work is parallel/multi-stage, must be reproducible, long enough to fail halfway (resume matters), or benefits from per-step context isolation. One-offs → use Claude directly.

## Build → validate → run loop

1. **Scaffold** a starter from the confirmed topology (fan-out / pipeline / loop / judge-panel).
2. **Edit:** `meta` block first (pure literal, first statement), then async body using injected globals — `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`, `budget`, `args`, `workflow()`.
3. **Validate** before running (catches parser-fatal mistakes).
4. **Run:** `export CLAUDE_CODE_WORKFLOWS=1`, save under `.claude/workflows/`, launch via `/workflows`. **P** pause/resume, **X** skip a sub-agent; failed agents retry automatically.

## Hard rules (validator enforces)
- `meta` is a **pure literal** and the **first statement** — no variables, spreads, template strings, or function calls inside it.
- **No non-determinism:** no `Date.now()`, `Math.random()`, argless `new Date()` (they break resume) — pass timestamps via `args`.
- **No filesystem / Node APIs** (`require`, `fs`, `process`, network) in the orchestrator — that work belongs *inside* `agent()` prompts.
- `parallel()` takes **thunks** (`() => agent(...)`), not bare promises. Default to `pipeline()` unless a stage needs the whole prior result set.
- **Guard every open-ended loop** with a counter or `budget.remaining()` check — unguarded loops hit the 1000-agent cap.
- Filter skipped/failed agents: `results.filter(Boolean)`.
