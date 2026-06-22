---
name: GitHub Contributor (open-source PR playbook)
description: Use whenever creating, editing, or pushing a PR to a third-party GitHub repo you don't maintain — discovery, CONTRIBUTING compliance, PR-size check, minimal-diff implementation, evidence-backed description, AI disclosure, conflict resolution, and maintainer/bot interaction.
tags: [github, pull-request, open-source, contributing, gh-cli, conventional-commits, rebase, ai-disclosure, code-review]
source: daymade/claude-code-skills
derived_from: github-contributor
---

Phase-based playbook for PRs maintainers actually merge. The most common mistake is doing the right thing at the wrong phase (a perfect description on a 10× too-large PR).

## Phase 0 — when to use
All true: contributing to a repo you don't maintain; touches code/tests/docs/build config; you want it merged. Not for: own repos, internal team PRs, hot-fixes a maintainer is waiting on, or trivial one-liners.

## Phase 1 — Pre-PR discovery
- **Read CONTRIBUTING.md as a hard contract**, not style advice. Watch for: AI-assisted clauses ("AI PRs without prior discussion may be closed", "explain every line", "one issue one PR") → you owe explicit disclosure + small PR; issue-first rules; per-language test commands (run exactly those).
- **Sanity-check PR size vs baseline:** `gh pr list --repo <o>/<r> --state merged --limit 10 --json additions,deletions,title`. If your PR is 5-10× the biggest recent merge → split.
- **Write a one-paragraph scope contract** to yourself (Goal / In scope 3-5 / Explicitly out of scope). Every edit: "is this in scope?" Scope creep is the #1 close-without-merge cause.

## Phase 2 — Implementation
- Branch off upstream `main`: `git fetch origin; git switch -c feat/name origin/main` (never your stale fork main).
- Smallest diff that solves the problem. No "while I'm here" refactors, no reformatting untouched lines, no renames unless that IS the fix.
- Conventional Commits (`feat|fix|docs|refactor|test|chore|ci|perf(scope): desc`), one logical change per commit. Review fixes via `git commit --fixup=<sha>` + autosquash before pushing.

## Phase 3 — Quality gates (produce evidence)
- Run the project's full lint+test locally (exact commands from CONTRIBUTING.md). Don't push red checks expecting CI to clarify.
- GUI/desktop apps: isolate the data dir first (`XXX_TEST_HOME`/`XXX_DATA_DIR` → `/tmp/app-e2e/`), run the real binary, trigger through the real surface, verify persisted state (SQLite/JSON), capture screenshots.
- **Self-audit:** list every "I tested/verified/ran" claim; for each, "what's my evidence?" If "I think so", you haven't done it. Write only what you can defend — a maintainer running your "tested" command and finding it broken is a permanent trust hit.

## Phase 4 — PR description
Skeleton: Summary (2 sentences) / What (commits or files + purpose) / Why (problem solved) / Test Plan (exact runnable commands; coverage matrix for non-trivial) / Backward Compatibility / Security (if auth/inputs/shared state) / Screenshots / Related Issue / Checklist (project template + real evidence) / AI-Assisted Disclosure.
- **Test coverage matrix** (>2 tests): table mapping each test → behavior it locks in.
- **Screenshots:** `gh` can't attach images. Prefer leaving `[SCREENSHOT_N_PLACEHOLDER]` markers for the user to drag images into the GitHub web UI (zero pollution); fallback orphan branch on fork via `raw.githubusercontent.com`.
- **AI disclosure** (if CONTRIBUTING asks or maintainer is skeptical): specific, not vague — "read every line; tested with <actual commands+results>; single-topic; AI tools used: Claude Code for drafting, final decisions mine".

## Phase 5 — Post-submission
- **Reply to each bot finding** (Codex/CodeRabbit/Claude bot) inline: `gh api repos/<o>/<r>/pulls/<pr>/comments -X POST -F in_reply_to=<id> -f body="Addressed in <sha>: <fn/test>. <one sentence>."` Even when the bot is wrong, reply — silence reads as "didn't notice".
- **Rebase:** `git fetch origin; git rebase origin/main`; resolve; `git push fork <branch> --force-with-lease` (never plain `--force` — lease aborts if a bot pushed, protecting review threads). No scope creep during rebase.
- **Filter counter-review findings** before responding (probability / cost / already-prevented-upstream). Filter ruthlessly; explain accept vs decline.

## Quality metrics target
Files: 1-5 (fixes), ≤~15 (features w/ tests). Production diff <200 lines if possible; rest tests/docs. Description 200-600 lines w/ evidence. First response to bot/maintainer <24h. CI passing on first push.
