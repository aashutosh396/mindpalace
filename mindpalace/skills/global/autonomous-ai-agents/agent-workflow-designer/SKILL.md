---
name: Agent Workflow Designer
description: Use when architecting a multi-step agent pipeline, choosing single-agent vs multi-agent, or refactoring an LLM workflow with context bloat or unreliable handoffs — picks the pattern and scaffolds the config.
tags: [agent-workflow, orchestration, sequential, parallel, router, evaluator, handoff, context-budget, retry, llm-pipeline]
source: alirezarezvani/claude-skills
derived_from: agent-workflow-designer
---

# Agent Workflow Designer

Design production multi-agent workflows with explicit pattern choice, handoff contracts, failure handling, and cost/context controls.

## When to use
A single prompt is insufficient for the task complexity · you need specialist agents with explicit boundaries · you want deterministic structure before implementation · you need validation loops for quality/safety gates.

## Pattern map
- `sequential` — strict step-by-step dependency chain
- `parallel` — fan-out/fan-in for independent subtasks
- `router` — dispatch by intent/type with fallback
- `orchestrator` — planner coordinates specialists with dependencies
- `evaluator` — generator + quality-gate loop

## Recommended workflow
1. Select pattern based on dependency shape and risk profile.
2. Scaffold config from the chosen pattern.
3. Define handoff-contract fields for every edge (explicit, bounded payloads — pass targeted artifacts, not full upstream context).
4. Add retry/timeouts and output-validation gates per step.
5. Dry-run with small context budgets before scaling.

## Common pitfalls
Over-orchestrating tasks a single well-structured prompt could solve · missing timeout/retry on external-model calls · passing full upstream context instead of targeted artifacts · ignoring per-step cost accumulation.

## Best practices
1. Start with the smallest pattern that satisfies requirements. 2. Keep handoff payloads explicit and bounded. 3. Validate intermediate outputs before fan-in synthesis. 4. Enforce budget + timeout limits in every step.
