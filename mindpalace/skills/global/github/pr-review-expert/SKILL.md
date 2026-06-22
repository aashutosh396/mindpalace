---
name: PR Review Expert
description: Use when reviewing pull requests / merge requests, analyzing diffs, checking PRs for security issues, or assessing code-change quality — blast radius, security scan, coverage delta, breaking-change detection.
tags: [pr-review, code-review, github, gitlab, blast-radius, security-scan, breaking-changes, coverage-delta, diff, merge-request]
source: alirezarezvani/claude-skills
derived_from: pr-review-expert
---

# PR Review Expert

Structured, systematic review for GitHub PRs and GitLab MRs. Goes beyond style nits: blast-radius analysis, security scanning, breaking-change detection, test-coverage delta. Produces a reviewer-ready report with prioritized findings.

## Use when
PR touches shared libs/APIs/DB schema · PR is large (>200 lines) · onboarding new contributors · security-sensitive paths (auth/payments/PII) · post-incident proactive review.

## Workflow
1. **Fetch context** — `gh pr view --json title,body,labels,milestone,assignees`, `gh pr diff --name-only`, dump diff to file. (GitLab: `glab mr view/diff`.)
2. **Blast radius** — for each changed file: direct dependents (who imports it), service boundaries (cross-service in monorepo), shared contracts (types/interfaces/schemas). Severity: CRITICAL (shared lib, DB model, auth middleware, API contract), HIGH (service used by >3, shared config/env), MEDIUM (single-service internal), LOW (UI/test/docs).
3. **Security scan** the diff — SQL injection (raw interpolation), hardcoded secrets, AWS key patterns, JWT secrets, XSS (innerHTML/dangerouslySetInnerHTML), auth bypass markers, weak hashes (md5/sha1), eval/exec, prototype pollution, path traversal.
4. **Coverage delta** — count source vs test files changed; new function without tests → flag; deleted tests without deleted code → flag; coverage drop >5% → block; auth/payments → require 100%.
5. **Breaking changes** — removed/renamed REST routes, GraphQL/TS interface removals, destructive DB ops (DROP/ALTER NOT NULL/TRUNCATE), index removals, added/removed env vars.
6. **Performance** — N+1 (DB calls in loops), heavy new deps, unbounded loops, missing/sequential awaits, large in-memory allocations.

## Ticket linking
Extract ticket refs from PR body; verify Jira/Linear ticket exists. Feed credentials to curl via a stdin config (`-K -`) or `~/.netrc` (chmod 600) so tokens never appear in argv / process list / shell history.

## Output format
Header: blast radius · security findings · coverage delta · breaking changes. Then **MUST FIX (blocking)** with file:line + fix, **SHOULD FIX (non-blocking)**, **SUGGESTIONS**, **LOOKS GOOD** (specific praise). Label each comment: "nit:", "must:", "question:", "suggestion:". Batch all comments in one round.

## Pitfalls / best practices
Don't review style over substance (let the linter do style) · don't miss blast radius (a 5-line shared-util change can break 20 services) · always verify error-path coverage · NOT NULL additions need default/two-phase migration · check indirect secret exposure (logs/error messages). Read the linked ticket first, check CI status before reviewing, reproduce non-trivial auth/perf changes locally, request a split if a PR is too large to review properly.
