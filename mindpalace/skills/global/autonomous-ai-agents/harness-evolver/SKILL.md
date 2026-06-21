---
name: harness-evolver
description: "Use when you want to autonomously optimize/evolve an LLM agent codebase — improve prompts, routing, tools, or architecture — running a propose-evaluate-iterate loop scored by LangSmith. Trigger on: evolve the agent, optimize LLM agent, improve agent performance/accuracy, harness:setup/evolve/status, agent evolution, LangSmith eval loop."
version: 1.0.0
license: MIT
tags: [llm-agent, agent-optimization, evolution, langsmith, eval, prompt-optimization, multi-agent, autonomous, claude-code]
source: https://github.com/raphaelchristi/harness-evolver
derived_from: awesomeclaude
prerequisites:
  commands: [python3, git, claude]
---

# Harness Evolver

Point at any LLM agent codebase and autonomously improve it (prompts, routing, tools,
architecture) using a multi-agent propose-evaluate-iterate loop. LangSmith is the
evaluation backend; git worktrees give each candidate isolation. Only improvements
that beat the current best on a held-out split get merged — regressions are rejected
by a constraint gate, so the best score only goes up.

## When to use
- User wants to optimize/evolve an LLM agent and lift a measurable score (accuracy,
  latency, token efficiency, error rate).
- User says "evolve the agent", "improve agent performance", "run the optimization loop",
  or invokes any `harness:*` command.
- The agent has (or can generate) an eval dataset and a runnable entry point.

Do NOT use for one-off prompt tweaks with no eval harness — the value is the scored loop.

## Install (Claude Code plugin)
```
/plugin marketplace add raphaelchristi/harness-evolver-marketplace
/plugin install harness-evolver
```
Or `npx harness-evolver@latest` for first-time setup / non-Claude-Code runtimes
(Cursor, Codex, Windsurf).

## Prerequisites
- `LANGSMITH_API_KEY` in env (`export LANGSMITH_API_KEY=lsv2_pt_...`), in `.env`, or in
  the langsmith-cli credentials file. NEVER pass the key inline on a Bash command — the
  tools load it automatically; inline exposes it in output.
- A runnable agent entry point (e.g. `python main.py {input}` where `{input}` is a JSON
  file path the runner fills in).

## Workflow (the six commands)
```
/harness:setup      # explore project, configure LangSmith, run baseline eval
/harness:health     # check dataset quality, auto-correct issues (also auto-run by evolve)
/harness:evolve     # the propose-evaluate-iterate optimization loop
/harness:status     # progress + ASCII score chart, detect stagnation
/harness:certify    # re-run eval N times, report mean ± std (score stability)
/harness:deploy     # tag, push, finalize (best code already auto-merged in evolve)
```

## How it works (mechanics)
- **Config** lives in `.evolver.json` (entry command, framework, python, dataset,
  goals/evaluators, mode, `best_experiment`, `best_score`, `project_dir`).
- **Tool path resolution** at the top of every command:
  ```bash
  TOOLS="${EVOLVER_TOOLS:-$([ -d ".evolver/tools" ] && echo ".evolver/tools" || echo "$HOME/.evolver/tools")}"
  EVOLVER_PY="${EVOLVER_PY:-$([ -f "$HOME/.evolver/venv/bin/python" ] && echo "$HOME/.evolver/venv/bin/python" || echo "python3")}"
  ```
  Use `$EVOLVER_PY` (not bare `python3`) for ALL tool calls so the venv with langsmith is used.
- **Setup**: scans for entry points (`main.py`, `agent.py`, `graph.py`, etc.) and the
  framework (LangGraph/CrewAI/Agno/OpenAI Agents SDK...). Detects monorepos and asks WHICH
  app. Detects venvs and prefers them. Maps goals to evaluators, generates ~30 test examples
  if none supplied, runs a baseline experiment.
- **Evolve loop per iteration**: read state → gather data (`trace_insights.py`,
  `read_results.py`) → generate `strategy.md` (capped ~1500 tokens, current iteration only)
  and `lenses.json` → spawn N proposer agents in worktrees → evaluate each candidate on
  LangSmith → constraint gate merges only candidates that beat best on held-out split →
  update `best_*` in config. Iteration traces logged to LangSmith (optional).
- **Modes** (cost/quality knob): `light` (~2 min/iter, 2 proposers, sampled),
  `balanced` (~8 min/iter, 3 proposers, 2 waves), `heavy` (~25 min/iter, 5 proposers,
  full analysis + pairwise). Set in config or via `--mode`.
- **Evolution memory** (`evolution_memory.md`) carries promoted insights across iterations
  so later proposers reuse what worked and avoid rejected approaches.

## Key arguments
- `harness:evolve --iterations N` (default ask or 5)
- `--mode light|balanced|heavy`
- `--no-interactive` — skip prompts, use defaults (for cron/background runs)
- interactive prompts: iterations (3/5/10), target score (0.8/0.9/0.95/none), exec mode.

## Gotchas
- `.evolver.json` must exist before `evolve`/`health`/`status`/`certify` — run
  `harness:setup` first.
- If the eval shows code-only baseline scores but LLM-judge evaluators are configured,
  evolve scores the baseline with the judge first and updates `best_score`.
- Preflight (`preflight.py`) validates key, schema, LangSmith state, dataset health, and
  canary in one pass before the loop; on failure offer fix-and-retry, continue, or abort.
- Not every iteration improves — that is expected. The best/line score never drops because
  regressions are not merged; raw candidate scores (bars) bounce around.
- Helper scripts live in the source `skills/<cmd>/` dirs and `tools/`; do not re-copy them —
  the plugin/npx install places them at `$EVOLVER_TOOLS` / `~/.evolver/tools`.

## Reference
Source skills: https://github.com/raphaelchristi/harness-evolver/tree/main/skills
(`setup`, `health`, `evolve`, `status`, `certify`, `deploy`). Paper: Meta-Harness (arXiv 2603.28052).
