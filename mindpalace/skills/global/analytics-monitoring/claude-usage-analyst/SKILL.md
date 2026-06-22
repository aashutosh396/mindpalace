---
name: Claude Usage Analyst
description: Use when the user asks why Claude quota was exhausted, whether opus/sonnet/fable is unusually expensive, how many tokens were spent, or wants a plain-language read of local Claude Code / Desktop usage — analyzes ccusage data, separating observed numbers from interpretation.
tags: [ccusage, claude-code, token-usage, quota, cost, cache, model-comparison, billing, usage-analysis]
source: daymade/claude-code-skills
derived_from: claude-usage-analyst
---

# Claude Usage Analyst

Produce evidence-based usage explanations from local `ccusage` data. Separate observed numbers from interpretation; explain quota burn in human terms.

## Workflow

1. Verify `ccusage` is available: `ccusage --version`. If missing, `npm install -g ccusage@latest` or run via `npx ccusage@latest`.
2. Run the analyzer for the window: `--since YYYY-MM-DD --until YYYY-MM-DD --timezone <tz>`. Default = today in the chosen timezone. For historical comparison set `--since` to an earlier date (e.g. first of month); otherwise rank/median fields describe only the single day.
3. For model comparison, pass aliases (`--model-a fable --model-b opus-4-8`).

## Evidence rules

- Base every numeric claim on `ccusage` output, never memory.
- State scope: `ccusage claude` measures local Claude Code usage logs (including Claude Desktop's Claude Code sessions when local logs exist). It is NOT a full Claude.ai chat bill.
- Report dates with timezone.
- Explain cache plainly: cache-read tokens are still quota pressure even though the user never typed them.
- Do not infer Anthropic plan quota rules from local token counts unless the user gives plan details. Say "quota-like pressure" or "ccusage-estimated cost/burn" when exact accounting is unknown.
- When comparing models, compare both token volume AND estimated cost — a model can have similar volume but higher cost.

## Output shape

1. Short plain-language conclusion.
2. Evidence table: total tokens, cost, input, output, cache create, cache read.
3. Model comparison table.
4. 5-hour block table when quota exhaustion is discussed.
5. Why the burn happened.
6. Confidence and caveats.

Keep readable for non-technical users; translate terms like "cache read" in one sentence.
