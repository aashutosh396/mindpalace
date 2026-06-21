---
name: javascript-pro
description: "Use when building vanilla JavaScript apps with modern ES2023+ features, Promise/async-await flows, ESM modules, Node.js APIs, Web Workers, or Fetch API, or reviewing .js/.mjs/.cjs files. Triggers: JavaScript, ES2023, async await, Node.js, vanilla JavaScript, Web Workers, Fetch API, browser API, module system."
version: 1.0.0
license: MIT
tags: [javascript, es2023, async-await, nodejs, esm, web-workers, fetch, jest]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/javascript-pro
derived_from: awesomeclaude
---

# JavaScript Pro

Modern vanilla JavaScript (ES2023+), browser and Node.js.

## When to use

Vanilla JS apps; async/await + Promise handling; ESM/CJS module systems; browser perf/memory tuning; Node.js backend; Web Workers, Service Workers, browser APIs.

## Core workflow

1. **Analyze** — package.json, module system, Node version, browser targets; `.js`/`.mjs`/`.cjs` conventions.
2. **Design** — modules, async flows, error handling.
3. **Implement** — ES2023+ patterns.
4. **Validate** — `eslint --fix`; check leaks (DevTools / `--inspect`); verify bundle size.
5. **Test** — Jest 85%+ coverage; no unhandled rejections.

## Key patterns

```js
// Async error handling — always try/catch + guard
async function fetchUser(id) {
  try {
    const r = await fetch(`/api/users/${id}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (err) { console.error("fetchUser failed:", err); return null; }
}

// Optional chaining + nullish coalescing
const city = user?.address?.city ?? "Unknown";

// ESM named exports
export const add = (a, b) => a + b;
```

## Constraints

MUST: ES2023+ only; `?.` and `??`; async/await for all async; ESM for new projects; try/catch in async; JSDoc on complex fns; functional style.
MUST NOT: `var` (use const/let); callback patterns over Promises; mix CJS+ESM in one module; ignore leaks/perf; sync I/O in Node; mutate params; block the browser main thread.

## Output

1. Module with clean exports. 2. Test file (good coverage). 3. JSDoc on public APIs. 4. Brief note on patterns.

## Knowledge

ES2023+, Promises, async/await, event loop, ESM/CJS, dynamic imports, Fetch, Web/Service Workers, IntersectionObserver, fs/promises, streams, EventEmitter, worker threads, Jest, ESLint.
