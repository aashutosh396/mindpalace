---
name: laravel-specialist
description: "Use when building Laravel 10+ apps — Eloquent models/relationships, Sanctum auth, Horizon queues, RESTful APIs with API resources, Livewire reactive UIs. Triggers: Laravel, Eloquent, PHP framework, Laravel API, Artisan, Blade, Laravel queues, Livewire, Laravel testing, Sanctum, Horizon."
version: 1.0.0
license: MIT
tags: [laravel, eloquent, sanctum, horizon, livewire, blade, artisan, php]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/laravel-specialist
derived_from: awesomeclaude
---

# Laravel Specialist

Laravel 10+: Eloquent, Sanctum, queues, Livewire.

## When to use

Eloquent models + relationships; Sanctum auth flows; Horizon queue workers; RESTful APIs with API resources; Livewire components; Eloquent query optimization; Pest/PHPUnit tests.

## Core workflow

1. **Analyze** — models, relationships, routes.
2. **Design** — migrations + Eloquent models with relationships, casts.
3. **Implement** — controllers, form requests, API resources.
4. **Auth / queues** — Sanctum tokens; queued jobs via Horizon.
5. **Test** — Pest/PHPUnit feature + unit tests.

## Key practices

- Eloquent: eager load (`with()`) to avoid N+1; `$fillable`/`$guarded`; casts for value objects.
- Form requests for validation; API resources to shape JSON responses.
- Sanctum for SPA/token auth; policies + gates for authorization.
- Queue slow work (mail, external APIs); monitor with Horizon; idempotent jobs.
- Livewire for reactive UI without a separate SPA.

## Constraints

MUST: eager-load relations (no N+1); form request validation; API resources for responses; policies/gates for authz; queue slow tasks; `.env` for secrets; Pest/PHPUnit tests.
MUST NOT: mass-assignment without `$fillable`/`$guarded`; raw unparameterized queries; business logic in Blade; secrets in code; block requests on slow external calls; skip migrations.

## Output

1. Migrations + Eloquent models. 2. Controllers + form requests + API resources. 3. Auth (Sanctum) / queued jobs. 4. Pest/PHPUnit tests. 5. Brief note on query/queue decisions.

## Knowledge

Laravel 10+, Eloquent, Sanctum, Horizon, Livewire, Blade, Artisan, queues/jobs, API resources, form requests, policies, Pest, PHPUnit.
