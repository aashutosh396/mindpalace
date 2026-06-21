---
name: coordinate-reasoning
description: "Use during long or complex agent tasks where sub-tasks must coordinate, the context has grown long, information freshness is uncertain, or after context compression — track which facts are fresh vs stale, apply lightweight local protocols, audit staleness, and test that sub-task outputs combine coherently. Triggers: long context, stale information, context compression, multi-step task, sub-task coordination, information decay, re-read before relying."
version: 1.0.0
license: MIT
tags: [coordination, context-management, information-decay, agent-reasoning, freshness, multi-step, stigmergy]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/coordinate-reasoning
derived_from: awesomeclaude
---

# Coordinate Reasoning

Manage internal coordination of a long task by treating context as signals with freshness and decay — so coherent behavior emerges from simple local rules.

## When to Use

- Complex tasks where multiple sub-tasks must coordinate (multi-file edits, refactors)
- Context has grown long and freshness is uncertain
- After context compression when information may be lost
- Sub-task outputs need to feed into each other cleanly
- Earlier reasoning must be carried forward without degradation

## Procedure

### Step 1 — Classify the coordination problem
- Foraging (scattered search → share findings, avoid duplicate work) — most debugging
- Consensus (competing paths → independent evaluation) — most design decisions
- Construction (incremental build → consistency, ordering) — most implementation
- Defense (quality under pressure → monitor, correct fast)
- Division of labor (sub-tasks with dependencies → ordering, handoff, integration)
Pick the dominant type for the current phase; it can change as the task progresses.

### Step 2 — Treat context as signals with decay
Decay rates: user's explicit instruction = slow (re-read after >30 msgs or compression); file contents = moderate (re-read if possibly modified or >15 msgs); own earlier reasoning = fast (re-derive); inferred facts = very fast (verify); MEMORY.md/CLAUDE.md = very slow (stable). Also keep inhibition signals — note failed tool calls, abandoned approaches, and user corrections so you don't repeat them.

### Step 3 — Apply local protocols
- Safety: before using a fact, check when it was last verified; re-verify if below threshold
- Response: when the user corrects something, update all downstream reasoning that depended on it
- Deposit: after a sub-task, summarize its output in 1-2 sentences for the next sub-task
- Exploration: if stuck >3 actions, try a different tool/file/framing
- Inhibition: before an approach, check if it was already tried and what is different now
Keep it light — default to Safety + Deposit; add others only when problems emerge.

### Step 4 — Calibrate freshness (active audit)
List facts established >N messages ago; for each note source, age, and status (Fresh/Stale/Unknown/Lost). Check for compression losses and drift between early plans and current execution. Re-verify the 2-3 facts the most downstream work depends on.

### Step 5 — Test emergent coherence
Check: do sub-task outputs feed cleanly into each other? Are tool calls non-redundant? Is direction still aligned with the request? If one key assumption is wrong, how much cascades (high cascade = fragile)? Fix the point of divergence, then re-verify downstream outputs.

## Validation

- [ ] Coordination problem classified by type
- [ ] Decay rates considered for relied-upon facts
- [ ] Safety + Deposit protocols applied
- [ ] Freshness audit run (stale items found or freshness confirmed with evidence)
- [ ] Coherence tested across sub-tasks
- [ ] Inhibition signals respected (no blind retries)

## Common Pitfalls

- Over-engineering signals — start with Safety + Deposit.
- Trusting stale context — when in doubt, re-read.
- Ignoring inhibition signals (blind retries are not persistence).
- No deposits, forcing later re-derivation.
- Assuming coherence without testing the integration.

## Related

- manage-memory, manage-token-budget — companion agent-hygiene skills
- build-consensus — for the Consensus coordination type
