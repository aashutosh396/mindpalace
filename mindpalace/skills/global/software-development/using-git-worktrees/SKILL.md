---
name: using-git-worktrees
description: "Use when starting isolated feature work, before running an implementation plan, or when you need a clean separate workspace — sets up a git worktree (or native worktree tool) so the current branch stays untouched. Triggers: git worktree, isolated workspace, worktree add, .worktrees, separate branch checkout, EnterWorktree, sandbox the work."
version: 1.0.0
license: MIT
tags: [git, worktree, isolation, branch, workspace, setup, baseline, harness]
source: https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees
derived_from: awesomeclaude
prerequisites:
  commands: [git]
---

# Using Git Worktrees

Ensure work happens in an isolated workspace so the current branch is never polluted.
Order of preference: detect existing isolation → use a native worktree tool → fall back
to `git worktree`. Never fight the harness.

## When to use

- Starting feature/bugfix work that should not touch the current checkout.
- Before executing an implementation plan that will make many file changes.
- Any time you want a clean, separate branch workspace with a verified baseline.

## Step 0: Detect existing isolation (always run first)

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` usually means you are already in a linked worktree → skip to Step 2.
- **Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside a submodule. Verify first:
  ```bash
  git rev-parse --show-superproject-working-tree 2>/dev/null
  ```
  If this prints a path, you are in a submodule, not a worktree → treat as a normal repo.
- Detached HEAD in an existing worktree: note that a branch must be created at finish time.
- `GIT_DIR == GIT_COMMON` (or submodule) → normal checkout. If the user has not already
  stated a worktree preference, ask consent before creating one. If declined, work in place
  and skip to Step 2.

## Step 1: Create the workspace

### 1a. Native worktree tool (preferred)
If a native mechanism exists (e.g. an `EnterWorktree`/`WorktreeCreate` tool, a `/worktree`
command, or a `--worktree` flag), use it and skip to Step 2. Native tools handle directory
placement, branch creation, and cleanup. Using `git worktree add` when a native tool exists
creates phantom state the harness cannot manage — this is the #1 mistake.

### 1b. Git worktree fallback (only if no native tool)

Directory priority (explicit user preference beats filesystem state):
1. A worktree dir declared in your instructions → use it.
2. Existing project-local dir: prefer `.worktrees/`, else `worktrees/` (`.worktrees` wins if both).
3. Otherwise default to `.worktrees/` at project root.

Safety — project-local dirs MUST be gitignored before creating the worktree:
```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```
If not ignored: add to `.gitignore`, commit that change, then proceed. (Prevents committing
worktree contents into the repo.)

Create:
```bash
path="$LOCATION/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** if `git worktree add` fails with a permission/sandbox denial, tell the
user the sandbox blocked it and work in the current directory instead.

## Step 2: Project setup

Auto-detect and install:
```bash
[ -f package.json ]     && npm install
[ -f Cargo.toml ]       && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ]   && poetry install
[ -f go.mod ]           && go mod download
```

## Step 3: Verify clean baseline

Run the project-appropriate test command (`npm test` / `cargo test` / `pytest` / `go test ./...`).
- Tests fail → report failures and ask whether to proceed or investigate (so new bugs are
  distinguishable from pre-existing ones).
- Tests pass → report ready:
  ```
  Worktree ready at <full-path>
  Tests passing (<N> tests, 0 failures)
  Ready to implement <feature-name>
  ```

## Quick reference

| Situation | Action |
|---|---|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo |
| Native worktree tool available | Use it (1a) |
| No native tool | Git fallback (1b) |
| `.worktrees/` and/or `worktrees/` exist | Use it; `.worktrees` wins; verify ignored |
| Neither exists | Check instructions, else default `.worktrees/` |
| Directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Sandbox fallback, work in place |
| Baseline tests fail | Report + ask |
| No manifest file | Skip dependency install |

## Gotchas / red flags

- Never create a worktree when Step 0 already detects isolation (avoids nested worktrees).
- Never use `git worktree add` when a native tool exists.
- Never skip the gitignore check for project-local dirs.
- Never skip baseline test verification, and never proceed past failing tests without asking.
