---
name: vue-expert
description: "Use when building Vue 3 apps with Composition API, Nuxt 3 SSR/SSG, Pinia stores, composables, Quasar/Capacitor mobile, PWA, or Vite tuning (TypeScript). Triggers: Vue 3, Composition API, Nuxt, Pinia, Vue composables, ref, reactive, Vue Router, Vite Vue, Quasar, Capacitor, PWA, service worker."
version: 1.0.0
license: MIT
tags: [vue, composition-api, nuxt, pinia, composables, vite, quasar, pwa]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/vue-expert
derived_from: awesomeclaude
---

# Vue Expert

Vue 3 Composition API, Nuxt 3, Pinia (TypeScript).

## When to use

Vue 3 apps with Composition API; reusable composables; Pinia state; Nuxt 3 SSR/SSG; Quasar/Capacitor hybrid mobile; PWA/service workers; Vite + TS tuning.

## Core workflow

1. **Analyze** — component structure, state needs, SSR vs SPA.
2. **Design** — composables for reusable logic; Pinia stores for shared state.
3. **Implement** — `<script setup>` Composition API; typed props/emits.
4. **SSR/build** — Nuxt 3 server routes; Vite config + code splitting.
5. **Test** — Vitest + Vue Test Utils.

## Key practices

- `<script setup lang="ts">`; `ref`/`reactive`/`computed`; typed `defineProps`/`defineEmits`.
- Extract reusable stateful logic into composables (`useX`).
- Pinia stores (setup syntax) for cross-component state.
- Nuxt 3: `server/` API routes, `useFetch`/`useAsyncData` for SSR-safe data.
- Vite: route-level code splitting, optimize chunks, source maps in dev.
- Quasar/Capacitor for hybrid mobile + PWA.

## Constraints

MUST: Composition API + `<script setup>`; typed props/emits; composables for reuse; Pinia for shared state; SSR-safe data fetching in Nuxt; Vitest coverage.
MUST NOT: mutate props; Options API for new code (per this skill's stack); share state via global mutable singletons; block SSR with client-only APIs; ignore reactivity caveats (destructuring reactive loses reactivity).

## Output

1. Components (`<script setup>`). 2. Composables + Pinia stores. 3. Nuxt server routes / Vite config (if relevant). 4. Vitest tests. 5. Brief note on reactivity/SSR decisions.

## Knowledge

Vue 3, Composition API, `<script setup>`, ref/reactive/computed, composables, Pinia, Vue Router, Nuxt 3, Vite, Quasar, Capacitor, PWA, Vitest, Vue Test Utils.
