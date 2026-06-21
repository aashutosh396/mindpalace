---
name: subagent-driven-development
description: "Use when executing a written implementation plan with mostly-independent tasks in the current session — dispatch a fresh implementer subagent per task, run a spec+quality review after each, and a broad whole-branch review at the end. Triggers: 'execute this plan', task-by-task implementation, fresh-context-per-task, controller/implementer/reviewer loop, durable progress ledger."
version: 1.0.0
license: MIT
tags: [subagents, plan-execution, orchestration, tdd, code-review, workflow, agents, delegation, progress-ledger]
source: https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development
derived_from: awesomeclaude
---

# Subagent-Driven Development

Execute plan by dispatching a fresh implementer subagent per task, a task review (spec compliance + code quality) after each, and a broad whole-branch review at the end.

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

**Core principle:** Fresh subagent per task + task review (spec + quality) + broad final review = high quality, fast iteration

**Narration:** between tool calls, narrate at most one short line — the ledger and the tool results carry the record.

**Continuous execution:** Do not pause to check in between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete.

## When to Use

Use when you have an implementation plan, tasks are mostly independent, and you want to stay in the current session (fresh subagent per task, review after each, no human-in-loop between tasks). If tasks are tightly coupled, do manual execution or brainstorm first. For a parallel session instead of same-session execution, use executing-plans.

## The Process

Per task:
1. Dispatch implementer subagent with the task brief + report path + context.
2. If the implementer asks questions, answer them, then re-dispatch.
3. Implementer implements, tests, commits, self-reviews.
4. Generate a review package (diff file) and dispatch a task reviewer (spec compliance + code quality).
5. If the reviewer reports issues, dispatch a fix subagent for Critical/Important findings, then re-review.
6. When the review is clean, mark the task complete in the todo list and the progress ledger.

After all tasks: dispatch a final whole-branch code reviewer, then finish the development branch.

## Pre-Flight Plan Review

Before dispatching Task 1, scan the plan once for conflicts: tasks that contradict each other or the Global Constraints, and anything the plan mandates that a review rubric treats as a defect (a test that asserts nothing, verbatim duplication of a logic block). Present all findings as one batched question — each finding beside the plan text that mandates it — before execution begins, not one interrupt per discovery.

## Model Selection

Use the least powerful model that can handle each role to conserve cost and increase speed.

- **Mechanical implementation** (isolated functions, clear specs, 1-2 files): fast, cheap model.
- **Integration and judgment** (multi-file coordination, debugging): standard model.
- **Architecture and design**, and the final whole-branch review: most capable available model.
- **Review tasks**: scale to the diff's size, complexity, and risk.

**Always specify the model explicitly when dispatching** — an omitted model inherits your session's (often most expensive) model. Turn count beats token price: cheapest models often take 2-3× the turns on multi-step work. Use a mid-tier floor for reviewers and prose-driven implementers; use the cheapest tier only when the plan text contains the complete code to transcribe.

## Handling Implementer Status

- **DONE:** Generate the review package (BASE = the commit recorded before dispatch, never `HEAD~1`), then dispatch the task reviewer.
- **DONE_WITH_CONCERNS:** Read the concerns. If about correctness/scope, address before review; if observations, note and proceed.
- **NEEDS_CONTEXT:** Provide the missing info and re-dispatch.
- **BLOCKED:** Assess — context problem (add context, re-dispatch same model), needs more reasoning (re-dispatch capable model), too large (break up), plan wrong (escalate to human). Never force the same model to retry without changes.

## Handling Reviewer ⚠️ Items

The reviewer may report "⚠️ Cannot verify from diff" items — requirements in unchanged code or spanning tasks. These don't block the rest of the review, but resolve each yourself before marking complete: you hold the cross-task context the reviewer lacks. A confirmed gap is a failed spec review — send it back.

## Constructing Reviewer Prompts

Per-task reviews are task-scoped gates; the broad review happens once at the end.

- Don't add open-ended directives ("check all uses") without a concrete reason.
- Don't ask a reviewer to re-run tests the implementer already ran on the same code.
- **Never pre-judge findings** — don't instruct a reviewer to ignore an issue or pre-rate severity ("treat as Minor at most"). If the prompt contains "do not flag," "don't treat X as a defect," or "the plan chose," stop — you're pre-judging.
- The global-constraints block is the reviewer's attention lens: copy binding requirements verbatim (exact values, formats, stated relationships).
- Hand the reviewer its diff as a file, not pasted text.
- A dispatch prompt describes one task, not session history — don't paste accumulated prior-task summaries.
- Dispatch fix subagents for Critical and Important findings; record Minor findings in the ledger for the final review to triage.
- A plan-mandated finding (or one conflicting with plan text) is the human's decision: present finding + plan text, ask which governs.
- The final whole-branch review gets a package too (MERGE_BASE..HEAD).
- Every fix dispatch carries the implementer contract: re-run the covering tests and report results.
- If the final review returns findings, dispatch ONE fix subagent with the complete list — not one fixer per finding.

## File Handoffs

Everything pasted into a dispatch — and everything a subagent prints back — stays resident in your context and is re-read every turn. Hand artifacts over as files:

- **Task brief:** extract the task's full text to a file; the dispatch contains where the task fits, the brief path ("read this first — your requirements"), interfaces/decisions from earlier tasks the brief can't know, your resolution of any ambiguity, and the report-file path + contract. Exact values appear only in the brief.
- **Report file:** named after the brief; the implementer writes the full report there and returns only status, commits, one-line test summary, and concerns.
- **Reviewer inputs:** brief file + report file + review package + binding global constraints.
- Fix dispatches append their fix report (with test results) to the same report file.

## Durable Progress

Conversation memory does not survive compaction. Track progress in a ledger file, not only in todos.

- At skill start, check for a ledger (`.superpowers/sdd/progress.md` under the repo root). Tasks marked complete there are DONE — do not re-dispatch; resume at the first incomplete task.
- When a review comes back clean, append one line: `Task N: complete (commits <base7>..<head7>, review clean)`.
- The ledger is your recovery map: after compaction, trust the ledger and `git log` over recollection.

## Red Flags

**Never:**
- Start implementation on main/master without explicit consent
- Skip task review or accept a report missing either verdict (spec + quality both required)
- Proceed with unfixed Critical/Important issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make a subagent read the whole plan file (hand it its task brief)
- Tell a reviewer what not to flag, or pre-rate a finding's severity
- Re-dispatch a task the ledger already marks complete

**If subagent asks questions:** answer clearly and completely before they proceed.
**If reviewer finds issues:** same subagent fixes them, reviewer reviews again, repeat until approved.
**If subagent fails:** dispatch a fix subagent — don't fix manually (context pollution).

## Integration

Pairs with: using-git-worktrees (isolated workspace), writing-plans (creates the plan this executes), requesting-code-review (final whole-branch review template), finishing-a-development-branch (complete after all tasks). Subagents follow test-driven-development per task. Alternative: executing-plans for a parallel session.

> Note: the upstream skill ships companion prompt templates (`implementer-prompt.md`, `task-reviewer-prompt.md`) and helper scripts (`review-package`, `task-brief`). This is the standalone methodology; recreate those helpers as needed for your harness.
