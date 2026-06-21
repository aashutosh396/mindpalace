---
name: typescript-pro
description: "Use when building TypeScript applications needing advanced generics, conditional or mapped types, discriminated unions, branded types, monorepo setup, or full-stack type safety with tRPC. Triggers: TypeScript, generics, type safety, conditional types, mapped types, tRPC, tsconfig, type guards, discriminated unions, satisfies."
version: 1.0.0
license: MIT
tags: [typescript, generics, type-safety, trpc, type-guards, discriminated-unions, tsconfig, satisfies]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/typescript-pro
derived_from: awesomeclaude
---

# TypeScript Pro

Advanced TypeScript 5.x type systems and end-to-end type safety.

## When to use

Advanced generics, conditional/mapped types, branded types, discriminated unions, monorepo project references, tRPC full-stack type safety, type guards.

## Core workflow

1. **Analyze** — tsconfig, type coverage, build perf.
2. **Design type-first APIs** — branded types, generics, utility types.
3. **Implement** — type guards, discriminated unions, conditional types; `tsc --noEmit` to catch errors.
4. **Optimize build** — project references, incremental compilation, tree shaking; re-run `tsc --noEmit`.
5. **Test types** — verify with `type-coverage`; all public APIs have explicit return types. Iterate until zero errors.

## Key patterns

```typescript
// Branded types — prevent id mix-ups at compile time
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, "UserId">;
const toUserId = (id: string): UserId => id as UserId;
```

```typescript
// Discriminated union + exhaustive guard
type RequestState =
  | { status: "loading" }
  | { status: "success"; data: string[] }
  | { status: "error"; error: Error };

function render(s: RequestState): string {
  switch (s.status) {
    case "loading": return "Loading…";
    case "success": return s.data.join(", ");
    case "error": return s.error.message;
    default: { const _x: never = s; throw new Error(_x); }
  }
}
```

```json
// tsconfig.json essentials
{ "compilerOptions": {
  "strict": true, "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true, "isolatedModules": true,
  "declaration": true, "incremental": true } }
```

## Constraints

MUST: strict mode + all flags; type-first API design; branded types for domain modeling; `satisfies` for validation; discriminated unions for state machines; generate declaration files for libraries; optimize for inference.
MUST NOT: `any` without justification; skip type coverage on public APIs; mix type-only/value imports; disable strict null checks; needless `as` assertions; use enums (prefer `const` objects `as const`).

## Output

1. Type definitions. 2. Implementation with type guards. 3. tsconfig if needed. 4. Brief note on type design.

## Knowledge

TypeScript 5.x, generics, conditional/mapped/template-literal types, discriminated unions, type guards, branded types, tRPC, project references, declaration files, const assertions, satisfies.
