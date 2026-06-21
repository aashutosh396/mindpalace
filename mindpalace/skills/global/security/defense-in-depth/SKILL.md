---
name: defense-in-depth
description: "Use when fixing a bug caused by invalid/empty/malformed data and a single validation check feels enough — add validation at EVERY layer (entry point, business logic, environment guard, debug logging) so the bug becomes structurally impossible, not just patched."
version: 1.0.0
license: MIT
tags: [validation, defense-in-depth, security, bug-fix, input-validation, guards, hardening, layered-validation]
source: https://github.com/obra/superpowers/tree/main/skills/defense-in-depth
derived_from: awesomeclaude
---

# Defense-in-Depth Validation

## What it does

When you fix a bug caused by invalid data, adding one validation check feels
sufficient — but that single check gets bypassed by other code paths,
refactoring, or mocks. This skill says: validate at EVERY layer the data passes
through, so the bug is structurally impossible instead of merely patched.

- Single validation = "we fixed the bug"
- Multiple layers = "we made the bug impossible"

## When to use

- You just fixed (or are about to fix) a bug rooted in invalid/empty/malformed input.
- A value reached somewhere dangerous (wrong dir, wrong env, null where required).
- You catch yourself adding ONE `if (!x) throw` and calling it done.
- Hardening code paths that mocks or tests can sneak bad data through.

## The four layers

Add a check at each layer the data crosses. Different layers catch different cases.

1. **Entry point validation** — reject obviously invalid input at the API
   boundary (empty, missing, wrong type, path doesn't exist / isn't a dir).
   Catches most bugs.
2. **Business logic validation** — ensure the data makes sense for THIS
   operation (e.g. `projectDir` required before initializing a workspace).
   Catches edge cases that bypass entry checks.
3. **Environment guards** — refuse dangerous operations in specific contexts.
   e.g. in tests, refuse `git init` outside a temp dir:
   ```ts
   if (process.env.NODE_ENV === 'test') {
     const normalized = normalize(resolve(directory));
     const tmp = normalize(resolve(tmpdir()));
     if (!normalized.startsWith(tmp)) {
       throw new Error(`Refusing git init outside temp dir during tests: ${directory}`);
     }
   }
   ```
4. **Debug instrumentation** — capture context for forensics when other layers
   fail. Log the value, `cwd`, and a stack trace right before the risky call:
   ```ts
   logger.debug('About to git init', { directory, cwd: process.cwd(), stack: new Error().stack });
   ```

## How to apply

1. **Trace the data flow** — where does the bad value originate, where is it used?
2. **Map every checkpoint** — list each point the data passes through.
3. **Add validation at each layer** — entry, business, environment, debug.
4. **Test each layer** — try to bypass layer 1 and verify layer 2 catches it;
   exercise the mock/edge-case path that motivated the fix.

## Worked example

Bug: empty `projectDir` caused `git init` to run in the source-code directory.

Data flow: test setup passes `''` → `Project.create(name, '')` →
`WorkspaceManager.createWorkspace('')` → `git init` runs in `process.cwd()`.

Layers added:
- L1: `Project.create()` validates not-empty / exists / is-directory / writable.
- L2: `WorkspaceManager` validates `projectDir` not empty.
- L3: `WorktreeManager` refuses `git init` outside tmpdir during tests.
- L4: stack-trace log before `git init`.

Result: all tests passed; bug impossible to reproduce. Each layer caught cases
the others missed — different code paths bypassed entry validation, mocks
bypassed business checks, platform edge cases needed the env guard, and the log
exposed structural misuse.

## Gotcha

Don't stop at one validation point. The temptation is to add a single check and
move on — but that's the failure mode this skill exists to prevent. All layers
are necessary; each catches what the others let through.
