---
name: deliver-acceptance-criteria
description: "Use when turning a user story or feature slice into verifiable pass/fail conditions — write Given/When/Then acceptance criteria covering happy path, failure/recovery, and non-functional expectations for engineering and QA. Triggers: acceptance criteria, Given/When/Then, definition of done, QA criteria, testable scenarios, story acceptance, pass/fail conditions."
version: 1.0.0
license: Apache-2.0
tags: [acceptance-criteria, given-when-then, gherkin, qa, definition-of-done, user-story, testable-scenarios, engineering-handoff]
source: https://github.com/product-on-purpose/pm-skills/tree/main/skills/deliver-acceptance-criteria
derived_from: awesomeclaude
---

# Acceptance Criteria

Acceptance criteria define the observable behavior that must be true for a story or feature to be done. This skill turns feature context into concise, testable Given/When/Then scenarios that engineers and QA can verify without guessing intent.

## When to use

- After a user story, PRD section, or feature slice is defined
- When a team needs clear pass/fail conditions for implementation
- When writing QA-ready criteria for sprint planning or handoff
- When a story has edge cases, error paths, or non-functional expectations to make explicit

## When NOT to use

- You need the user stories themselves → user stories (this deepens an existing story)
- You need systematic failure coverage across a whole feature → edge cases (this stays story-scoped)
- No story/slice to bind to yet → write the PRD or stories first
- You're defining experiment success metrics, not story done-ness → experiment design

## How

1. **Confirm scope.** Identify the exact slice; if unclear, ask for the story/PRD section first.
2. **Separate happy path from exceptions.** Primary success flow first, then likely or costly edge/error cases.
3. **Write each criterion as an observable scenario.** Given/When/Then only; independently testable; no implementation details.
4. **Cover recovery and failure.** What the user sees/can do when validation fails, a dependency is down, or a save can't complete.
5. **Include non-functional expectations.** Performance, accessibility, security, reliability, auditability when they matter.
6. **Avoid duplication.** One outcome per criterion; merge or split overlapping ones.
7. **Review for testability.** A reviewer must pass/fail each without interpretation; rewrite subjective statements into measurable outcomes.

## Output

Use Given/When/Then throughout. Group: Happy Path; Failure & Recovery; Non-Functional. Each criterion independently verifiable.

## Quality checklist

- [ ] Scope bound to a specific story/slice
- [ ] Happy path and key failure paths both covered
- [ ] Recovery behavior described
- [ ] Non-functional expectations included where relevant
- [ ] Each criterion observable and testable without interpretation
- [ ] No duplicate or overlapping criteria
