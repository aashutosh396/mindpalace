---
name: deliver-prd
description: "Use when specifying a feature, epic, or product initiative for engineering handoff — write a Product Requirements Document covering problem, goals, success metrics, scope, requirements, risks. Triggers: PRD, product requirements document, spec a feature, requirements doc, engineering handoff, write a spec."
version: 1.0.0
license: Apache-2.0
tags: [prd, product-requirements, spec, requirements, scope, success-metrics, engineering-handoff, product-management]
source: https://github.com/product-on-purpose/pm-skills/tree/main/skills/deliver-prd
derived_from: awesomeclaude
---

# Product Requirements Document (PRD)

A PRD is the primary specification artifact: it communicates what to build and why, bridging problem understanding and engineering implementation. A good PRD enables engineering to build the right thing while keeping flexibility on implementation details.

## When to use

- After problem and solution alignment, before engineering work begins
- When specifying features, epics, or initiatives for handoff
- When multiple people/teams must coordinate on a shared deliverable
- When stakeholders need to approve scope before investment
- As reference documentation during development and QA

## When NOT to use

- Problem is still unframed or contested → frame it first (problem statement)
- You only need a one-page pitch to align on an approach → solution brief
- You only need the work broken into sprint tickets → user stories
- You are recording a technical/architectural decision → ADR

## How

1. **Summarize the problem.** Brief recap of why this work matters before what to build.
2. **Define goals & success metrics.** Specific, measurable, with baseline and target, tied to the problem.
3. **Outline the solution.** High-level user-facing functionality; enough to evaluate, not over-specified.
4. **Detail functional requirements.** Testable requirement statements or user stories — each verifiable.
5. **Define scope boundaries.** Explicit in-scope / out-of-scope / deferred. Prevents scope creep.
6. **Address technical considerations.** Surface constraints, integrations, architectural notes — don't design the system.
7. **Identify dependencies & risks.** External deps, assumptions, risks, with mitigations and owners.
8. **Propose timeline & milestones.** Key phases and checkpoints without over-committing to dates.

## Output sections

Overview; Goals & Success Metrics; User Stories; Scope (in/out/future); Solution Design; Technical Considerations; Dependencies & Risks; Timeline & Milestones; Open Questions; Appendix (when supporting material exists).

## Quality checklist

- [ ] Problem and "why now" are clear
- [ ] Success metrics are specific and measurable
- [ ] Scope boundaries explicit (in/out/future)
- [ ] Requirements testable and unambiguous
- [ ] Technical considerations surfaced without over-specifying
- [ ] Dependencies/risks documented with owners
- [ ] Readable in under 15 minutes
