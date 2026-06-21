---
name: verification-before-completion
description: "Use right before claiming any work is complete, fixed, passing, or done — and before committing or opening a PR. Run the actual verification command fresh in this turn, read the full output and exit code, and only then make the claim. Triggers: 'is it done?', about to say tests pass / build succeeds / bug fixed, before commit/push/PR, trusting an agent's success report, any wording implying success."
version: 1.0.0
license: MIT
tags: [verification, testing, quality-gate, honesty, completion, evidence, build, regression, ci]
source: https://github.com/obra/superpowers/tree/main/skills/verification-before-completion
derived_from: awesomeclaude
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always. Violating the letter of this rule is violating the spirit of this rule.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim
Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once" / tired and wanting work over
- ANY wording implying success without having run verification

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:** [Run test command] [See: 34/34 pass] "All tests pass" — not "Should pass now".

**Regression tests (TDD Red-Green):** Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass) — not "I've written a regression test" without the red-green cycle.

**Build:** [Run build] [See: exit 0] "Build passes" — the linter doesn't check compilation.

**Requirements:** Re-read plan → create checklist → verify each → report gaps or completion — not "Tests pass, phase complete".

**Agent delegation:** Agent reports success → check VCS diff → verify changes → report actual state — don't trust the report alone.

## When To Apply

ALWAYS before: any variation of success/completion claims, any expression of satisfaction, any positive statement about work state, committing, PR creation, task completion, moving to the next task, or delegating to agents. The rule applies to exact phrases, paraphrases, synonyms, implications of success — any communication suggesting completion or correctness.

## The Bottom Line

No shortcuts for verification. Run the command. Read the output. THEN claim the result. This is non-negotiable.
