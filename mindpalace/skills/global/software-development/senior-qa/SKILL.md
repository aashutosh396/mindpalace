---
name: Senior QA Engineer
description: Use when you need to generate tests, analyze coverage, or set up E2E testing for React/Next.js apps — scaffolds Jest + RTL unit tests, Playwright E2E, MSW mocks, and reads Istanbul/LCOV coverage to surface gaps.
tags: [testing, jest, playwright, react-testing-library, coverage, e2e, msw, qa, nextjs]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-qa
---

# Senior QA Engineer

Test automation, coverage analysis, and QA patterns for React/Next.js.

## Three workflows

### 1. Unit test generation (Jest + React Testing Library)
1. Scan for untested components.
2. Generate test stubs — describe blocks, render tests, interaction tests.
3. Review/customize. Each component gets: a render-with-props test + an interaction (`fireEvent` / `userEvent`) test + accessibility queries.
4. Run with coverage: `npm test -- --coverage`.

Stub shape:
```tsx
describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### 2. Coverage analysis
1. Generate report: `npm test -- --coverage --coverageReporters=json`.
2. Parse Istanbul/LCOV → identify uncovered branches and critical paths.
3. Enforce threshold (exit non-zero below target). Set in `jest.config.js`:
```js
coverageThreshold: { global: { branches: 80, functions: 80, lines: 80, statements: 80 } }
```
4. Generate stubs for uncovered code, re-run, compare against previous.

### 3. E2E setup (Playwright)
1. `npm init playwright@latest`.
2. Scaffold tests from Next.js routes (one file per route, common interactions).
3. Configure auth fixtures (login once, reuse authenticated page).
4. Run: `npx playwright test`; report: `npx playwright show-report`.
5. Add to CI (run tests + upload `playwright-report/` artifact).

## Key patterns

**RTL queries (prefer accessible):** `getByRole('button', { name: /submit/i })`, `getByLabelText(/email/i)`; fall back to `getByTestId`.

**Async:** `await screen.findByText(...)`, `waitForElementToBeRemoved(...)`, `waitFor(() => expect(mockFn).toHaveBeenCalled())`.

**MSW mocking:**
```ts
const server = setupServer(rest.get('/api/users', (_, res, ctx) => res(ctx.json([{ id: 1 }]))));
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Playwright locators:** `page.getByRole('button', { name: 'submit' })`, chain with `.filter({ hasText: 'Product' })`.

## Strategy: test pyramid — many unit, fewer integration, fewest E2E. Target 80% coverage on critical paths; don't chase 100%. Stabilize flaky tests by removing arbitrary waits and using web-first assertions.
