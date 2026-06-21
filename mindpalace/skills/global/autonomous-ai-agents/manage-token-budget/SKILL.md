---
name: manage-token-budget
description: "Use when running long-lived agent loops (heartbeats, polling, autonomous workflows) where cost compounds, when context windows grow unpredictably between cycles, when API costs spike beyond baseline, when designing a new agentic workflow that needs cost guardrails, or after a cost incident. Triggers: token budget, context window cost, runaway agent cost, heartbeat interval, prune context, progressive disclosure, cost cap, API spend."
version: 1.0.0
license: MIT
tags: [token-budget, cost-control, context-window, agent-loops, pruning, progressive-disclosure, finops, autonomous]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/manage-token-budget
derived_from: awesomeclaude
---

# Manage Token Budget

Control cost and context footprint of agentic systems: every token in the window should earn its place. (A real 37-hour autonomous session cost $13.74 from a 30-min heartbeat + verbose prompts + unchecked context growth — fixed by 4-hour intervals and notification-only mode.)

## When to Use

- Long-lived loops (heartbeats, polling) where cost compounds
- Context windows growing unpredictably between cycles
- API costs spiked beyond baseline; post-mortem needed
- Designing a new workflow needing cost guardrails
- System prompts, memory, or tool schemas dominating the window

## Procedure

### Step 1 — Per-cycle cost tracking
Log input tokens, output tokens, cost, timestamp, and trigger for every cycle — stored externally (file/db), never in the context window. If no usage metadata, derive averages from the billing dashboard.

### Step 2 — Audit the context window
Decompose and rank consumers: system prompt, memory, tool schemas, active skill procedures, conversation history, current-cycle dynamic content. Flag components large relative to their decision value (e.g., a 4k-token memory file the task never references). Use chars/4 (text) or chars/3 (JSON) as a rough token estimate.

### Step 3 — Set budget caps with enforcement
Three levels: soft limit (60-75% → warn, begin pruning, slow cadence), hard limit (→ halt, alert a human, preserve resume state), per-cycle cap (→ truncate outputs/skip low-priority). Each cap needs an explicit enforcement action, wired into the loop, not just documented.

### Step 4 — Emergency pruning
Drop lowest-value first: old tool outputs, redundant/superseded turns, verbose formatting, completed sub-task context, inactive skill procedures, irrelevant memory. Prune evidence AFTER the decision it informed, and leave a ~20-token tombstone preserving the conclusion.

### Step 5 — Progressive disclosure for loading
Route through lightweight metadata before loading full content: read a skill's registry entry (~50 tokens) before its full SKILL.md; read MEMORY.md index before topic files; read tool names before full schemas; read file listings/signatures before full files. Unload after use.

### Step 6 — Cost-aware cycle intervals
Compute cost/hour and hours-until-hard-limit; match the interval to the data's actual refresh rate, not anxiety (polling every 30 min when data updates every 4 h wastes 87.5% of cycles). Prefer webhooks/push over polling. If low latency is required, cut per-cycle cost instead.

### Step 7 — Validate controls
Test that tracking logs, soft-limit warning + pruning, hard-limit halt + alert, per-cycle truncation, and progressive disclosure all fire. Project daily/monthly cost and days-until-limit.

## Validation

- [ ] Per-cycle tracking logs tokens, cost, timestamp externally
- [ ] Context audit ranks consumers with %
- [ ] Soft/hard/per-cycle caps with explicit enforcement actions
- [ ] Pruning follows priority order with tombstones
- [ ] Progressive disclosure routes via metadata first
- [ ] Cycle interval justified by cost data + refresh rate
- [ ] Controls verified firing; projection within budget

## Common Pitfalls

- Tracking inside the context window (inflates what you're controlling).
- Soft limits without enforcement.
- Pruning evidence before the decision it informs.
- Matching cycle interval to anxiety, not data refresh.
- Loading full skills just to decide relevance.
- Ignoring the system prompt — it's paid every cycle.
- Budget caps without human escalation.

## Related

- manage-memory, coordinate-reasoning — companion agent-hygiene skills
- optimize-cloud-costs — infra-side cost control
