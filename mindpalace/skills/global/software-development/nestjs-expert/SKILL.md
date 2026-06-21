---
name: nestjs-expert
description: "Use when building NestJS REST or GraphQL backends — modules, controllers, services, DTOs, guards, interceptors, pipes, JWT/Passport auth, TypeORM/Prisma. Invoke for .module.ts/.controller.ts/.service.ts files. Triggers: NestJS, Nest, Node.js backend, TypeScript backend, dependency injection, controller, service, module, guard, interceptor."
version: 1.0.0
license: MIT
tags: [nestjs, nodejs, typescript, dependency-injection, guards, typeorm, prisma, jwt]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/nestjs-expert
derived_from: awesomeclaude
---

# NestJS Expert

Enterprise NestJS: modular TypeScript backends.

## When to use

NestJS REST or GraphQL services; DI + modular architecture; JWT/Passport auth; TypeORM or Prisma; guards, interceptors, pipes, validation; Swagger docs; unit/E2E tests.

## Core workflow

1. **Analyze** — domain modules, boundaries, data layer.
2. **Design** — modules per bounded context; DTOs with class-validator.
3. **Implement** — controllers (thin) → services (logic) → repositories; DI throughout.
4. **Cross-cutting** — guards (authz), interceptors (logging/transform), pipes (validation).
5. **Test** — Jest unit tests + Supertest E2E.

## Key practices

- One module per feature; export only what other modules need.
- DTOs validated by `ValidationPipe` + class-validator decorators.
- Guards for auth (JWT via Passport strategy); `@UseGuards`.
- Interceptors for response shaping, logging, caching.
- TypeORM/Prisma repositories injected into services; never query in controllers.
- `@nestjs/swagger` decorators for OpenAPI.

## Constraints

MUST: thin controllers, logic in services; DI for all dependencies; global `ValidationPipe` + DTO validation; guards for protected routes; module boundaries respected; unit + E2E tests.
MUST NOT: business logic in controllers; direct DB access outside repositories/services; skip DTO validation; circular module dependencies; secrets in code (use ConfigModule/env).

## Output

1. Module + DTOs (class-validator). 2. Controller + service + repository. 3. Guards/interceptors/pipes. 4. Jest + Supertest tests. 5. Brief note on module design.

## Knowledge

NestJS, dependency injection, modules/controllers/providers, DTOs, class-validator, guards/interceptors/pipes, Passport/JWT, TypeORM, Prisma, @nestjs/swagger, Jest, Supertest.
