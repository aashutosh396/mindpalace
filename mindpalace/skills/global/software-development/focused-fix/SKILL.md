---
name: Focused Fix — Deep-Dive Feature Repair
description: Use when an entire feature or module needs systematic end-to-end repair ("make X work", "fix the Y feature", "Z module is broken") — a strict 5-phase scope→trace→diagnose→fix→verify protocol. Not for quick single-bug fixes.
tags: [debugging, feature-repair, dependency-tracing, root-cause, systematic, diagnose, regression, blast-radius, fix-protocol]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/focused-fix
---

# Focused Fix — Deep-Dive Feature Repair

For when an entire feature/module needs systematic repair — tracing every dependency, reading logs, checking tests, mapping the full graph. NOT for quick single-bug fixes.

## The Iron Law
**NO FIXES WITHOUT COMPLETING SCOPE → TRACE → DIAGNOSE FIRST.** If you haven't finished Phase 3, you cannot propose fixes.

## The 5 phases (strictly in order)
`SCOPE → TRACE → DIAGNOSE → FIX → VERIFY`. FIX loops back to DIAGNOSE if a fix breaks something; 3+ fixes creating new issues → STOP and question the architecture with the user.

### Phase 1: SCOPE — map the feature boundary
Ask which feature/folder if unclear. Read every file in the primary folder. Produce a manifest: primary path, entry points (imported elsewhere), internal files, total files/lines.

### Phase 2: TRACE — map all dependencies (inside AND outside)
**Inbound** (what the feature imports): trace each import to source, verify it exists and is exported, check signatures match. Also: env vars (grep `process.env`/`os.environ`), config files, DB models, API endpoints, third-party packages.
**Outbound** (what imports the feature): search the whole codebase for imports from this folder; verify each consumer uses entities that exist with the correct interface. Output a dependency map + required env vars + config files.

### Phase 3: DIAGNOSE — find every issue
Run ALL checks. **Code quality:** imports resolve, no circular deps, consistent types at boundaries, error handling on async, no TODO/FIXME signaling known issues. **Runtime:** env vars set, migrations current, endpoints return expected shapes, no hardcoded values. **Tests:** run all related tests, record every failure with full output, check coverage. **Logs/errors:** error tracking, `git log --oneline -20 -- <path>`, recent commits to dependencies. **Config:** valid config files, dev/prod parity, credentials valid.
**Root-cause confirmation:** for each critical issue, state "I think X is root cause because Y", trace flow backward to verify — don't trust surface symptoms. **Risk label** each: HIGH (public API / breaking contract / DB schema / auth / >3 callers / git hotspot), MED (internal w/ tests / shared util / runtime config), LOW (leaf / isolated / test-only). Output a diagnosis report grouped CRITICAL/WARNINGS + test pass/fail counts.

### Phase 4: FIX — repair systematically
Order: **dependencies → types → logic → tests → integration.** Fix one issue at a time; run the related test after each; HIGH before MED before LOW; never change code outside the feature folder without stating why; keep a running change log. **3-strike rule:** if 3+ fixes create NEW issues, STOP — this is an architectural problem, not a bug collection. Tell the user, don't attempt fix #4 without that discussion.

### Phase 5: VERIFY
Run all tests in the feature folder (every one must pass), all tests in files that import the feature, then the full suite (check regressions). For UI, describe manual verification. Summarize: files changed, total fixes, tests passing, regressions, consumers verified.

## Red flags (you're skipping phases)
"I can see the bug, just fix it" · "scoping is overkill" · "map deps later" · "user said fix X so only look at X" · "tests pass so I'm done" (did you run consumer tests?) · "one more fix should do it" (after 2+ cascades — escalate) · "skip the diagnosis report". All mean: return to the phase you should be in.
