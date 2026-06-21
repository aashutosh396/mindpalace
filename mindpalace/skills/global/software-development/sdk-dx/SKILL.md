---
name: sdk-dx
description: Use when designing SDKs or client libraries for great developer experience — API design, error messages that guide, type safety, IDE/autocomplete integration, SDK versioning, deprecation, and migration guides.
version: 1.0.0
license: MIT
tags: [sdk, developer-experience, api-design, error-messages, type-safety, versioning, migration, client-library]
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/sdk-dx
derived_from: awesomeclaude
---

# SDK Design & Developer Experience

The best SDK marketing is an SDK developers can't stop talking about. DX spans discovery, learning, daily use, debugging, and upgrading. Developers choose tools that make them feel smart.

## API design principles

1. **Optimize for the common case** — the most frequent use needs the least code; offer full control via optional params.
2. **Progressive disclosure** — simplest call works; add options as needed; full control available but not required.
3. **Fail fast and clearly** — validate at construction (empty key raises immediately with a fix), specific runtime errors (NotFoundError naming the resource), never silently return None.
4. **Sensible defaults** — auto-retry with backoff, reasonable timeouts, JSON, auth headers, connection pooling all work without config.

## Error messages that guide

Every error answers: what happened, why, how to fix. Bad: `Error: 401 Unauthorized`. Good: states the problem, the cause (test key used in production), numbered fix steps, and a docs link.

Create specific catchable types: AuthenticationError, AuthorizationError, ValidationError, NotFoundError, RateLimitError, ServerError. Include context in errors (field, value, expected format, docs).

## Type safety

Types are docs that never go stale. Define explicit input/output types; use discriminated unions for responses (`{success:true,data}` | `{success:false,error}`). Design for autocomplete (namespaced methods so `client.users.` reveals operations). Use enum/literal types for constrained values, not bare `string`.

## IDE integration

Namespace methods logically (`client.users.get/list/create/update/delete`). Add JSDoc/docstrings everywhere with `@param`, `@returns`, `@throws`, and `@example`. Include runnable inline examples in docstrings.

## Versioning

Strict semver. **Breaking (major)**: removing public method/property, changing signatures or return types, changing default behavior, dropping runtime support. **Non-breaking (minor/patch)**: adding methods, adding optional params, deprecating (not removing), bug fixes.

Deprecation process: emit a `DeprecationWarning` pointing to the replacement and migration guide, keep the old method working until the next major.

## Migration guides

Structure: overview (what changed, time estimate) → breaking changes (before/after code + why for each) → removed deprecated features → new features (why migrating is worth it) → where to get help. Provide automation where possible (migration scripts, codemods via jscodeshift).

## Make SDKs feel native

Use language idioms: Python (snake_case, context managers, generators); JavaScript (Promises/async-await, destructuring); Go (error returns, `fmt.Errorf("...: %w", err)`, never panic). Match ecosystem conventions: expected package manager (npm/pip/gem/go get), naming of popular libraries, integration with popular frameworks, standard testing patterns.

## Quality checklist

Before release: all public APIs documented and typed, errors include remediation, doc examples auto-tested, changelog updated, migration guide for breaking changes, deprecation warnings. For great DX: quickstart succeeds in <5 min, autocomplete works for all ops, errors catchable by type, retry handles transient failures, configurable useful logging, debug mode showing request/response.

## Tools

SDK generation: OpenAPI Generator, Swagger Codegen, Speakeasy, Fern. Testing: VCR/Betamax, WireMock, Pact. Docs: TypeDoc, Sphinx, GoDoc, YARD.
