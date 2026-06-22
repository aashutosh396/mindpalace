---
name: API Test Suite Builder
description: Use when generating API tests, building integration test suites, testing REST endpoints, or creating contract tests — scans routes and auto-generates auth/validation/error/pagination/upload/rate-limit coverage.
tags: [api-testing, integration-tests, rest, contract-tests, vitest, supertest, pytest, httpx, auth-tests, validation]
source: alirezarezvani/claude-skills
derived_from: api-test-suite-builder
---

# API Test Suite Builder

Scan API routes across frameworks (Next.js App Router, Express, FastAPI, Django REST) and auto-generate test suites covering auth, input validation, error codes, pagination, file uploads, and rate limiting. Output: Vitest+Supertest (Node) or Pytest+httpx (Python).

## Route detection
- **Next.js**: find `app/api/**/route.ts`, grep exported HTTP method functions.
- **Express**: grep `router.(get|post|put|delete|patch)(`.
- **FastAPI**: grep `@app.`/`@router.` decorators.
- **Django REST**: extract `urlpatterns` paths + `router.register` ViewSets.

## Generation process
1. Scan routes. 2. Read each handler for request schema, auth requirements, return types/status codes, business rules (ownership, role checks). 3. Generate one test file per route group. 4. Name tests descriptively ("returns 401 when token is expired"). 5. Use factories/fixtures — never hardcode IDs. 6. Assert response shape, not just status code.

## Auth test matrix (every authenticated endpoint)
No Authorization header → 401 · invalid token format → 401 · valid token wrong role → 403 · expired JWT → 401 · valid + correct role → 2xx · token from deleted user → 401.

## Input validation matrix (every body endpoint)
Empty body → 400/422 · each missing required field → 400/422 · wrong type → 400/422 · boundary min-1/min/max/max+1 · SQL injection / XSS payload → 400 or sanitized 200 · null for required → 400/422.

## Common pitfalls
Testing only happy paths (80% of bugs are in error paths) · hardcoded IDs · shared state between tests (clean up in afterEach/afterAll) · testing implementation not behavior · missing boundary tests (off-by-one in pagination) · not testing token expiry vs invalid · ignoring Content-Type rejection.

## Best practices
One describe block per endpoint · seed minimal data · `beforeAll`/`afterAll` for expensive setup/cleanup · assert specific error fields/messages · verify sensitive fields (password, secret) never appear in responses · test "missing header" separately from "invalid token" · add rate-limit tests last (they interfere with parallel suites).
