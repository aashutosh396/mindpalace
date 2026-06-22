---
name: Promptfoo LLM Evaluation
description: Use when setting up LLM/prompt evaluation — building promptfooconfig.yaml, Python custom assertions, llm-rubric (LLM-as-judge), few-shot prompts, model comparison, or debugging relay/proxy 401s and ignored maxConcurrency.
tags: [promptfoo, llm-eval, prompt-testing, llm-as-judge, model-comparison, assertions, few-shot, yaml]
source: daymade/claude-code-skills
derived_from: promptfoo-evaluation
---

# Promptfoo Evaluation

Test and compare LLM outputs with Promptfoo CLI.

## Quick start
```bash
npx promptfoo@latest init
npx promptfoo@latest eval
npx promptfoo@latest view
```

## Config (promptfooconfig.yaml)
```yaml
description: "My Eval"
prompts: [file://prompts/system.md, file://prompts/chat.json]
providers:
  - { id: anthropic:messages:claude-sonnet-4-6, label: Claude }
  - { id: openai:gpt-4.1, label: GPT-4.1 }
tests: file://tests/cases.yaml
commandLineOptions: { maxConcurrency: 2 }   # MUST be here, NOT top-level
defaultTest:
  assert:
    - { type: python, value: "file://scripts/metrics.py:custom_assert" }
    - { type: llm-rubric, value: "Score quality 0-1.", threshold: 0.7 }
outputPath: results/eval-results.json
```

## Python assertions
Default fn `get_assert(output, context)` → return bool, float, or dict `{pass, score, reason, named_scores}`. Specify with `file://path.py:fn`. Access vars via `context['vars']`.

## LLM-as-judge (llm-rubric)
Provide clear scoring criteria + `threshold`. **Relay/proxy gotcha**: each `llm-rubric` needs its OWN `provider` with `apiBaseUrl` — the main provider's is NOT inherited (else grader 401s on default endpoint).

## Assertion types
`contains`, `icontains`, `equals`, `regex`, `python`, `llm-rubric`, `latency`.

## file:// resolution
ALL `file://` paths resolve relative to `promptfooconfig.yaml` location — NOT the file containing the reference (common gotcha when `tests:` points to a separate YAML).

## Relay/proxy
`apiBaseUrl` in `providers[].config` (Promptfoo appends `/v1/messages`). `maxConcurrency` under `commandLineOptions` (top-level silently ignored). With LLM-judge set `maxConcurrency: 1` (gen+grading share pool). Pass token as `ANTHROPIC_API_KEY`.

## Echo provider (free preview)
`providers: [echo]` returns the rendered prompt with no API calls — verify few-shot loading, var substitution, structure.

## Troubleshooting
Python not found → `export PROMPTFOO_PYTHON=python3`. Outputs >30k chars truncated → `head_limit`. HTML inflating metrics → strip `re.sub(r'<[^>]+>','',text)` in Python assertion. maxConcurrency ignored → wrong nesting. Judge 401 → per-rubric provider.
