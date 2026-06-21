---
name: vue-expert-js
description: "Use when building Vue 3 apps with JavaScript only (no TypeScript) — components, vanilla JS composables, Vite, routing, state, JSDoc-typed code. Triggers: Vue JavaScript, Vue without TypeScript, Vue JSDoc, Vue JS only, Vue vanilla JavaScript, .mjs Vue, Vue no TS, migrating Vue 2 Options to Composition API in JS."
version: 1.0.0
license: MIT
tags: [vue, javascript, composition-api, jsdoc, vite, composables, pinia, no-typescript]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/vue-expert-js
derived_from: awesomeclaude
---

# Vue Expert (JavaScript)

Vue 3 with JavaScript only — JSDoc-typed, no TypeScript compiler.

## When to use

Vue 3 apps in plain JS (no TS); JSDoc-based type hints; migrating Vue 2 Options API → Composition API in JS; teams preferring vanilla JS / `.mjs`; quick prototypes without TS setup.

## Core workflow

1. **Analyze** — existing JS/Vue setup, module format, build tooling.
2. **Design** — composables for reuse; JSDoc `@typedef` for shapes.
3. **Implement** — `<script setup>` Composition API in JS; JSDoc on props and functions.
4. **State/routing** — Pinia stores, Vue Router; Vite config.
5. **Test** — Vitest + Vue Test Utils.

## Key practices

- JSDoc for type coverage: `@typedef`, `@param`, `@returns`, `@type` — get type hints without a TS compiler.
- `<script setup>` Composition API; `defineProps` with JSDoc-documented shapes.
- Composables (`useX`) return JSDoc-typed objects.
- Vite project config; `.mjs` ESM modules.
- Pinia stores in setup syntax.

## Constraints

MUST: JSDoc annotations (`@typedef`/`@param`/`@returns`) for type coverage; Composition API + `<script setup>`; composables for reuse; ESM modules; Vitest tests.
MUST NOT: introduce TypeScript (this skill is JS-only by design); mutate props; global mutable state singletons; skip JSDoc on public composables/functions; destructure reactive objects (loses reactivity).

## Output

1. JS components (`<script setup>`) with JSDoc. 2. JSDoc-typed composables + Pinia stores. 3. Vite/router config. 4. Vitest tests. 5. Brief note on JSDoc typing choices.

## Knowledge

Vue 3, Composition API (JS), `<script setup>`, JSDoc (@typedef/@param/@returns), composables, Pinia, Vue Router, Vite, ESM/.mjs, Vitest, Vue Test Utils.
