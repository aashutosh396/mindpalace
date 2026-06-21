---
name: react-expert
description: "Use when building React 18+/19 apps in .jsx/.tsx, Next.js App Router projects, or CRA setups — components, custom hooks, Server Components, Suspense, state management, perf. Triggers: React, JSX, hooks, useState, useEffect, useContext, Server Components, React 19, Suspense, TanStack Query, Redux, Zustand, component."
version: 1.0.0
license: MIT
tags: [react, jsx, hooks, server-components, suspense, zustand, tanstack-query, frontend]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/react-expert
derived_from: awesomeclaude
---

# React Expert

React 18+/19: components, hooks, Server Components, performance.

## When to use

Building/refactoring React components (.jsx/.tsx); custom hooks; debugging rendering; migrating class → functional; state management; Server Components, Suspense, `useActionState`; perf optimization.

## Core workflow

1. **Analyze** — component tree, state ownership, render triggers.
2. **Design** — composition, custom hooks for reuse, server vs client boundary.
3. **Implement** — functional components + hooks; lift state appropriately.
4. **Optimize** — `memo`, `useMemo`, `useCallback` only where measured; stable keys.
5. **Test** — React Testing Library, user-centric assertions.

## Key practices

- Functional components + hooks only; rules of hooks (top level, no conditionals).
- Custom hooks (`useX`) to extract reusable stateful logic.
- Server Components for data fetching; `"use client"` only where interactivity needed.
- State libs: Zustand for client state, TanStack Query for server state.
- Effects only for true external synchronization; derive don't store.
- Stable, unique keys in lists (never index for dynamic lists).

## Constraints

MUST: follow rules of hooks; lift state to lowest common ancestor; stable list keys; memoize only proven hot paths; clean up effects; user-centric tests.
MUST NOT: derive state into other state (compute during render); index keys on reorderable lists; overuse `useEffect`; prop-drill deeply (use context/store); mutate state directly.

## Output

1. Component(s) + custom hooks. 2. State management wiring. 3. RTL tests. 4. Brief note on render/perf decisions.

## Knowledge

React 18/19, JSX, hooks, Server Components, Suspense, useActionState, Context, Zustand, Redux Toolkit, TanStack Query, React Testing Library, memoization.
