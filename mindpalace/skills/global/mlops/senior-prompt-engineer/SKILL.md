---
name: Senior Prompt Engineer
description: Use when optimizing prompts, designing prompt templates, evaluating LLM outputs with an eval set, measuring RAG quality, validating agent/tool configs, or budgeting tokens/cost — eval-driven, model-agnostic.
tags: [prompt-engineering, llm-eval, rag, agent-validation, token-budget, structured-output, few-shot, eval-set, retrieval-quality, model-agnostic]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-prompt-engineer
---

# Senior Prompt Engineer

Eval-driven prompt engineering, RAG measurement, agent config validation. Model-agnostic: never hardcode model IDs or pricing — supply current rates for dollar figures.

## Operating Rules
1. **Never change a prompt without a baseline** — capture metrics first, compare every iteration.
2. **Eval set before optimization** — 10-20 representative cases with expected outputs minimum. No eval set = optimizing against vibes (the #1 failure).
3. **Prefer platform features over prompt hacks** — native structured outputs / JSON schema, tool-use APIs, prompt caching over "respond ONLY with JSON."
4. **Current models need less scaffolding** — don't add CoT boilerplate, role framing, or few-shot reflexively; add each only when the eval set shows it helps.
5. **Cost numbers are always user-supplied** — never trust a remembered price table.

## Prompt Optimization (eval-gated)
1. Baseline: token estimate, clarity/structure scores, ambiguity + redundancy detection.
2. Diagnose: ambiguous verbs ("analyze","handle"), redundant blocks, missing output contract, token waste.
3. Apply one change at a time, by leverage:
   - Malformed output → native structured outputs / schema-in-prompt.
   - Inconsistent across runs → tighten + 2-3 contrastive examples (one near-miss).
   - Misses edge cases → enumerate them + "when uncertain, do X."
   - Token bloat → stable prefix first (caching), trim redundancy.
   - Wrong reasoning on hard cases → stepwise reasoning in a scratch field, or extended-thinking mode.
4. Re-analyze + compare.
5. **Eval gate (before shipping)**: revised must not lose any previously-passing case (no-regression); clarity ≥ baseline AND tokens ≤ baseline×1.10.

## Few-Shot Design
Define task contract first (input/output shape, edge-case policy). Start with **zero examples**, measure, add only for failure clusters. Max 3-5, ordered simple→edge→negative (what NOT to extract), formatted identically to real output. Add held-out variants so cases don't pass only by resembling examples.

## Structured Output
Write JSON Schema first. Prefer API-native enforcement (prompt text can't guarantee shape). Fallback: schema as field-by-field rules + one valid example + "output only the JSON object." Gate: 10/10 eval outputs must parse.

## RAG Tuning Loop
Measure context relevance, precision@k, coverage, faithfulness, groundedness. Fix lowest metric first: relevance → chunking/embeddings/metadata filters; faithfulness → "answer only from context" + citations; coverage → retrieval k / query expansion. **Relevance < 0.80 is a retrieval problem, not a prompt problem** — fix retrieval before rewriting the generation prompt. Gate: every metric ≥ baseline.

## Agent Config Review
Validate: tool wiring, missing required config, loop risk (unbounded iterations), token estimates. Check context discipline: tool descriptions ≤ 1-2 sentences, minimal tool count, stable system prompt first (cache-friendly), iteration cap + early-exit. Budget per N runs; if over budget, cut tools/context before downgrading the model.
