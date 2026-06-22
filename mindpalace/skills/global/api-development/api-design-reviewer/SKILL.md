---
name: API Design Reviewer
description: Use when reviewing a PR that adds/changes API endpoints, auditing an API for v2 migration, or establishing team API standards — automated linting, breaking-change detection, and design scorecards.
tags: [api-design, rest, openapi, linting, breaking-changes, versioning, pagination, scorecard, http-status, idempotency]
source: alirezarezvani/claude-skills
derived_from: api-design-reviewer
---

# API Design Reviewer

REST API design review with automated linting, breaking-change detection, and design scorecards. Never sign off on prose alone — attach the tool outputs.

## Review flow
1. **Lint** the OpenAPI/Swagger spec for convention violations.
2. **Detect breaking changes** between two spec versions (gate: fail on breaking unless version-bumped).
3. **Score design quality** (gate: fails below `--min-grade`).
Run all three, report findings + grade, fix, re-run until linter clean, breaking-change gate passes, and scorecard meets the agreed grade.

## REST conventions
- Resource naming: kebab-case URLs, camelCase fields. Nouns not verbs (`/users` not `/getUsers`).
- HTTP methods: GET (safe/idempotent), POST (create), PUT (replace/idempotent), PATCH (partial), DELETE (idempotent).
- URLs: collection `/v1/users`, item `/v1/users/123`, nested `/v1/users/123/orders`, actions `/v1/users/123/activate` (POST), filtering via query params.

## Versioning
URL versioning (recommended — clear, easy to route), header, media-type, or query-param versioning.

## Pagination patterns
Offset-based (offset/limit/total/hasMore), cursor-based (nextCursor/hasMore), page-based (page/pageSize/totalPages).

## Error response standard
`{ error: { code, message, details[{field, code, message}], requestId, timestamp } }`. Status codes: 400 bad request, 401 unauthorized, 403 forbidden, 404 not found, 409 conflict, 422 unprocessable, 429 rate limit, 500 server error.

## Scoring dimensions
Consistency 30% · Documentation 20% · Security 20% · Usability 15% · Performance 15%. Letter grade A–F.

## Breaking vs safe changes
**Safe (non-breaking)**: add optional request fields, add response fields, add endpoints, make required fields optional, add enum values (with graceful handling).
**Breaking (version bump)**: remove response fields, make optional fields required, change field types, remove endpoints, change URL structure, modify error formats.

## Other essentials
Idempotency keys for unsafe operations (`Idempotency-Key` header). Rate-limit headers (`X-RateLimit-*`). Auth: Bearer token / API key / OAuth 2.0 / RBAC. Caching: `Cache-Control`, `ETag`, conditional requests. Field selection (`?fields=`), compression, batch operations.

## Anti-patterns
Verb-based URLs · inconsistent response formats · over-nesting · ignoring status codes · poor error messages · missing pagination · no versioning strategy · exposing internal structure · missing rate limiting · inadequate error-case testing.
