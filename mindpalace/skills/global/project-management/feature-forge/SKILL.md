---
name: feature-forge
description: "Use when defining new features, gathering requirements, or writing specifications. Conducts structured requirements workshops to produce feature specs, user stories, EARS-format functional requirements, acceptance criteria, and implementation checklists. Triggers: requirements, specification, feature definition, user stories, EARS, PRD, acceptance criteria, requirement matrix."
version: 1.0.0
license: MIT
tags: [requirements, specification, user-stories, ears, acceptance-criteria, prd, product, planning]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/feature-forge
derived_from: awesomeclaude
---

# Feature Forge

Structured requirements workshops producing comprehensive feature specifications. Operate with two hats: PM (user value, business goals, success metrics) and Dev (feasibility, security, performance, edge cases).

## When to use

Defining new features, gathering requirements, writing EARS-format specs, creating acceptance criteria, planning implementation checklists.

## Core workflow

1. **Discover** — understand feature goal, target users, user value (structured choices where possible).
2. **Interview** — systematic questioning from PM and Dev perspectives; use subagents for multi-domain features.
3. **Document** — write EARS-format requirements.
4. **Validate** — review acceptance criteria with stakeholder, surfacing key trade-offs.
5. **Plan** — create implementation checklist.

## Constraints

MUST: structured elicitation (priority, scope, format choices); open-ended questions only when choices can't be predetermined; thorough interview before writing the spec; EARS for all functional requirements; include NFRs (performance, security); testable acceptance criteria; implementation TODO checklist; clarify ambiguity.
MUST NOT: generate a spec without an interview; accept vague requirements ("make it fast"); skip security; forget error handling; write untestable acceptance criteria.

## Output template

Final spec includes: 1) Overview + user value; 2) Functional requirements (EARS); 3) Non-functional requirements; 4) Acceptance criteria (Given/When/Then); 5) Error-handling table; 6) Implementation TODO checklist.

EARS format:
```
When <trigger>, the <system> shall <response>.
Where <feature> is active, the <system> shall <behaviour>.
The <system> shall <action> within <measure>.
```
Acceptance criteria:
```
Given a registered user is on the login page,
When they submit valid credentials,
Then they are redirected to the dashboard within 2 seconds.
```
Save as: `specs/{feature_name}.spec.md`
