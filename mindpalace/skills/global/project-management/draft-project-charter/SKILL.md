---
name: draft-project-charter
description: "Use when kicking off a new project or initiative, formalizing scope after an informal start, or aligning stakeholders before detailed planning — produces a charter with problem statement, scope boundaries, RACI, SMART success criteria, milestones, and an initial risk register. Triggers: project charter, project kickoff, scope, stakeholders, RACI, risk register, project brief."
version: 1.0.0
license: MIT
tags: [project-charter, scope, stakeholders, raci, risk-register, milestones, project-management, kickoff]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/draft-project-charter
derived_from: awesomeclaude
---

# Draft a Project Charter

Establish project boundaries, stakeholder agreements, and success criteria before detailed planning. Works for agile, classic, or hybrid.

## When to Use

- Kicking off a new project or initiative
- Formalizing scope after an informal start
- Aligning stakeholders before detailed planning
- Transitioning from discovery to active work

## Inputs

- Required: project name + brief description, primary sponsor/stakeholder
- Optional: existing docs (proposals, briefs, emails), known constraints, methodology preference

## Procedure

### Step 1 — Context and template
Read any existing docs. Create `PROJECT-CHARTER-[NAME].md` with ID `PC-[PROJECT]-[YYYY]-[NNN]`. Write a 2-3 sentence problem statement (situation, gap, impact) and a one-paragraph purpose. If context is unclear, add a QUESTIONS section for the sponsor; note contradictions in OPEN ISSUES.

### Step 2 — Scope boundaries
Write 3-5 in-scope deliverables (each with testable acceptance criteria and target date) and 3-5 explicit out-of-scope items to prevent scope creep. If a deliverable is vague, ask "how would we demonstrate this is complete?"

### Step 3 — Stakeholders + RACI
List 5-10 stakeholders with roles. Build a RACI matrix mapping each stakeholder to each deliverable. Exactly one Accountable per deliverable, at least one Responsible. Sponsor is Accountable for final approval. Escalate multiple-A conflicts to the sponsor.

### Step 4 — Success criteria + milestones
Write 3-5 SMART success criteria, each with a measure and target value (baseline → target). Define 4-6 milestones with target dates and dependencies. Work backward from the final deadline with buffers if dates seem unrealistic.

### Step 5 — Initial risk register
Identify 5-10 risks covering scope, schedule, resource, technical, and external. For each: likelihood, impact, severity (L×I), specific mitigation, and an owner. Replace generic "monitor closely" with what/how-often/what-triggers-action.

## Validation

- [ ] Charter file with document ID
- [ ] Specific, measurable problem statement
- [ ] In-scope and out-of-scope both defined
- [ ] RACI covers all deliverables (one A each)
- [ ] SMART success criteria
- [ ] >=5 risks with mitigations and owners
- [ ] Milestones with target dates; approval section

## Common Pitfalls

- Scope without explicit boundaries (scope creep).
- Vague success criteria — tie every one to a number.
- Missing stakeholders surfacing late.
- Risk register as a checkbox without real mitigations.
- Over-detailed charter — keep it 2-4 pages; it's a compass, not a map.

## Related

- manage-backlog — translate charter scope into a prioritized backlog
- conduct-retrospective — review charter assumptions after execution
