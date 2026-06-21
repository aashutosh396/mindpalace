---
name: ralph-goal-loop
description: "Use when a task should be GROUND ON until it's actually done — not one shot. 'keep going until tests pass', 'loop until it works', 'goal: …', autonomous overnight/unattended work, self-correcting build-test-fix cycles. The ralph-wiggum iterate-until-complete pattern."
version: 1.0.0
license: MIT
tags: [goal, loop, ralph, ralph-wiggum, iterate, autonomous, until-done, self-correct, unattended, tdd-loop]
derived_from: awesomeclaude
source: https://awesomeclaude.ai/ralph-wiggum
---

# Ralph-Wiggum Goal Loop

**The idea (Geoffrey Huntley's "Ralph"):** instead of assuming perfect output on the first try,
re-feed the same goal until a completion signal appears. Iteration over perfection; failures are
data; progress lives in the ARTIFACTS (files, tests, repo state), not in the chat.

## When to use
- The goal has **checkable** success: tests pass, a file/endpoint exists, build is clean, a script
  runs green. ("keep going until all tests pass", "loop until the page loads 200")
- Unattended / overnight grinding on a well-defined build or fix.
- Self-correcting cycles: write test → implement → run → fix → repeat.

## When NOT to use
- Subjective/judgment tasks, production debugging with irreversible side effects, or anything
  needing human approval mid-way. Those want a single careful turn, not a loop.

## How to run it
mindpalace has this built in — you don't hand-roll a bash loop:

- **Terminal:** `mindpalace goal "<task>" [--max N] [--until PROMISE]`
- **Discord/chat:** start with `goal:` or phrase it as a loop —
  `goal: get the auth test suite green`, or "keep working until all tests in test/auth pass".
  It runs in the **background** (parallel to live chat) and reports each iteration + a final card.

## How it works (so you can write good goals)
Each iteration is a full autonomous turn that:
1. **Inspects the current state** first (what's already done — progress persisted in files), then
2. does the **next concrete steps**, then
3. **verifies** (runs the tests/checks/command).
When the goal is fully met AND verified, it emits the completion line `<<GOAL_COMPLETE>>` and the
loop stops. Otherwise it reports progress and iterates. A `--max` cap (default 10) is the safety net.

## Writing a strong goal (this is the lever — operator skill > model)
- **Clear completion criteria**: state exactly what "done" means (which tests, which command exits 0).
- **Incremental phases**: break a big goal into sequential, verifiable chunks.
- **Embed the self-correction**: "write failing tests → implement → run → fix → refactor".

Example:
```
goal: implement the /batch-uploads endpoint with TDD —
1) write failing tests for create/list/delete
2) implement until they pass
3) run the full suite; fix any regressions
done = `pytest test/batch_uploads` exits 0 and lint is clean
```
