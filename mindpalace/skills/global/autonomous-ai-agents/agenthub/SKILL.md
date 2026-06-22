---
name: AgentHub — Multi-Agent Competition
description: Use when you want N parallel agents to compete on the same task in isolated git worktrees — code optimization, content variations, research exploration — then evaluate by metric or LLM judge and merge the winner.
tags: [multi-agent, parallel-agents, git-worktree, tournament, fan-out, optimization, llm-judge, coordinator, competition]
source: alirezarezvani/claude-skills
derived_from: engineering/agenthub
---

# AgentHub — Multi-Agent Competition

Spawn N parallel AI agents that compete on the same task, each in an isolated git worktree. The main session is the coordinator: it dispatches, monitors, evaluates, and merges the winner. Requires a git repo.

**Principle:** parallel competition, immutable history, best result wins. Agents never see each other's work; every approach is preserved in the git DAG; the coordinator evaluates objectively and merges only the winner.

**When:** "try multiple approaches", "have agents compete", "parallel optimization", "spawn N agents", "compare solutions", "fan-out/tournament", "generate content variations", "A/B test copy", "explore multiple strategies".

## Coordinator lifecycle: INIT → DISPATCH → MONITOR → EVALUATE → MERGE

1. **Init** — create a session: `.agenthub/sessions/{id}/config.yaml` (task, agent count, eval criteria), `state.json`, `.agenthub/board/` channels.
2. **Dispatch/spawn** — for each agent 1..N, post assignment to `board/dispatch/`, then launch ALL agents in a **single message** with multiple Agent tool calls, each with `isolation: "worktree"` (mandatory). Assign each a different strategy to maximize diversity. Agents work, commit, write a result summary to `board/results/agent-{i}-result.md`, and exit. They do not read or communicate with each other.
3. **Monitor** — `dag_analyzer.py --status` and the `board/progress/` channel.
4. **Evaluate** — *metric mode*: run the eval command in each worktree, parse the metric, rank by direction (lower/higher). *Judge mode*: read each `git diff base...agent-branch`, rank by correctness → simplicity (fewer lines) → quality. *Hybrid*: metric first, LLM-judge to break ties within 10%.
5. **Merge** — confirm with user (show diff summary first), then `git merge --no-ff` the winner into base. Tag losers `git tag hub/archive/{session}/agent-{i}` (archive, never delete commits), clean up worktrees, post a merge summary. Never force-push.

## Branch naming
`hub/{session-id}/agent-{N}/attempt-{M}` (session id = `YYYYMMDD-HHMMSS`). DAG is append-only: never rebase or force-push agent branches; delete only branch refs after archival.

## Agent templates (diverse iteration patterns)
- **optimizer** — edit → eval → keep/discard → repeat (latency, size, perf)
- **refactorer** — restructure → test → iterate until green (code quality)
- **test-writer** — write tests → measure coverage → repeat
- **bug-fixer** — reproduce → diagnose → fix → verify

## Message board (`.agenthub/board/`)
`dispatch/` (coordinator→agents), `progress/` (agents→coordinator), `results/` (both). Rules: append-only, never edit/delete, unique filenames `{seq:03d}-{author}-{timestamp}.md`, YAML frontmatter required.

## Proactive coordinator actions
All agents crashed → post failure summary, suggest retry with different constraints · no improvement over baseline → archive, suggest different approaches · orphan worktrees → run cleanup · stuck in `running` → check board, consider timeout.
