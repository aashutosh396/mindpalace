---
name: debugging-wizard
description: "Use when investigating errors, analyzing stack traces, finding root causes of unexpected behavior, troubleshooting crashes, or doing log analysis. Applies systematic hypothesis-driven debugging to isolate and fix bugs. Triggers: debug, error, bug, exception, traceback, stack trace, troubleshoot, not working, crash, fix issue."
version: 1.0.0
license: MIT
tags: [debugging, error, stack-trace, root-cause, troubleshoot, git-bisect, pdb, regression]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/debugging-wizard
derived_from: awesomeclaude
---

# Debugging Wizard

Systematic methodology to isolate and resolve issues in any codebase.

## When to use

Investigating errors, analyzing stack traces, finding root causes, troubleshooting crashes, or analyzing logs.

## Core workflow

1. **Reproduce** — Establish consistent reproduction steps.
2. **Isolate** — Narrow to the smallest failing case.
3. **Hypothesize and test** — Form testable theories, verify/disprove one at a time.
4. **Fix** — Implement and verify the solution.
5. **Prevent** — Add regression tests/safeguards.

## Constraints

MUST: reproduce first; gather complete errors + stack traces; test one hypothesis at a time; document findings; add regression tests after fixing; remove all debug code before committing.
MUST NOT: guess without testing; change many things at once; skip reproduction; assume the cause; debug in production without safeguards; leave console.log/debugger statements behind.

## Common debugging commands

```bash
# Python (pdb)
python -m pdb script.py    # b 42 / n / s / p var / bt

# Node.js
node --inspect-brk script.js   # attach chrome://inspect, step through Sources

# Git bisect (regression hunting)
git bisect start
git bisect bad                 # current is broken
git bisect good v1.2.0         # last known good
# test each midpoint -> git bisect good|bad ; repeat ; git bisect reset

# Go (delve)
dlv debug ./cmd/server         # break main.go:55 / continue / print myVar
```

## Output template

1. **Root cause** — what specifically caused it
2. **Evidence** — stack trace, logs, or test that proves it
3. **Fix** — the code change that resolves it
4. **Prevention** — test/safeguard against recurrence
