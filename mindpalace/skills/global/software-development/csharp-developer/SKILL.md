---
name: csharp-developer
description: "Use when building C# / .NET 8+ apps, ASP.NET Core APIs (minimal or controller), or Blazor web apps. Builds EF Core data access, async + cancellation patterns, CQRS via MediatR, and Blazor components. Triggers: C#, .NET, ASP.NET Core, Blazor, Entity Framework, EF Core, Minimal API, MAUI, SignalR, CQRS, MediatR."
version: 1.0.0
license: MIT
tags: [csharp, dotnet, aspnet-core, blazor, ef-core, minimal-api, cqrs, signalr]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/csharp-developer
derived_from: awesomeclaude
---

# C# Developer

C# / .NET 8+: ASP.NET Core APIs, Blazor, EF Core.

## When to use

REST APIs (minimal or controller-based); EF Core data access; async + cancellation; CQRS via MediatR; Blazor components with state; SignalR; MAUI.

## Core workflow

1. **Analyze** — project type, .NET version, dependency graph.
2. **Design** — records for DTOs, interfaces, CQRS commands/queries.
3. **Implement** — endpoints, EF Core context, MediatR handlers.
4. **Async** — `async`/`await` end to end; thread `CancellationToken`.
5. **Test** — xUnit + `WebApplicationFactory` integration tests; EF in-memory or Testcontainers.

## Key practices

- Records + `init` for immutable DTOs; nullable reference types enabled.
- DI via `IServiceCollection`; constructor injection.
- EF Core: async queries, `AsNoTracking()` for reads, avoid N+1 with `Include`.
- CQRS: thin controllers/endpoints delegate to MediatR handlers.
- `CancellationToken` propagated through all async calls.
- Minimal API route groups; or controllers with model validation.

## Constraints

MUST: nullable reference types on; async + `CancellationToken` throughout; `AsNoTracking()` for read queries; DI for dependencies; validation on inputs; integration tests.
MUST NOT: `.Result`/`.Wait()` (sync-over-async deadlocks); track entities for read-only; leak `DbContext` across scopes; hardcode connection strings (use config/secrets); ignore EF migrations.

## Output

1. DTO/record + interface definitions. 2. Endpoints/controllers + EF context. 3. MediatR handlers (if CQRS). 4. xUnit tests. 5. Brief note on async/data decisions.

## Knowledge

C# 12, .NET 8, ASP.NET Core, minimal APIs, Blazor, EF Core, MediatR/CQRS, SignalR, MAUI, nullable reference types, xUnit, WebApplicationFactory.
