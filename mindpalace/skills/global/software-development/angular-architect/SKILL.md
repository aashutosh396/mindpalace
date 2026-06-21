---
name: angular-architect
description: "Use when building Angular 17+ apps with standalone components or signals — advanced routing with lazy loading and guards, NgRx state, RxJS patterns, bundle perf, Angular tests. Triggers: Angular, Angular 17, standalone components, signals, RxJS, NgRx, Angular performance, Angular routing, Angular testing."
version: 1.0.0
license: MIT
tags: [angular, standalone-components, signals, rxjs, ngrx, routing, performance, typescript]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/angular-architect
derived_from: awesomeclaude
---

# Angular Architect

Angular 17+: standalone components, signals, NgRx, RxJS.

## When to use

Angular 17+ apps with standalone components/signals; advanced routing (lazy loading, guards); NgRx state; RxJS reactive patterns; bundle/performance tuning; enterprise app testing.

## Core workflow

1. **Analyze** — module/standalone structure, routing, state needs.
2. **Design** — standalone components, signals for local state, NgRx for shared.
3. **Implement** — typed components, services with DI, RxJS for async streams.
4. **Routing/perf** — lazy-loaded routes, guards, `OnPush` change detection.
5. **Test** — Jasmine/Karma or Jest + TestBed.

## Key practices

- Standalone components (no NgModules) for new code.
- Signals for synchronous reactive local state; RxJS for async event streams.
- `OnPush` change detection + immutable updates for performance.
- Lazy-load feature routes; route guards (`canActivate`/`canMatch`).
- NgRx (store/effects/selectors) for complex shared state; memoized selectors.
- Always unsubscribe (`takeUntilDestroyed`/async pipe) to avoid leaks.

## Constraints

MUST: standalone components; `OnPush` change detection; unsubscribe / use async pipe; lazy-loaded feature routes; memoized NgRx selectors; typed reactive forms; tests via TestBed.
MUST NOT: leak subscriptions; mutate NgRx state; default change detection on heavy trees; logic in templates; eager-load everything; nest subscriptions (use RxJS operators).

## Output

1. Standalone components + services. 2. Routing config (lazy + guards). 3. NgRx slices (if needed) / signals. 4. Tests. 5. Brief note on change-detection/state decisions.

## Knowledge

Angular 17+, standalone components, signals, RxJS, NgRx (store/effects/selectors), lazy loading, route guards, OnPush, typed reactive forms, dependency injection, TestBed.
