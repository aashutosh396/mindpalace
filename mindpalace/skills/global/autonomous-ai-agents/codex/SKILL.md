---
name: codex
description: "Delegate coding tasks (features, refactors, PR reviews) to the OpenAI Codex CLI from bash; use when offloading coding work to the standalone codex agent."
license: MIT
platforms: [linux, macos, windows]
related_skills: [claude-code, opencode]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex), OpenAI's autonomous coding agent CLI, by running the `codex` command from bash. Codex is interactive, so launch it inside a tmux session when you need to monitor or feed it input from a non-interactive shell.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow (`codex login`)
- **Must run inside a git repository** — Codex refuses to run outside one
- Codex is an interactive terminal app; launch it inside tmux when you need to
  monitor/feed it from a non-interactive bash tool

A valid CLI OAuth session may live under `~/.codex/auth.json`; do not treat a
missing `OPENAI_API_KEY` alone as proof that Codex auth is missing.

## One-Shot Tasks

`codex exec` runs non-interactively and exits when done — safe to run directly:

```bash
cd ~/project && codex exec 'Add dark mode toggle to settings'
```

For scratch work (Codex needs a git repo):
```bash
cd "$(mktemp -d)" && git init && codex exec 'Build a snake game in Python'
```

## Background / Long Tasks (tmux)

For long or potentially-interactive runs, drive Codex through a tmux session:

```bash
# Start a tmux session and launch Codex in it
tmux new-session -d -s codex-work -x 140 -y 40
tmux send-keys -t codex-work 'cd ~/project && codex exec --full-auto "Refactor the auth module"' Enter

# Monitor progress
tmux capture-pane -t codex-work -p -S -50

# Send input if Codex asks a question
tmux send-keys -t codex-work 'yes' Enter

# Kill if needed
tmux kill-session -t codex-work
```

Alternatively, for a fully non-interactive run (`--full-auto`/`--yolo`), background it directly and tee output to a log:

```bash
cd ~/project && codex exec --full-auto 'Refactor the auth module' > /tmp/codex-refactor.log 2>&1 &
# then poll the log
tail -n 30 /tmp/codex-refactor.log
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```bash
REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git "$REVIEW" && cd "$REVIEW" && gh pr checkout 42 && codex review --base origin/main
```

## Parallel Issue Fixing with Worktrees

```bash
# Create worktrees
cd ~/project && git worktree add -b fix/issue-78 /tmp/issue-78 main
cd ~/project && git worktree add -b fix/issue-99 /tmp/issue-99 main

# Launch Codex in each (backgrounded, each logging to its own file)
( cd /tmp/issue-78 && codex --yolo exec 'Fix issue #78: <description>. Commit when done.' > /tmp/issue-78.log 2>&1 ) &
( cd /tmp/issue-99 && codex --yolo exec 'Fix issue #99: <description>. Commit when done.' > /tmp/issue-99.log 2>&1 ) &

# Monitor
jobs; tail -n 20 /tmp/issue-78.log /tmp/issue-99.log

# After completion, push and create PRs
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'

# Cleanup
cd ~/project && git worktree remove /tmp/issue-78
```

## Batch PR Reviews

```bash
# Fetch all PR refs
cd ~/project && git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Review multiple PRs in parallel (backgrounded with per-PR logs)
( cd ~/project && codex exec 'Review PR #86. git diff origin/main...origin/pr/86' > /tmp/pr86.log 2>&1 ) &
( cd ~/project && codex exec 'Review PR #87. git diff origin/main...origin/pr/87' > /tmp/pr87.log 2>&1 ) &

# Post results
cd ~/project && gh pr comment 86 --body "$(cat /tmp/pr86.log)"
```

## Rules

1. **Use tmux for interactive runs** — bare `codex` is a TUI and hangs a non-interactive shell; drive it via `tmux send-keys`/`capture-pane`, or stick to `codex exec` for non-interactive one-shots
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly (no tmux needed)
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background long tasks** — run with `&` (tee to a log) or in a tmux session, then poll the log/pane
6. **Don't interfere** — monitor the log/pane and be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work (separate workdirs)
