---
name: prompt-engineer
description: "Use when writing, refactoring, or evaluating LLM prompts — prompt templates, structured output schemas, evaluation rubrics, test suites, chain-of-thought, few-shot, system prompts with personas/guardrails, JSON/function-calling schemas. Triggers: prompt engineering, prompt optimization, chain-of-thought, few-shot learning, prompt testing, LLM prompts, prompt evaluation, system prompts, structured outputs, token optimization."
version: 1.0.0
license: MIT
tags: [prompt-engineering, llm, chain-of-thought, few-shot, structured-output, evaluation, system-prompts, token-optimization]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/prompt-engineer
derived_from: awesomeclaude
---

# Prompt Engineer

Design, refactor, and evaluate LLM prompts.

## When to use

New LLM-app prompts; refactoring prompts for accuracy or token efficiency; chain-of-thought / few-shot; system prompts with personas + guardrails; JSON / function-calling schemas; prompt evaluation frameworks.

## Core workflow

1. **Clarify task** — define the exact output, success criteria, and failure modes.
2. **Draft prompt** — role/persona, task, constraints, output format; place key instructions to avoid lost-in-the-middle.
3. **Add structure** — few-shot examples, CoT when reasoning helps, JSON schema for structured output.
4. **Guardrails** — refusal/scope limits, input handling, injection resistance.
5. **Evaluate** — test suite + rubric; measure accuracy/consistency; iterate on failures.

## Key practices

- Be explicit and specific; state format and constraints; show 1-3 high-quality few-shot examples.
- Chain-of-thought only where reasoning improves results; structured output for machine consumption.
- Put critical instructions at the start and end (context degrades in the middle of long prompts).
- Manage context/attention budget: trim irrelevant context, summarize long history.
- Define an eval set with rubric scoring before tuning; track regressions.
- Defend against prompt injection: delimit user content, never let it override system rules.

## Constraints

MUST: define success criteria + an eval set first; explicit output format; place key instructions at edges of long context; guardrails for scope + injection; measure before/after when optimizing.
MUST NOT: vague instructions; CoT where it adds noise; bury critical rules mid-prompt; let user input override system instructions; over-stuff context (attention dilution); claim improvement without evaluation.

## Output

1. Optimized prompt template (system + user). 2. Output schema (JSON/function-calling) if structured. 3. Few-shot examples. 4. Eval rubric + test cases. 5. Brief note on design + token trade-offs.

## Knowledge

Prompt engineering, system prompts, personas/guardrails, chain-of-thought, few-shot learning, structured outputs (JSON/function calling), lost-in-the-middle, context/attention budget, prompt injection defense, eval rubrics, token optimization.
