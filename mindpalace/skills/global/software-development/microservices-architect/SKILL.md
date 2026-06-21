---
name: microservices-architect
description: "Use when designing distributed systems, decomposing monoliths into bounded-context services, or implementing microservices patterns — service boundaries, DDD, saga, event sourcing, CQRS, service mesh, distributed tracing. Triggers: microservices, service mesh, distributed systems, service boundaries, domain-driven design, event sourcing, CQRS, saga pattern, Istio, distributed tracing."
version: 1.0.0
license: MIT
tags: [microservices, ddd, saga, event-sourcing, cqrs, service-mesh, distributed-systems, tracing]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/microservices-architect
derived_from: awesomeclaude
---

# Microservices Architect

Distributed system design and monolith decomposition.

## When to use

Designing distributed systems; decomposing monoliths into bounded contexts; communication patterns; service boundary + resilience strategies; saga, event sourcing, CQRS, service mesh, distributed tracing.

## Core workflow

1. **Domain analysis** — identify bounded contexts (DDD); map data ownership.
2. **Define boundaries** — one service per bounded context; each owns its data.
3. **Communication** — sync (REST/gRPC) vs async (events); choose per interaction.
4. **Consistency** — saga for distributed transactions; event sourcing/CQRS where it fits.
5. **Resilience + observability** — timeouts, retries, circuit breakers; service mesh; distributed tracing.

## Key practices

- Database-per-service; no shared DB across service boundaries.
- Async events for decoupling; sync only where strong consistency/latency demands.
- Saga (choreography or orchestration) for cross-service transactions; compensating actions.
- Idempotent consumers; outbox pattern for reliable event publishing.
- Circuit breakers, timeouts, bulkheads; mesh (Istio/Linkerd) for mTLS + traffic policy.
- Distributed tracing (OpenTelemetry) + correlation IDs end to end.

## Constraints

MUST: bounded contexts drive service boundaries; database-per-service; idempotent event consumers; resilience (timeout/retry/circuit-breaker); distributed tracing + correlation IDs; saga + compensation for cross-service consistency.
MUST NOT: shared database across services; distributed monolith (chatty sync coupling); two-phase commit across services; ignore partial-failure handling; unbounded retries without backoff; lose trace context across hops.

## Output

1. Service boundary map (bounded contexts + data ownership). 2. Communication + consistency strategy. 3. Resilience + observability plan. 4. Brief note on key trade-offs.

## Knowledge

Microservices, DDD/bounded contexts, database-per-service, REST/gRPC, event-driven, saga (orchestration/choreography), outbox, event sourcing, CQRS, circuit breakers, service mesh (Istio/Linkerd), OpenTelemetry tracing.
