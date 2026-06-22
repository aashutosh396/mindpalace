---
name: Git Worktree Manager
description: Use when running multiple feature branches at once, isolating experimental work, or coordinating multi-agent development on one repo — sets up isolated Git worktrees with their own ports, env, and clean teardown.
tags: [git, worktree, parallel, branch, multi-agent, ports, isolation, docker-compose, cleanup]
source: alirezarezvani/claude-skills
derived_from: git-worktree-manager
---

# Git Worktree Manager

Run parallel feature work safely with Git worktrees. Each worktree behaves like an independent local app: own branch, own ports, own env, with safe cleanup. One branch per worktree, one agent per worktree.

## When to create a worktree (decision matrix)
- Need isolated deps + server ports → new worktree
- Quick local diff review only → stay on current tree
- Hotfix while feature branch is dirty → dedicated hotfix worktree
- Ephemeral bug-repro branch → temp worktree, clean up same day

## Create a fully-prepared worktree
1. Pick branch name + worktree name (deterministic: `wt-<topic>` or `wt-<taskid>-<topic>`).
2. Create worktree from new/existing branch (create branch if missing) OUTSIDE the main repo dir.
3. Auto-allocate non-conflicting ports; persist to `.worktree-ports.json` in the worktree.
4. Copy `.env*` from main repo into the worktree.
5. Optionally install deps (detect lockfile).
6. Start app on the allocated ports.

## Port allocation strategy
Default: `base + (index * stride)` with collision checks. App 3000, Postgres 5432, Redis 6379, stride 10. Persist the map to a file — never keep it only in memory/terminal notes. Per-worktree Docker Compose: use override files mapped from the allocated port map.

## Parallel session convention
- Main repo: integration branch (main/develop) on default port
- Worktree A: feature branch + offset ports
- Worktree B: hotfix branch + next offset

## Cleanup with safety checks
1. Scan all worktrees + stale age.
2. Inspect dirty trees and branch merge status.
3. Remove only merged + clean worktrees. Never force-remove a dirty worktree unless changes are intentionally discarded.

## Validation checklist (before claiming done)
1. `git worktree list` shows expected path + branch.
2. `.worktree-ports.json` exists with unique ports.
3. `.env` files copied (if present in source).
4. Dependency install exits 0 (if enabled).
5. App boots on the allocated app port; DB/cache target isolated ports.
6. Cleanup scan reports no unintended stale dirty trees.

## Common pitfalls
1. Creating worktrees inside the main repo dir.
2. Reusing `localhost:3000` across all branches.
3. Sharing one DB URL across isolated branches.
4. Removing a worktree with uncommitted changes.
5. Forgetting to prune metadata after branch deletion.
6. Assuming merged status without checking against the target branch.

## Failure recovery
- `git worktree add` fails on existing path → inspect, do not overwrite.
- Dep install fails → keep worktree, mark status, recover manually.
- Env copy fails → continue with warning + explicit missing-file list.
- Port collides with external service → rerun with adjusted base ports.
