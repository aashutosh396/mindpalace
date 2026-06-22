---
name: Autoresearch Setup (/ar:setup)
description: Use when starting a new autoresearch optimization experiment — interactively collects domain, target file, eval command, metric, direction, evaluator, and scope.
tags: [autoresearch, setup, experiment-config, optimization, metric, evaluator, ar-setup]
source: alirezarezvani/claude-skills
derived_from: engineering/autoresearch-agent/skills/setup
---

# /ar:setup — Create New Experiment

Set up a new autoresearch experiment with all required config. Pairs with the autoresearch-agent loop.

## If arguments provided
Pass straight to setup: `--domain --name --target --eval "{cmd}" --metric --direction [--evaluator] [--scope]`.

## Interactive mode (collect one at a time)
1. **Domain** — engineering / marketing / content / prompts / custom
2. **Name** — e.g., api-speed, blog-titles
3. **Target file** — verify it exists
4. **Eval command** — e.g., `pytest bench.py`, `python evaluate.py`
5. **Metric** — what the eval outputs (e.g., p50_ms, ctr_score)
6. **Direction** — lower or higher better
7. **Evaluator** (optional) — built-in or own
8. **Scope** — project (`.autoresearch/`) or user (`~/.autoresearch/`)

## Built-in evaluators
benchmark_speed (p50_ms↓) · benchmark_size (size_bytes↓) · test_pass_rate (↑) · build_speed (build_seconds↓) · memory_usage (peak_mb↓) · llm_judge_content (ctr_score↑) · llm_judge_prompt (quality_score↑) · llm_judge_copy (engagement_score↑).

## After setup
Report: experiment path + branch name; whether the eval command worked + baseline metric. Suggest: `/ar:run {domain}/{name}` to iterate, or `/ar:loop {domain}/{name}` for autonomous mode.
