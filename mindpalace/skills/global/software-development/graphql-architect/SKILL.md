---
name: graphql-architect
description: "Use when designing GraphQL schemas, implementing Apollo Federation, or building real-time subscriptions — resolvers with DataLoader, query optimization, federation directives. Triggers: GraphQL, Apollo Federation, GraphQL schema, API graph, GraphQL subscriptions, Apollo Server, schema design, GraphQL resolvers, DataLoader."
version: 1.0.0
license: MIT
tags: [graphql, apollo-federation, schema-design, resolvers, dataloader, subscriptions, api]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/graphql-architect
derived_from: awesomeclaude
---

# GraphQL Architect

Schema design, Apollo Federation, and real-time GraphQL.

## When to use

GraphQL schema design; Apollo Federation (subgraphs/supergraph); resolvers with DataLoader; query optimization; real-time subscriptions; Apollo Server setup.

## Core workflow

1. **Model the graph** — types, relationships, nullability; schema-first SDL.
2. **Design queries/mutations** — clear naming, input types, pagination (Relay cursor connections).
3. **Implement resolvers** — DataLoader to batch + cache (kill N+1).
4. **Federate** — `@key`/`@external`/`@requires` directives; subgraph boundaries by domain.
5. **Subscriptions** — pub/sub transport for real-time; auth on the socket.

## Key practices

- Schema-first SDL; non-null where guaranteed; avoid over-nesting.
- DataLoader per request to batch resolver fetches (prevents N+1).
- Cursor-based pagination (Relay connections) over offset for large lists.
- Query cost/depth limiting + persisted queries to prevent abuse.
- Federation: one subgraph per bounded context; entities keyed with `@key`.
- Field-level authorization in resolvers/directives.

## Constraints

MUST: DataLoader for batched fetches; cursor pagination for collections; depth/cost limits; field-level authorization; schema-first design; federation `@key` on entities.
MUST NOT: N+1 resolvers (no per-item DB calls without DataLoader); unbounded queries (no depth/cost limit); leak internal fields; expose mutations without authz; deeply nested resolver chains without batching.

## Output

1. SDL schema (types, queries, mutations). 2. Resolvers with DataLoader. 3. Federation directives (if multi-subgraph). 4. Brief note on N+1 + pagination decisions.

## Knowledge

GraphQL, SDL, Apollo Server, Apollo Federation (@key/@external/@requires), DataLoader, Relay cursor connections, subscriptions/pub-sub, query cost/depth limiting, persisted queries.
