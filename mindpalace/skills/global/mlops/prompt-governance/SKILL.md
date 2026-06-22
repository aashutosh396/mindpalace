---
name: Prompt Governance
description: Use when managing prompts in production at scale — versioning prompts, building a prompt registry, running eval pipelines to prevent regressions, A/B testing prompts, and governed promote/rollback workflows. Treats prompts as first-class infrastructure.
tags: [prompt-governance, prompt-versioning, prompt-registry, eval-pipeline, golden-dataset, prompt-ab-test, regression, llm-as-judge, mlops]
source: alirezarezvani/claude-skills
derived_from: engineering/prompt-governance
---

# Prompt Governance

Treat prompts as first-class infrastructure — versioned, tested, evaluated, deployed with the rigor of application code. Prompts are code: they change behavior in production; ship them like code. **NOT** for writing/improving individual prompts, RAG design, or cost reduction.

## Before Starting (ask in one shot)

Current state (how stored: hardcoded/config/db/tool? how many prod prompts? ever had an uncaught regression?) · goals (primary pain: versioning chaos / no evals / blind A-B / slow iteration? team size + ownership model? tooling constraints?) · AI stack (providers, frameworks, existing test/CI).

## Mode 1 — Build Prompt Registry

Provides: single source of truth, version history + rollback, environment promotion (dev→staging→prod), audit trail (who/what/when/why), variable/template management.

**Minimum viable (file-based)** — structured files in version control:
```
prompts/
  registry.yaml          # index: id, description, owner, model, versions[]
  summarizer/v1.1.0.md   # versioned prompt content
```
`registry.yaml` per version tracks: version, file, status (production/archived), promoted_at, promoted_by.

**Production (db-backed)** — API-accessible registry; `prompts` + `prompt_versions` tables tracking slug, content, model, environment, eval_score, promotion metadata.

## Mode 2 — Build Eval Pipeline

Automated evals run on every prompt change, like unit tests.

**Eval types:** exact match (classification/extraction); contains check (key-point/summary); LLM-as-judge (open-ended/tone, scores 1-5); semantic similarity (paraphrase-tolerant); schema validation (structured output); human eval (high-stakes launch gates).

**Golden dataset:** fixed input/expected-output pairs defining correct behavior. Requirements: ≥20 examples (100+ for production confidence); cover edge cases + failure modes, not just happy path; reviewed by a domain expert (not just the prompt author); versioned alongside the prompt.

**Pass thresholds (calibrate):** classification/extraction ≥95% exact match; summarization ≥0.85 LLM-judge; structured output 100% schema valid; open-ended ≥80% human approval. Runner iterates the golden set, calls the LLM with the version under test, scores each, reports pass_rate + avg_score + failure details.

## Mode 3 — Governed Iteration

Lifecycle with a gate at each stage: BRANCH → DEVELOP (dev env, manual test) → EVAL (vs golden set, in CI) → COMPARE (new vs current prod score) → REVIEW (PR with eval results + diff) → PROMOTE (staging→prod, approval gate) → MONITOR (24-48h prod metrics) → ROLLBACK (one command).

**A/B testing prompts:** stable assignment (user_id hash → same variant); log every assignment (user_id, slug, variant); define success metric *before* starting; run ≥1 week or 1,000 req/variant; check novelty effect; require p<0.05; monitor latency + cost alongside quality.

**Rollback:** one command promotes the previous version back to production, then re-run evals against the restored version to verify.

## Proactive Triggers (surface unprompted)

Prompts hardcoded in app code (changes need code deploys, mixes concerns) · no golden dataset for prod prompts (flying blind) · eval pass rate declining (model updates silently break prompts — scheduled evals catch it) · no rollback capability · one person owns all prompt knowledge (bus factor) · prompt changes deployed without eval (every uneval'd deploy is a bet).

## Communication

Bottom line first · What + Why + How · actions have owners + deadlines · confidence tag (verified/medium/assumed).
