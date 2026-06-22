---
name: QA Expert (Test Strategy + Autonomous Execution)
description: Use when establishing a QA process — writing test cases (AAA), tracking bugs with P0-P4 severity, computing quality-gate metrics, OWASP security testing, or enabling autonomous LLM-driven test execution.
tags: [qa, testing, test-cases, bug-tracking, owasp, security-testing, quality-gates, coverage, aaa-pattern, autonomous]
source: daymade/claude-code-skills
derived_from: qa-expert
---

# QA Expert

World-class QA process using Google Testing Standards + OWASP best practices.

## Initialize
```bash
python scripts/init_qa_project.py <project-name> [output-dir]
```
Creates `tests/docs/`, `tests/e2e/`, `tests/fixtures/`, tracking CSVs (`TEST-EXECUTION-TRACKING.csv`, `BUG-TRACKING-TEMPLATE.csv`), doc templates (`BASELINE-METRICS.md`, `WEEKLY-PROGRESS-REPORT.md`), and a master QA prompt.

## Test cases (AAA pattern)
Format `TC-[CATEGORY]-[NUMBER]` (e.g. TC-CLI-001, TC-SEC-007). Structure: Prerequisites (Arrange) → Test Steps (Act) → Expected Results (Assert). Assign priority P0-P4. Include edge cases.

## Execution — Ground Truth Principle
- **Test case docs are authoritative** for test steps. The tracking CSV holds execution status ONLY — never trust it for specs.
- Always read the test from the category doc, execute exactly, update tracking CSV **immediately after each test** (never batch), file a bug if it fails.
- **Autonomous mode**: paste the master prompt to an LLM — it auto-executes, auto-tracks, auto-files bugs, auto-resumes from last completed test, escalates P0.

## Bug severity
- **P0 Blocker** (24h): security vuln, core broken, data loss
- **P1 Critical**: major feature broken w/ workaround
- **P2 High**: minor/edge case
- **P3 Medium**: cosmetic
- **P4 Low**: doc typo
Required fields: Bug ID, Severity, numbered repro steps, environment.

## Metrics & quality gates
```bash
python scripts/calculate_metrics.py path/to/TEST-EXECUTION-TRACKING.csv
```
All gates must pass to release: Test Execution 100%, Pass Rate ≥80%, P0 = 0, P1 ≤5, Code Coverage ≥80%, Security 90% OWASP.

## Security (OWASP Top 10, target 90%)
A01 Broken Access Control, A02 Crypto Failures, A03 Injection, A04 Insecure Design, A05 Misconfig, A07 Auth Failures, plus data integrity/logging/SSRF. Each test = AAA with documented attack vector.

## Sizing
50 tests → 2 weeks, daily summary. 200 → 4 weeks, daily+weekly. 500+ → 8-10 weeks, +stakeholder reports.

## Success
Reproducible by any engineer, objectively-measured gates, fully-documented bugs, real-time CSV visibility, autonomous-capable, handoff-ready.
