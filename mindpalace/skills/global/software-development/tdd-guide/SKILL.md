---
name: TDD Guide
description: Use when writing tests, improving coverage, practicing TDD, generating mocks/fixtures, or working with Jest/Pytest/JUnit/Vitest/Go — red-green-refactor, coverage gap triage, property-based and mutation testing.
tags: [tdd, testing, jest, pytest, junit, vitest, coverage, red-green-refactor, property-based-testing, mutation-testing, mocks]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/tdd-guide
---

# TDD Guide

Test generation, coverage analysis, red-green-refactor across Jest/Pytest/JUnit/Vitest/Go.

## Core Workflows
- **Generate tests from code**: source + framework → stubs covering happy path, error cases, edge cases. Validate they compile.
- **Coverage gaps**: parse LCOV/JSON/XML → triage P0 (uncovered error paths) / P1 (core logic branches) / P2 (utilities). Fill P0 first to reach 80%.
- **TDD new feature**: RED (failing test) → GREEN (minimal code) → REFACTOR (clean, tests stay green). All pass after each cycle.

## Spec-First
Write/receive spec in `specs/<feature>.md` → extract numbered acceptance criteria → one+ test per criterion → reference AC number in test docstring for traceability. Each criterion maps to a test (e.g. "locks after 5 failures" → `test_login_locks_after_five_failures`).

## Red-Green-Refactor Per Language
- **Jest**: `describe`/`it`, test add/increment/throw cases.
- **Pytest**: shared fixtures in `conftest.py` (session-scoped engine, function-scoped session with rollback); `@pytest.mark.parametrize` for tiered cases.
- **Go**: table-driven `tests := []struct{name, input, want}` + `t.Run(tt.name, ...)`.

## Bounded Autonomy
**Stop and ask** when: ambiguous/conflicting requirements · edge cases need domain knowledge · test count > 50 (summarize, ask priorities) · undocumented external deps · security-sensitive logic (auth/authz/crypto/payments need human sign-off).
**Continue** when: clear numbered ACs · straightforward CRUD · typed/OpenAPI contracts · pure functions · existing test patterns to follow.

## Property-Based Testing
Generate random inputs to verify invariants vs hand-picked examples. Python Hypothesis (`@given(st.text())`), TS fast-check (`fc.assert(fc.property(...))`). Use for: data transforms (roundtrips), math properties (commutativity/idempotency), encoding/decoding, sorting/filtering, parser correctness.

## Mutation Testing
Modify production code, check if tests catch it. Stryker (TS), mutmut (Python), PIT (Java). 100% line coverage ≠ good tests — coverage shows execution, not verification. Catches weak assertions + off-by-one (`<`→`<=`). Target 85%+ mutation score on P0 modules (auth, payments, data).

## Limitations
Unit-test focus (E2E → Playwright/Cypress); static analysis can't run tests; best for TS/JS/Python/Java; LCOV/JSON/XML only; generated tests need human review for complex logic.
