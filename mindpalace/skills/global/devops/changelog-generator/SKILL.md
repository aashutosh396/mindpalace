---
name: Changelog Generator
description: Use when cutting a release, generating CHANGELOG.md from git history, computing the next semantic version from commits, automating release notes in CI, or planning a hotfix/rollback.
tags: [changelog, release-notes, conventional-commits, semver, version-bump, hotfix, rollback, keep-a-changelog, commit-lint]
source: alirezarezvani/claude-skills
derived_from: changelog-generator
---

# Changelog Generator

Produce consistent, auditable release notes from Conventional Commits. Separates commit parsing, semantic-bump logic, and changelog rendering so releases automate without losing editorial control.

## Workflows
1. **Generate changelog** from a git tag range (`--from-tag`/`--to-tag`/`--next-version`, markdown or JSON), or from stdin/file commit input.
2. **Update CHANGELOG.md** in place (prepend new entry, never overwrite history).
3. **Compute next version** from commits when undecided — derive `recommended_version` + `bump_type`, feed into changelog gen. Pre-releases via `--prerelease alpha|beta|rc`.
4. **Lint commits before merge** (`--strict` returns non-zero on violations).

## Conventional Commit rules
Types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `security`, `deprecated`, `remove`. Breaking: `type(scope)!: summary` or `BREAKING CHANGE:` footer.
SemVer mapping: breaking → major · non-breaking `feat` → minor · all others → patch.

## Release governance flow
1. Lint commit history for the range. 2. Generate changelog draft. 3. Manually adjust wording for customer clarity. 4. Validate semver bump. 5. Tag release only after changelog is approved.

## Hotfix severity & SLAs
| Severity | Definition | SLA | Approval |
|---|---|---|---|
| P0 Critical | Outage, data loss, exploited vuln | ≤2h; bypasses normal gates | Eng Lead + On-call Mgr |
| P1 High | Major feature broken | ≤24h; expedited review | Eng Lead + PM |
| P2 Medium | Minor, limited impact | Next release | Standard PR review |
Hotfix branch comes from the last stable tag, contains the minimal fix only, gets its own patch-bump changelog entry.

## Rollback triggers (pre-commit thresholds)
Error rate >2x baseline within 30min · latency >50% increase · core functionality broken · security vuln being exploited · DB integrity compromised. Prefer feature-flag disable over code rollback; DB rollbacks only for non-destructive migrations (forward-only preferred).

## Output quality checks
Each bullet user-meaningful (not impl noise) · breaking changes include migration action · security fixes isolated in `Security` section · empty sections omitted · duplicate bullets removed.

## CI policy
Run commit-lint `--strict` on all PRs, block merge on invalid commits, auto-generate draft notes on tag push, require human approval before writing CHANGELOG.md on main.

## Failure handling
No valid conventional commits → fail early (don't generate empty notes). Invalid git range → surface the explicit range. Missing write target → create safe changelog header scaffolding.
