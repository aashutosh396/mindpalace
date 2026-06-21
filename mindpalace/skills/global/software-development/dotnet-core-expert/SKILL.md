---
name: dotnet-core-expert
description: "Use when building .NET 8 apps with minimal APIs, clean architecture, or cloud-native microservices. Invoke for Entity Framework Core, CQRS with MediatR, JWT auth, AOT compilation. Triggers: .NET Core, .NET 8, ASP.NET Core, C# 12, minimal API, Entity Framework Core, microservices .NET, CQRS, MediatR."
version: 1.0.0
license: MIT
tags: [dotnet, dotnet8, aspnet-core, minimal-api, ef-core, cqrs, mediatr, microservices]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/dotnet-core-expert
derived_from: awesomeclaude
---

# .NET Core Expert

.NET 8: minimal APIs, clean architecture, cloud-native microservices.

## When to use

.NET 8 minimal APIs; clean architecture; cloud-native microservices; EF Core; CQRS with MediatR; JWT auth; AOT compilation.

## Core workflow

1. **Analyze** — solution layout, layers (domain/application/infrastructure/api).
2. **Design** — domain entities, records for DTOs, CQRS commands/queries.
3. **Implement** — minimal API route groups → MediatR handlers → EF Core.
4. **Secure** — JWT bearer auth, authorization policies.
5. **Test** — xUnit + `WebApplicationFactory`; Testcontainers for EF.

## Key practices

- Clean architecture: domain has no framework deps; dependencies point inward.
- CQRS: minimal API endpoints dispatch MediatR commands/queries; thin handlers.
- EF Core: async, `AsNoTracking()` for reads, `Include` to avoid N+1, migrations.
- `CancellationToken` threaded through all async paths.
- Nullable reference types on; records + `init` for immutable DTOs.
- AOT-friendly code where startup/size matters (source generators over reflection).

## Constraints

MUST: clean-architecture dependency direction; CQRS via MediatR; async + `CancellationToken`; `AsNoTracking()` reads; EF migrations; nullable refs on; integration tests.
MUST NOT: `.Result`/`.Wait()` (deadlocks); domain depends on infrastructure; track read-only entities; secrets in source (use config/secrets); reflection-heavy code in AOT paths.

## Output

1. Domain + DTO records. 2. Minimal API endpoints + MediatR handlers. 3. EF Core context + migrations. 4. xUnit tests. 5. Brief note on architecture decisions.

## Knowledge

.NET 8, C# 12, ASP.NET Core minimal APIs, clean architecture, EF Core, MediatR/CQRS, JWT, Native AOT, nullable reference types, xUnit, WebApplicationFactory, Testcontainers.
