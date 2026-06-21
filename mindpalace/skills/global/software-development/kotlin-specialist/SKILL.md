---
name: kotlin-specialist
description: "Use when building Kotlin apps needing coroutine concurrency, Flow streams, Kotlin Multiplatform (KMP), Jetpack Compose UI, Ktor servers, or type-safe DSLs. Triggers: Kotlin, coroutines, Kotlin Multiplatform, KMP, Jetpack Compose, Ktor, Flow, Android Kotlin, suspend function, sealed classes."
version: 1.0.0
license: MIT
tags: [kotlin, coroutines, flow, kmp, jetpack-compose, ktor, android, dsl]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/kotlin-specialist
derived_from: awesomeclaude
---

# Kotlin Specialist

Idiomatic Kotlin: coroutines, Flow, multiplatform, Compose, Ktor.

## When to use

Coroutine concurrency; Flow stream handling; Kotlin Multiplatform (KMP) projects; Android with Jetpack Compose; Ktor servers; type-safe DSL design.

## Core workflow

1. **Analyze** — module/target layout (common/jvm/native), Gradle config.
2. **Design** — sealed classes for state, data classes, interfaces.
3. **Implement** — coroutines with structured concurrency; Flow for streams.
4. **UI / server** — Compose state hoisting; or Ktor routes + plugins.
5. **Test** — `runTest`, Turbine for Flow, MockK; verify cancellation behavior.

## Key practices

- Structured concurrency: scope-bound `launch`/`async`; never `GlobalScope`.
- `suspend` functions main-safe via `withContext(Dispatchers.IO)`.
- Flow: cold streams, `flowOn` for upstream dispatcher, collect in scope.
- Sealed classes/interfaces for exhaustive `when` state machines.
- KMP: shared business logic in `commonMain`, platform code via `expect`/`actual`.
- Compose: hoist state, remember, key stable; avoid recomposition pitfalls.

## Constraints

MUST: structured concurrency (scoped); main-safe suspend functions; sealed types for state; exhaustive `when`; cancellation cooperation (`ensureActive`/`isActive`); test with `runTest`.
MUST NOT: `GlobalScope`; block in coroutines (`Thread.sleep`/blocking I/O on Main); swallow `CancellationException`; mutable shared state without sync; leak Android contexts.

## Output

1. Sealed/data model types. 2. Coroutine/Flow implementation. 3. Compose or Ktor wiring. 4. Tests. 5. Brief note on concurrency design.

## Knowledge

Kotlin, coroutines, Flow/StateFlow/SharedFlow, structured concurrency, KMP (expect/actual), Jetpack Compose, Ktor, sealed classes, DSL builders, MockK, Turbine.
