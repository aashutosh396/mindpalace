---
name: Spec-Driven Workflow
description: Use when the user wants specs before code, acceptance criteria, feature planning before implementation, or tests generated from specifications — enforces spec-first development with the iron law "no code without an approved spec".
tags: [spec, acceptance-criteria, rfc-2119, given-when-then, tdd, requirements, scope-control, bounded-autonomy]
source: alirezarezvani/claude-skills
derived_from: spec-driven-workflow
---

# Spec-Driven Workflow

One non-negotiable rule: **write the spec BEFORE any code.** A spec is a contract — what the system MUST do, SHOULD do, and WILL NOT do. Every line of code traces to a requirement; every test to an acceptance criterion. **NO CODE WITHOUT AN APPROVED SPEC. NO EXCEPTIONS.**

## Why spec-first
60–80% of defects originate in requirements, not implementation. Catching ambiguity in a spec costs minutes; in production, days. Specs force clarity, enable parallelism (FE/BE/QA/docs start together once approved), create accountability (spec = definition of done), and feed TDD (Given/When/Then → test cases 1:1).

## The spec format (9 mandatory sections)
1. Title + Metadata (author, date, status, reviewers). 2. Context (why, with evidence). 3. Functional Requirements (RFC 2119 keywords, numbered FR-N, atomic + testable). 4. Non-Functional Requirements (measurable thresholds). 5. Acceptance Criteria (Given/When/Then, each references an FR/NFR). 6. Edge Cases (EC-N, failure modes for every external dependency). 7. API Contracts (typed interfaces, success + error). 8. Data Models (field/type/constraints). 9. Out of Scope (explicit exclusions with reasons).
If a section doesn't apply, write "N/A — [reason]" so reviewers know it was considered.

**RFC 2119**: MUST (absolute), MUST NOT (prohibition), SHOULD (recommended; omit only with justification), MAY (optional).

## 6-phase workflow
1. **Gather requirements** — interview (problem? users? success? what NOT to build?), read existing code, identify constraints, list unknowns. Exit: can explain feature in 2 min.
2. **Write spec** — fill every section, number all requirements, precise RFC 2119, Given/When/Then ACs, typed API contracts. Exit: a dev not in the meeting can implement without clarifying questions.
3. **Validate spec** — run validator (0–100), score 80+, all manual checklist items pass (every FR has an AC; every AC testable; contracts/models cover all entities; edge cases cover dependency failures; NFRs measurable).
4. **Generate tests** — each AC and EC → test stubs; all fail initially (red phase).
5. **Implement** — one AC at a time, minimal code to pass, full suite green, commit, repeat. Do NOT build anything not in spec; do NOT optimize/refactor before all ACs pass; if you find a missing requirement, STOP and update the spec.
6. **Self-review** — verify implementation matches spec via checklist.

## Bounded autonomy — STOP and ask when
1. Scope creep (something not in spec). 2. Ambiguity >30% of a requirement. 3. Breaking changes to an API/schema/interface. 4. Security implications (auth/authz/encryption/PII). 5. Unknown performance characteristics. 6. Cross-team dependencies.
**Continue autonomously** when spec is clear, ACs have passing tests and you're refactoring internals, changes are non-breaking, implementation is a direct AC translation, or error handling follows documented patterns.

**Escalation format**: Blocked on [FR-id] · specific answerable Question · Options A/B with pros/cons · My recommendation (always give one) · Impact of waiting. Never escalate open-ended.

## Self-review checklist
Every AC has a passing test · every EC has a test · no scope creep · API contracts match code exactly · error scenarios tested · NFRs verified with evidence · data model matches · out-of-scope items not built.

## Anti-patterns
Coding before approval · vague ACs ("works well") · missing edge cases · spec written after the code (that's documentation) · gold-plating beyond spec · ACs without FR/NFR traceability · skipping validation.
