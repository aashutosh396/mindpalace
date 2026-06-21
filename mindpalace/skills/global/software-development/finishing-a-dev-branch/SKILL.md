---
name: finishing-a-dev-branch
description: "Use when implementation is done and tests pass and you need to wrap up / finish / close out a feature branch — deciding whether to merge locally, push and open a PR, keep the branch, or discard the work, plus cleaning up git worktrees safely."
version: 1.0.0
license: MIT
tags: [git, branch, worktree, merge, pull-request, cleanup, workflow, finishing]
source: https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch
derived_from: awesomeclaude
prerequisites:
  commands: [git]
---

# Finishing a Dev Branch

Wrap up completed development work by verifying tests, detecting the workspace
state, presenting a fixed set of options, executing the chosen one, and cleaning
up safely.

**Core flow:** Verify tests -> Detect environment -> Present options -> Execute choice -> Clean up.

## When to use

The implementation is complete and you are ready to integrate it: "finish this
branch", "wrap up the feature", "merge or PR?", "close out this work". Do NOT
guess what the user wants — present the structured options below.

## Step 1: Verify tests

Run the project's suite (`npm test` / `cargo test` / `pytest` / `go test ./...`).
If anything fails, STOP. Show the failures and refuse to proceed — do not merge
broken code or open a failing PR.

## Step 2: Detect environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | 4 options | no worktree to clean |
| differ, named branch (worktree) | 4 options | provenance-based (Step 6) |
| differ, detached HEAD | 3 options (no local merge) | none — externally managed |

## Step 3: Determine base branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main — correct?"

## Step 4: Present options (verbatim, no extra explanation)

Normal repo / named worktree — exactly 4:
```
1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

Detached HEAD — exactly 3:
```
1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work
```

## Step 5: Execute

**Option 1 — Merge locally.** Get the main repo root and merge there first;
verify success BEFORE removing anything:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
<test command>   # verify tests on merged result
```
Then cleanup worktree (Step 6), then `git branch -d <feature-branch>`.

**Option 2 — Push + PR.** `git push -u origin <feature-branch>`.
Do NOT clean up the worktree — the user needs it to iterate on PR feedback.

**Option 3 — Keep as-is.** Report path; preserve branch and worktree.

**Option 4 — Discard.** Require a typed `discard` confirmation listing the
branch, commits, and worktree path. Only then:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
# cleanup worktree (Step 6), then force-delete:
git branch -D <feature-branch>
```

| Option | Merge | Push | Keep worktree | Delete branch |
|--------|-------|------|---------------|---------------|
| 1 Merge | yes | - | - | yes |
| 2 PR | - | yes | yes | - |
| 3 Keep | - | - | yes | - |
| 4 Discard | - | - | - | yes (force) |

## Step 6: Cleanup workspace (Options 1 and 4 only)

```bash
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```
- `GIT_DIR == GIT_COMMON`: normal repo, nothing to clean. Done.
- Worktree path under `.worktrees/` or `worktrees/`: this skill owns it —
  `cd` to main root, then `git worktree remove "$WORKTREE_PATH"` and
  `git worktree prune`.
- Otherwise: the host/harness owns the workspace — do NOT remove it. Use a
  workspace-exit tool if the platform provides one, else leave it in place.

## Gotchas / red flags

- Never proceed with failing tests, and re-verify tests on the merged result.
- Never delete work without a typed confirmation.
- Never force-push unless explicitly asked.
- Remove the worktree BEFORE deleting the branch — `git branch -d` fails while a
  worktree still references it.
- Never run `git worktree remove` from inside the worktree being removed — `cd`
  to the main repo root first.
- Only clean up worktrees you created (the `.worktrees/`/`worktrees/` provenance
  check); removing harness-owned worktrees causes phantom state.
