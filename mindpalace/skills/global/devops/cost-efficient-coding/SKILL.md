---
name: cost-efficient-coding
description: "Build and debug large codebases with an agent at a fraction of the token/Max cost — without losing productivity. Scope, retrieval, model routing, caching, verification, debugging."
version: 1.0.0
author: mindpalace
license: MIT
platforms: [linux, macos]
tags: [cost, tokens, max, claude, coding, debugging, context, caching, subagents, scope, productivity]
related_skills: [build-automation, deploy-django-app]
---

# Cost-Efficient Coding

Use this whenever you write or debug code on a real/large codebase. The goal: **maximum
productivity per token.** This is a double win — a tight context is both cheaper AND produces
better answers ("context rot": as context fills, attention thins and quality drops). Bloated
context costs more and works worse.

Grounding facts (Anthropic + Microsoft Research): reads/tool-output are **~60–76% of tokens**
(not the model's thinking); agentic coding uses **~1000× more tokens than chat**, input-dominated;
**more tokens ≠ better accuracy** (same task varies up to 30×). So the cheapest, smartest token is
the one you never spend reading something you didn't need.

## The cost drivers (what to fight)
1. Re-reading files / dumping whole files (the #1 sink).
2. "Infinite exploration" — investigating the whole repo with no scope.
3. Re-deriving the codebase every session (no persistent notes).
4. Tool-output bloat (full test logs, stack traces, API JSON).
5. Retries from wrong-path work (a 10-step chain at 95%/step is ~60% reliable).
6. Using the expensive model for mechanical work.

## The playbook (ranked by impact)

### Tier 1 — biggest wins
- **Scope to named files/functions.** Not "fix the login bug" → "login fails after session
  timeout; check token refresh in `src/auth/`; write a failing test, then fix." Never read the
  whole repo to "understand" it.
- **Retrieve just-in-time.** Use `grep`/`glob` to locate, then RANGED reads (offset/limit) on the
  few files that matter; `head`/`tail` big files. A repo map / symbol search beats reading files.
- **Delegate read-heavy exploration to a subagent** (the Explore agent, read-only, cheap model).
  It can burn 10k tokens exploring and hand back a 1–2k summary — your main context never pays for
  the raw reads. Use for "how does X work / where is Y / trace this flow."
- **Protect the prompt cache.** A cache read costs ~10% of a fresh read. Keep the stable stuff
  (system prompt, instructions) first and identical across calls; put volatile content (the task,
  recent files) last. Don't reorder or inject changing values (timestamps) early — it busts the
  whole downstream cache.
- **Model routing.** Cheap model (Sonnet/Haiku) for execution, search, boilerplate, summarizing;
  reserve the expensive model (Opus) for hard reasoning, architecture, stubborn bugs. "Default
  cheap, escalate on purpose." In mindpalace: the owner says "think hard"/"use opus" to escalate.

### Tier 2 — habitual wins
- **Persistent project memory.** OPEN each task by reading `vault/projects/<slug>.md` + recent
  `git log` so you don't re-learn the codebase; CLOSE by appending "what changed / next / gotchas".
  This single handoff habit is the highest-leverage thing for multi-session work.
- **Lean CLAUDE.md.** It loads every turn — every line taxes every prompt and dilutes attention.
  Keep only what the agent can't guess (build/test commands, non-default conventions, gotchas).
  Occasional knowledge → a skill (loads on demand), not CLAUDE.md.
- **Cheap verification.** Give the loop a check it can run: build, lint, or a SINGLE relevant test
  (not the whole suite). TDD red→green is the cheapest correction signal; it lets the agent
  self-correct instead of round-tripping through you.
- **Plan only when it pays.** Non-trivial change → brief plan first (avoids an expensive wrong-path
  redo). If the diff fits in one sentence, skip the plan and just do it.
- **One focused task per run; reset between unrelated tasks.** A "kitchen-sink" session bloats
  context. After ~2 failed corrections, start fresh with a better prompt rather than piling on.

### Tier 3 — targeted
- **Debug by narrowing first.** Reproduce the failure as ONE failing unit test + the suspected
  file; hand the agent THAT, not a full stack trace + repo dump (that's the removable ~60%). Add a
  targeted log at the suspected boundary instead of ingesting everything.
- **CLI over chatty APIs/MCP.** `gh`, `psql`, `aws` give one compact line vs verbose JSON in context.
- **Cap tool output.** Pipe noisy commands (`| tail -50`, `| grep -E 'FAIL|ERROR'`); don't let a
  10k-line log into context.
- **`/compact` at task boundaries, not mid-task** (compaction itself re-reads, so do it between
  phases). Preserve the modified-file list + test commands when you compact.

## Done checklist
- [ ] Scoped to specific files; no whole-repo investigation.
- [ ] Used grep/glob + ranged reads (or an Explore subagent) instead of dumping files.
- [ ] Read the project note + git log at the start; appended a handoff note at the end.
- [ ] Verified with a single test / build, fixed root cause.
- [ ] Used the cheap model unless the problem genuinely needed deep reasoning.
- [ ] Kept tool output capped; didn't pull a giant log/trace into context.
