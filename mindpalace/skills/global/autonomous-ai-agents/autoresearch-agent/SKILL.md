---
name: Autoresearch Agent
description: Use when the user wants to optimize a file by a measurable metric — code speed, bundle/image size, test pass rate, prompts, content/CTR — via an autonomous edit→evaluate→keep/discard git loop (Karpathy-inspired).
tags: [autoresearch, optimization-loop, karpathy, benchmark, experiment, git, metric, autonomous-agent, self-improvement]
source: alirezarezvani/claude-skills
derived_from: engineering/autoresearch-agent
---

# Autoresearch Agent

Autonomous experiment loop inspired by Karpathy's autoresearch. The agent edits ONE file, runs a fixed evaluation, keeps improvements (git commit), discards failures (git reset), loops indefinitely. Not one guess — many measured attempts, compounding. Requires: target file, eval command that outputs a metric, git repo.

## Setup (`/ar:setup`)
Create the experiment: `--domain` (engineering/marketing/content/prompts/custom), `--name`, `--target` (file to optimize), `--eval` (command that measures), `--metric` (name to find in output), `--direction` (lower|higher), `--scope` (project=`.autoresearch/` git-tracked defs, results gitignored; or user=`~/.autoresearch/`).
Creates: `program.md` (objectives/constraints/strategy), `config.cfg`, `results.tsv` (commit|metric|status|description), `evaluate.py` (if `--evaluator` used). If `program.md` exists, read it — it overrides the template.

## Built-in evaluators
Free: `benchmark_speed` (p50_ms↓), `benchmark_size` (size_bytes↓), `test_pass_rate` (↑), `build_speed` (build_seconds↓), `memory_usage` (peak_mb↓). LLM-judge (uses your CLI subscription): `llm_judge_content` (ctr_score↑), `llm_judge_prompt` (quality_score↑), `llm_judge_copy` (engagement_score↑). Custom: any script that prints `metric_name: value`.

## Agent protocol — you ARE the loop
**Before starting:** read config.cfg (target, evaluate_cmd, metric, metric_direction, time_budget), program.md (strategy/constraints), results.tsv (history); checkout branch `autoresearch/{domain}/{name}`.
**Each iteration:** review results.tsv (worked/failed/untried) → decide ONE change → edit target → `git commit` → `run_experiment.py --single` (prints KEEP/DISCARD/CRASH + metric) → repeat. Script handles eval timeout, metric parsing, comparison, revert on failure, logging.

## Strategy escalation
Runs 1-5 low-hanging fruit · 6-15 systematic (one param at a time) · 16-30 structural (algorithm/architecture) · 30+ radical. No improvement in 20+ runs → update program.md Strategy. Every 10 runs → review results.tsv for patterns, record learnings in program.md.

## Hard rules
- **One change per experiment** — you won't know what worked otherwise.
- **Simplicity criterion** — small gain with ugly complexity isn't worth it; equal perf simpler = win; removing code for same result = best.
- **Never modify the evaluator** — it's ground truth; modifying invalidates all comparisons (hard stop).
- **Timeout** at 2.5× budget → treat as crash. **5 consecutive crashes** → pause and alert.
- **No new dependencies.**

## Proactive triggers
Eval command doesn't work → test before looping · target not in git → init first · direction unclear → ask · time budget too short → every run crashes · agent editing evaluate.py → hard stop · 5 crashes → pause · no improvement 20+ runs → suggest strategy change.

## Viewing results
`log_results.py --experiment/--domain/--dashboard` (TSV/CSV/markdown). Dashboard: DOMAIN, EXPERIMENT, RUNS, KEPT, BEST, Δ FROM START, STATUS.
