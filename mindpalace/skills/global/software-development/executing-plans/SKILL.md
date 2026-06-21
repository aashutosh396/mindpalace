---
name: executing-plans
description: "Use when you have a written implementation plan to execute in the current session with review checkpoints — load it, review it critically, raise concerns first, then work the tasks step-by-step with verification. Triggers: 'execute this plan', 'implement the plan', run the implementation plan, batch execution with checkpoints, inline plan execution."
version: 1.0.0
license: MIT
tags: [plan-execution, implementation, workflow, verification, checkpoints, tdd, todos]
source: https://github.com/obra/superpowers/tree/main/skills/executing-plans
derived_from: awesomeclaude
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** This skill works much better with access to subagents. If subagents are available, prefer subagent-driven-development (fresh subagent per task, review between tasks) over inline execution.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically — identify any questions or concerns about the plan
3. If concerns: raise them with your human partner before starting
4. If no concerns: create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Use the finishing-a-development-branch skill
- Verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

Pairs with: using-git-worktrees (isolated workspace), writing-plans (creates the plan this executes), finishing-a-development-branch (complete after all tasks). Alternative: subagent-driven-development for fresh-context-per-task execution.
