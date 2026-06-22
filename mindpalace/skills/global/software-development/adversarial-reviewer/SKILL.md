---
name: Adversarial Code Reviewer
description: Use when you want a genuinely critical code review before merging a PR, or when an AI review feels too agreeable — three hostile reviewer personas that each MUST find an issue, breaking the self-review monoculture.
tags: [code-review, adversarial-review, pr-review, security-review, maintainability, self-review-trap, severity-classification, owasp]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/adversarial-reviewer
---

# Adversarial Code Reviewer

Forces genuine perspective shifts through three hostile personas. Each MUST find at least one issue — no "LGTM" escapes. Breaks the self-review trap: an AI reviewing code it wrote shares the same mental model and blind spots as the author.

## Workflow
1. **Gather changes**: no args → `git diff` + `git diff --cached` (fall back to `git diff HEAD~1`); `--diff <ref>`; `--file <path>` reviews whole file. None found → "Nothing to review."
2. **Read full context**: full file (not just changed lines — bugs hide in interactions), identify change purpose, note project conventions.
3. **Run all three personas** sequentially. Each must produce a finding. Don't soften, don't hedge — either it's a problem or it isn't.
4. **Deduplicate + synthesize**: merge dupes, promote findings caught by 2+ personas one severity level, produce output.

## The Three Personas
**Saboteur** ("I'm trying to break this in production"): unvalidated input, inconsistent state, concurrent access without sync, swallowed exceptions, data-format assumptions, off-by-one/overflow/null deref, resource leaks. For each function ask: worst input? what if external call fails/times out/returns garbage? what if it runs twice/concurrently/never?

**New Hire** ("modify this in 6 months with zero context"): names that don't communicate intent, logic needing 3+ files to understand, magic numbers/strings, functions doing more than one thing, missing types, style inconsistency, tests of implementation not behavior, comments describing *what* not *why*. Read each function as if you've never seen the codebase.

**Security Auditor** ("this will be attacked"): injection (SQL/NoSQL/OS/LDAP), broken auth (hardcoded creds, missing checks, tokens in URLs/logs), data exposure (sensitive data in errors/logs, missing encryption), insecure defaults (debug on, permissive CORS, wildcards), missing access control (IDOR, role checks, priv-esc), dependency CVEs, secrets in code. Identify every trust boundary; check validation + sanitization + least privilege.

If a persona finds the code genuinely clean, it must name the most fragile assumption / likeliest confusion / closest security-relevant assumption.

## Severity & Verdict
CRITICAL (data loss/breach/outage → block) · WARNING (edge-case bugs/perf/confusion → fix or accept with justification) · NOTE (style/minor → discretion). Promotion: 2+ personas → up one level. Verdict: **BLOCK** (1+ critical) · **CONCERNS** (no criticals, 2+ warnings) · **CLEAN** (only notes).

## Breaking the Self-Review Trap
Read bottom-up (last function first). State each function's contract before reading the body — does it match? Assume every variable could be null and every external call will fail. Ask: "if I deleted this change, what would break?" — if nothing, it may be unnecessary.

## Anti-Patterns
"LGTM no issues" (you didn't look hard enough) · cosmetic-only findings while missing a null deref · pulling punches · restating the diff · ignoring test gaps (always a finding) · reviewing only changed lines.
