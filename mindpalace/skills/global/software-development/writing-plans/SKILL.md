---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step coding task, before touching code — write a comprehensive implementation plan as bite-sized, independently testable tasks with exact file paths, complete code, exact commands, and expected output. Triggers: 'write a plan', 'plan this feature', break work into tasks, implementation plan, spec to tasks, TDD task breakdown."
version: 1.0.0
license: MIT
tags: [planning, implementation-plan, task-decomposition, tdd, spec, file-structure, workflow, no-placeholders]
source: https://github.com/obra/superpowers/tree/main/skills/writing-plans
derived_from: awesomeclaude
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything they need: which files to touch per task, the actual code, testing, docs to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer but know almost nothing about your toolset or problem domain, and don't know good test design well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` (user preferences override this default).

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking it into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each is responsible for.

- Design units with clear boundaries and well-defined interfaces. One clear responsibility per file.
- Prefer smaller, focused files over large ones — you reason and edit more reliably about code you can hold in context at once.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. Don't unilaterally restructure, but a split is reasonable if a file you're modifying has grown unwieldy.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate. Fold setup, configuration, scaffolding, and documentation into the task whose deliverable needs them; split only where a reviewer could meaningfully reject one task while approving its neighbor. Each task ends with an independently testable deliverable.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

Every plan MUST start with this header:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[Project-wide requirements — version floors, dependency limits, naming and
copy rules, platform requirements — one line each, with exact values copied
verbatim from the spec. Every task's requirements implicitly include this.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact names, parameter and return
  types. A task's implementer sees only their own task; this block is how
  they learn neighboring tasks' names and types.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are plan failures — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — they may read tasks out of order)
- Steps describing what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After writing the complete plan, check it against the spec with fresh eyes:

1. **Spec coverage:** Can you point to a task for each spec section/requirement? List gaps.
2. **Placeholder scan:** Search for the red flags above. Fix them.
3. **Type consistency:** Do types, signatures, and property names in later tasks match earlier definitions? (`clearLayers()` in Task 3 vs `clearFullLayers()` in Task 7 is a bug.)

Fix issues inline. If a spec requirement has no task, add the task.

## Execution Handoff

After saving the plan, offer the execution choice: subagent-driven (recommended — fresh subagent per task, review between tasks) or inline execution (executing-plans, batch with checkpoints).
