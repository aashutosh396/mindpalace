---
name: opencode
description: "Delegate coding tasks (features, refactors, PR reviews) to the OpenCode CLI from bash; use when offloading coding work to the open-source opencode agent."
license: MIT
platforms: [linux, macos, windows]
related_skills: [claude-code, codex]
---

# OpenCode CLI

Use [OpenCode](https://opencode.ai) as an autonomous coding worker driven from bash. OpenCode is a provider-agnostic, open-source AI coding agent with a TUI and a non-interactive `run` mode. Use `opencode run` for one-shot tasks (no TTY needed); drive the interactive TUI through tmux when you need multi-turn sessions.

## When to Use

- User explicitly asks to use OpenCode
- You want an external coding agent to implement/refactor/review code
- You need long-running coding sessions with progress checks
- You want parallel task execution in isolated workdirs/worktrees

## Prerequisites

- OpenCode installed: `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`
- Auth configured: `opencode auth login` or set provider env vars (OPENROUTER_API_KEY, etc.)
- Verify: `opencode auth list` should show at least one provider
- Git repository for code tasks (recommended)
- A TTY (run inside tmux) for the interactive TUI; `opencode run` needs no TTY

## Binary Resolution (Important)

Shell environments may resolve different OpenCode binaries. If behavior differs between shells, check:

```bash
which -a opencode
opencode --version
```

If needed, pin an explicit binary path:

```bash
cd ~/project && "$HOME/.opencode/bin/opencode" run '...'
```

## One-Shot Tasks

Use `opencode run` for bounded, non-interactive tasks:

```bash
cd ~/project && opencode run 'Add retry logic to API calls and update tests'
```

Attach context files with `-f`:

```bash
cd ~/project && opencode run 'Review this config for security issues' -f config.yaml -f .env.example
```

Show model thinking with `--thinking`:

```bash
cd ~/project && opencode run 'Debug why tests fail in CI' --thinking
```

Force a specific model:

```bash
cd ~/project && opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4
```

## Interactive Sessions (tmux)

For iterative work requiring multiple exchanges, drive the TUI through tmux:

```bash
# Start a tmux session and launch the OpenCode TUI in it
tmux new-session -d -s oc-work -x 140 -y 40
tmux send-keys -t oc-work 'cd ~/project && opencode' Enter
sleep 3

# Send a prompt (Enter may need to be pressed twice to submit)
tmux send-keys -t oc-work 'Implement OAuth refresh flow and add tests' Enter
sleep 0.3 && tmux send-keys -t oc-work Enter

# Monitor progress
tmux capture-pane -t oc-work -p -S -50

# Send follow-up input
tmux send-keys -t oc-work 'Now add error handling for token expiry' Enter && tmux send-keys -t oc-work Enter

# Exit cleanly — Ctrl+C
tmux send-keys -t oc-work C-c
# Or kill the whole session
tmux kill-session -t oc-work
```

**Important:** Do NOT use `/exit` — it is not a valid OpenCode command and will open an agent selector dialog instead. Use Ctrl+C (`tmux send-keys ... C-c`) or kill the tmux session to exit.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit OpenCode |

### Resuming Sessions

After exiting, OpenCode prints a session ID. Resume inside tmux with:

```bash
# Continue last session
tmux new-session -d -s oc-work -x 140 -y 40 && tmux send-keys -t oc-work 'cd ~/project && opencode -c' Enter
# Specific session
tmux new-session -d -s oc-work -x 140 -y 40 && tmux send-keys -t oc-work 'cd ~/project && opencode -s ses_abc123' Enter
```

## Common Flags

| Flag | Use |
|------|-----|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue the last OpenCode session |
| `--session <id>` / `-s` | Continue a specific session |
| `--agent <name>` | Choose OpenCode agent (build or plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output/events |
| `--file <path>` / `-f` | Attach file(s) to the message |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort (high, max, minimal) |
| `--title <name>` | Name the session |
| `--attach <url>` | Connect to a running opencode server |

## Procedure

1. Verify tool readiness:
   - `opencode --version`
   - `opencode auth list`
2. For bounded tasks, use `opencode run '...'` (no TTY needed) — run it directly or background with `&`.
3. For iterative tasks, start the `opencode` TUI inside a tmux session.
4. Monitor long tasks by tailing the log file (`&` runs) or `tmux capture-pane` (TUI).
5. If OpenCode asks for input, respond via `tmux send-keys`.
6. Exit with Ctrl+C (`tmux send-keys ... C-c`) or kill the tmux session.
7. Summarize file changes, test results, and next steps back to user.

## PR Review Workflow

OpenCode has a built-in PR command (interactive — run it in tmux):

```bash
tmux new-session -d -s oc-pr -x 140 -y 40 && tmux send-keys -t oc-pr 'cd ~/project && opencode pr 42' Enter
```

Or review non-interactively in a temporary clone for isolation:

```bash
REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git "$REVIEW" && cd "$REVIEW" \
  && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' \
     -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')
```

## Parallel Work Pattern

Use separate workdirs/worktrees to avoid collisions (background each `opencode run` with `&`):

```bash
( cd /tmp/issue-101 && opencode run 'Fix issue #101 and commit' > /tmp/issue-101.log 2>&1 ) &
( cd /tmp/issue-102 && opencode run 'Add parser regression tests and commit' > /tmp/issue-102.log 2>&1 ) &
jobs; tail -n 20 /tmp/issue-101.log /tmp/issue-102.log
```

## Session & Cost Management

List past sessions:

```bash
opencode session list
```

Check token usage and costs:

```bash
opencode stats
opencode stats --days 7 --models anthropic/claude-sonnet-4
```

## Pitfalls

- Interactive `opencode` (TUI) sessions need a TTY — run them inside tmux. The `opencode run` command does NOT need a TTY.
- `/exit` is NOT a valid command — it opens an agent selector. Use Ctrl+C to exit the TUI.
- PATH mismatch can select the wrong OpenCode binary/model config.
- If OpenCode appears stuck, inspect the log file / `tmux capture-pane` before killing.
- Avoid sharing one working directory across parallel OpenCode sessions.
- Enter may need to be pressed twice to submit in the TUI (once to finalize text, once to send).

## Verification

Smoke test:

```bash
opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'
```

Success criteria:
- Output includes `OPENCODE_SMOKE_OK`
- Command exits without provider/model errors
- For code tasks: expected files changed and tests pass

## Rules

1. Prefer `opencode run` for one-shot automation — it's simpler and doesn't need pty.
2. Use interactive background mode only when iteration is needed.
3. Always scope OpenCode sessions to a single repo/workdir.
4. For long tasks, provide progress updates from `process` logs.
5. Report concrete outcomes (files changed, tests, remaining risks).
6. Exit interactive sessions with Ctrl+C or kill, never `/exit`.
