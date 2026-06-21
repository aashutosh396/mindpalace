---
name: test-master
description: "Use when writing unit/integration/E2E tests, creating test strategies or automation frameworks, analyzing coverage gaps, load testing (k6/Artillery), security testing, or fixing flaky tests. Triggers: test, testing, QA, unit test, integration test, E2E, coverage, performance test, security test, regression, test strategy, test automation, quality gate, flaky test."
version: 1.0.0
license: MIT
tags: [testing, qa, unit-test, integration-test, e2e, coverage, load-testing, flaky-tests]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/test-master
derived_from: awesomeclaude
---

# Test Master

Comprehensive testing across functional, performance, and security disciplines.

## When to use

Writing tests at any level, building strategies/frameworks, analyzing coverage, load/security testing, or stabilizing flaky tests.

## Core workflow

1. **Define scope** — what to test and which test types apply.
2. **Create strategy** — functional, performance, security perspectives.
3. **Write tests** — proper assertions, isolated dependencies.
4. **Execute** — run and collect results. On failure, classify (assertion vs environment/flakiness), fix root cause, re-run. For flaky: isolate ordering deps, check async handling, stabilize.
5. **Report** — findings with severity + actionable fixes; verify coverage targets, flag gaps.

## Quick-start example

```js
describe('calculateDiscount', () => {
  it('applies 10% discount for premium users', () => {
    expect(calculateDiscount({ price: 100, userTier: 'premium' })).toBe(90); // specific, not truthy
  });
  it('throws on negative price', () => {
    expect(() => calculateDiscount({ price: -1, userTier: 'standard' }))
      .toThrow('Price must be non-negative');
  });
});
```
Apply the same structure for pytest (`def test_…`, `assert result == expected`).

## Constraints

MUST: test happy paths AND error/edge cases (empty, null, boundary); mock external deps in unit tests; use plain-English `it('…')` descriptions; assert specific outcomes; run in CI and remediate coverage gaps.
MUST NOT: skip error-path testing; use production data (use fixtures/factories); create order-dependent tests; ignore flaky tests (quarantine + fix, don't just re-run); test implementation details — test observable behavior.

## Output

1. Test scope and approach
2. Test cases with expected outcomes
3. Coverage analysis
4. Findings with severity (Critical/High/Medium/Low)
5. Specific fix recommendations
