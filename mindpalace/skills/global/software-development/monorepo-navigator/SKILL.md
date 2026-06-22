---
name: Monorepo Navigator
description: Use when setting up a monorepo, optimizing CI for a large workspace, debugging cross-package dependency issues, or consolidating multiple repos — covers Turborepo, Nx, pnpm workspaces, Lerna, Changesets.
tags: [monorepo, turborepo, nx, pnpm, lerna, changesets, affected, remote-cache, dependency-graph, workspace]
source: alirezarezvani/claude-skills
derived_from: monorepo-navigator
---

# Monorepo Navigator

Navigate, manage, and optimize monorepos: cross-package impact analysis, selective builds/tests on affected packages, remote caching, dependency-graph visualization, and structured multi-repo → monorepo migrations.

## Use vs skip
**Use** when multiple packages share code, builds are slow because everything rebuilds, you're consolidating repos, or you need coordinated npm publishing. **Skip** for single-app projects, fully isolated team boundaries, or minimal shared code.

## Tool selection
| Tool | Best for | Key feature |
|---|---|---|
| Turborepo | JS/TS, simple pipeline | Best remote caching, minimal config |
| Nx | Large enterprises | Project graph, codegen, affected commands |
| pnpm workspaces | Disk efficiency | `workspace:*` local refs |
| Lerna | npm publishing | Batch publishing |
| Changesets | Modern versioning (preferred over Lerna) | Changelog gen, pre-release channels |

Most modern setups: **pnpm workspaces + Turborepo + Changesets**.

## Capabilities
- Cross-package impact: which apps break when a shared package changes.
- Selective commands: tests/builds for affected packages only.
- Dependency graph as Mermaid.
- Build optimization: remote caching, incremental builds, parallel execution.
- Migration: multi-repo → monorepo with zero history loss.
- Workspace-aware CLAUDE.md with per-package rules.

## Common pitfalls → fixes
- `turbo run build` without `--filter` on every PR → use `--filter=...[origin/main]` in CI.
- `workspace:*` publish failures → `pnpm changeset publish` replaces with real versions.
- Unrelated change rebuilds everything → tune `inputs` in turbo.json to exclude docs/config from cache keys.
- Shared tsconfig breaks one package → use `extends` properly; each package overrides `rootDir`/`outDir`.
- Lost git history on migration → `git filter-repo --to-subdirectory-filter` before merging; never move files manually.
- Remote cache not working in CI → check `TURBO_TOKEN`/`TURBO_TEAM`; verify with `--summarize`.
- Generic CLAUDE.md → add explicit "when working on X, only touch files in apps/X" per package.

## Best practices
1. Root CLAUDE.md defines the map (every package + dependency rules). 2. Per-package CLAUDE.md defines what's allowed/forbidden + test commands. 3. Always scope with `--filter`. 4. Remote cache is not optional. 5. Changesets over manual versioning. 6. Shared configs in root, extended in packages. 7. Run affected check + communicate blast radius before merging shared-package changes. 8. Keep `packages/types` pure TypeScript (no runtime code/deps).
