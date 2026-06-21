---
name: api-designer
description: "Use when designing REST or GraphQL APIs, creating OpenAPI specifications, or planning API architecture. Covers resource modeling, versioning, pagination, error handling (RFC 7807), and contract validation. Triggers: API design, REST API, OpenAPI, API specification, API architecture, resource modeling, API versioning, GraphQL schema."
version: 1.0.0
license: MIT
tags: [api-design, rest, openapi, graphql, rfc7807, pagination, versioning, http]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/api-designer
derived_from: awesomeclaude
---

# API Designer

Design REST and GraphQL APIs with comprehensive OpenAPI 3.1 specifications.

## When to use

Designing new APIs, writing OpenAPI specs, planning versioning/pagination/error standards, or reviewing an API surface.

## Core workflow

1. **Analyze domain** — Business requirements, data models, client needs.
2. **Model resources** — Identify resources, relationships, operations; sketch an entity diagram first.
3. **Design endpoints** — URI patterns, HTTP methods, request/response schemas.
4. **Specify contract** — OpenAPI 3.1 spec; validate: `npx @redocly/cli lint openapi.yaml`.
5. **Mock and verify** — `npx @stoplight/prism-cli mock openapi.yaml`.
6. **Plan evolution** — Versioning, deprecation, backward compatibility.

## Constraints

MUST: resource-oriented design, proper HTTP methods; one consistent naming convention; full OpenAPI 3.1 spec; RFC 7807 error responses with actionable messages; pagination on all collections; clear version + deprecation policy; document auth; provide examples.
MUST NOT: verbs in URIs (`/users/{id}` not `/getUser/{id}`); inconsistent response shapes; undocumented error codes; ignore HTTP status semantics; ship without a versioning strategy; expose implementation details; create breaking changes without a migration path; omit rate limiting.

## Starter templates

OpenAPI cursor-paginated collection + RFC 7807 errors:
```yaml
openapi: "3.1.0"
info: { title: Example API, version: "1.0.0" }
paths:
  /users:
    get:
      operationId: listUsers
      parameters:
        - { name: cursor, in: query, schema: { type: string } }
        - { name: limit, in: query, schema: { type: integer, default: 20, maximum: 100 } }
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [data, pagination]
                properties:
                  data: { type: array, items: { $ref: "#/components/schemas/User" } }
                  pagination: { $ref: "#/components/schemas/CursorPage" }
components:
  schemas:
    CursorPage:
      type: object
      required: [next_cursor, has_more]
      properties:
        next_cursor: { type: string, nullable: true }
        has_more: { type: boolean }
    Problem:   # RFC 7807
      type: object
      required: [type, title, status]
      properties:
        type: { type: string, format: uri }
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
```

RFC 7807 error body (always `Content-Type: application/problem+json`):
```json
{ "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error", "status": 422,
  "detail": "The 'email' field must be a valid email address.",
  "errors": [{ "field": "email", "message": "Must be a valid email address." }] }
```
- `type` must be a stable, documented URI — never a generic string.
- `detail` must be human-readable and actionable. Extend with `errors[]` for field-level failures.

## Output checklist

Resource model + relationships; endpoint specs (URI + method); OpenAPI 3.1 YAML; auth/authz flows; error catalog (all 4xx/5xx with `type` URIs); pagination/filtering patterns; versioning/deprecation strategy; lint passes clean.
