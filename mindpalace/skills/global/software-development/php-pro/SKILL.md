---
name: php-pro
description: "Use when building PHP 8.3+ apps with Laravel or Symfony — strict typing, PHPStan level 9, PSR standards, async (Swoole/ReactPHP), typed DTOs, DI, REST/GraphQL APIs. Triggers: PHP, Laravel, Symfony, Composer, PHPStan, PSR, PHP API, Eloquent, Doctrine, Psalm, Pest, PHPUnit."
version: 1.0.0
license: MIT
tags: [php, laravel, symfony, composer, phpstan, psr, eloquent, doctrine]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/php-pro
derived_from: awesomeclaude
---

# PHP Pro

Modern PHP 8.3+: strict types, Laravel/Symfony, PSR-compliant.

## When to use

PHP 8.3+ features; Laravel or Symfony apps; strict typing + PHPStan level 9; PSR standards; typed DTOs/value objects; DI containers; REST/GraphQL APIs; async (Swoole/ReactPHP).

## Core workflow

1. **Analyze** — composer.json, framework, PHP version, static-analysis level.
2. **Design** — typed DTOs, value objects, interfaces; readonly properties.
3. **Implement** — controllers/services with constructor DI.
4. **Data** — Eloquent or Doctrine; avoid N+1 (eager load / fetch joins).
5. **Validate** — `phpstan analyse` (level 9), PHP-CS-Fixer (PSR-12), Pest/PHPUnit.

## Key practices

- `declare(strict_types=1)` in every file; typed params + return types.
- Readonly + promoted constructor properties for immutable DTOs.
- PSR-12 formatting, PSR-4 autoloading, PSR-11 container.
- Laravel: form requests for validation, API resources, Eloquent eager loading.
- Symfony: typed services, attributes for routing, Doctrine repositories.
- Enums (PHP 8.1+) for fixed sets.

## Constraints

MUST: `strict_types=1` everywhere; full type coverage; PHPStan level 9 clean; PSR-12; validate all input; eager-load relations to kill N+1; Pest/PHPUnit tests.
MUST NOT: untyped arrays as DTOs; raw unparameterized SQL; secrets in code (use `.env`); ignore PHPStan errors; suppress with `@` operator; mix framework concerns into domain.

## Output

1. Typed DTOs/value objects. 2. Controllers/services with DI. 3. Eloquent/Doctrine data layer. 4. Pest/PHPUnit tests. 5. Brief note on type/query decisions.

## Knowledge

PHP 8.3, Laravel, Symfony, Composer, PHPStan/Psalm, PSR-4/11/12, Eloquent, Doctrine, enums, readonly properties, Swoole/ReactPHP, Pest, PHPUnit.
