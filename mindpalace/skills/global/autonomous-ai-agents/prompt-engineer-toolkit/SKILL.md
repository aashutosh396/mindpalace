---
name: Prompt Engineer Toolkit
description: Use when prompts need to become tested, versioned production assets — A/B prompt evaluation against structured test cases, immutable version history with diffs, regression-safe rollout, and LLM governance for marketing teams.
tags: [prompt engineering, prompt testing, prompt versioning, ab testing, llm governance, regression, evaluation, ai content]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/prompt-engineer-toolkit
---

# Prompt Engineer Toolkit

Move prompts from ad-hoc drafts to production assets with repeatable testing, versioning, and regression safety. Measurable quality over intuition.

## Core capabilities
A/B prompt evaluation against structured test cases · quantitative scoring (adherence, relevance, safety) · immutable version history + changelog · semantic diffs · reusable templates · regression-friendly model/prompt-update workflows.

## Key workflows
1. **Run A/B test** — prepare JSON test cases (each with `input`, `expected_contains`, `forbidden_contains`, `expected_regex`); run prompt A vs B across the suite via an external LLM runner command; emit per-case + aggregate metrics.
2. **Choose winner with evidence** — scoring covers expected-content coverage, forbidden-content violations, regex/format compliance, length sanity. Take the higher scorer as candidate baseline, then run the regression suite.
3. **Version prompts** — `add` (with name, author, change note), `diff` (between versions), `changelog`. Store metadata + content snapshots; never overwrite history.
4. **Regression loop** — store baseline → propose edits → re-run A/B → promote only if score improves AND violation count stays zero.

## Evaluation design
Each test case is deterministic-gradeable: realistic production-like `input`, required `expected_contains`, disallowed `forbidden_contains` (safety/unsafe phrases), structural `expected_regex`. Build a realistic, edge-case-rich suite — never judge from a single case.

## Pitfalls to avoid
1. Picking from single-case outputs.
2. Changing prompt and model simultaneously — isolate variables.
3. Missing forbidden-content checks.
4. Editing without version metadata/author/rationale.
5. Skipping semantic diff before deploy.
6. Optimizing one benchmark while harming edge cases.
7. Model swap without rerunning the baseline suite.

## Pre-promotion checklist
- [ ] Task intent explicit and unambiguous.
- [ ] Output schema/format explicit.
- [ ] Safety + exclusion constraints explicit.
- [ ] No contradictory instructions.
- [ ] No unnecessary verbosity tokens.
- [ ] A/B score improves and violation count is zero.

## Versioning policy
Semantic identifiers per feature (`ad_copy_shortform`) · record author + change note every revision · never overwrite historical versions · diff before promoting.

## Rollout
Baseline version → candidate → A/B on same cases → promote only if winner improves average and keeps violations at zero → track post-release feedback → feed new failure cases back into the suite.

## LLM governance for marketing teams
Claim discipline (no unverifiable claims) · disclosure rules (AI-generated content) · data boundaries · mandatory human-review gates before publish.
