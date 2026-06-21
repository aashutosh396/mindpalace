---
name: debug-skill
description: "Use when a program crashes, throws unexpected exceptions, produces wrong output, hangs, or print/log debugging isn't enough — set breakpoints, step through code line by line, inspect live variables, evaluate expressions, and walk the call stack with the `dap` interactive debugger (Python, Go, Node/TS, Rust, C/C++)."
version: 1.0.0
license: MIT
tags: [debugging, breakpoints, debugger, dap, step-through, call-stack, python, go, nodejs, rust]
source: https://github.com/AlmogBaku/debug-skill
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [dap]
---

# Interactive Debugger (dap)

Debug source code the way a human developer does instead of guessing or adding print
statements. Pause a running program, read live variable values and the call stack at that
exact moment, step forward line by line or jump to the next breakpoint, and evaluate
arbitrary expressions against the live process — without restarting.

## When to use

- A program crashes or raises an unexpected exception
- Output is wrong and you need to see actual values vs. expected
- You must understand how execution reached a particular state
- A process hangs or is stuck (attach and pause it)
- Print-statement debugging isn't revealing the cause fast enough

## Setup

Uses `dap`, a stateless CLI wrapping the Debug Adapter Protocol. A background daemon holds
the session; each CLI call sends one command and returns full context. The daemon starts on
`dap debug` and shuts down on `dap stop` or after ~10 min idle.

Check it's installed: `command -v dap`. If missing, ask/notify the user, then install:
- macOS Homebrew: `brew install AlmogBaku/tap/dap`
- One-liner installer: `bash <(curl -fsSL https://raw.githubusercontent.com/AlmogBaku/debug-skill/master/skills/debugging-code/scripts/install-dap.sh)`
- From source: `go install github.com/AlmogBaku/debug-skill/cmd/dap@latest`

Languages auto-detected from file extension: Python (debugpy), Go (dlv), Node/TS (js-debug),
Rust/C/C++ (lldb-dap). Override with `--backend <name>`. All flags: `dap --help` or `dap <cmd> --help`.

## Starting a session

`dap debug <file>` launches the program under the debugger. Pick a strategy:

- Have a hypothesis: `dap debug script.py --break script.py:42`
- Conditional break (always quote): `dap debug script.py --break "script.py:42:x > 5"`
- Multi-file: `--break src/api/routes.py:55 --break src/models/user.py:30`
- No hypothesis, small program: `dap debug script.py --stop-on-entry` (noisy for large projects)
- Exception, location unknown: `dap debug script.py --break-on-exception raised` (Python) / `all` (Go/JS)
- Remote process: `dap debug --attach host:port --backend <name>`
- Already-running process: `dap debug --pid <PID> --backend <name>`
  - macOS + Go gotcha: `dlv --pid` requires SIP disabled. Prefer launching under the debugger or attaching remotely.

Concurrent agents: isolate with `--session <name>` (e.g. `${CLAUDE_SESSION_ID}`). Each session
has its own daemon/socket; `dap stop --session <name>` stops only that one.

## Debugging mindset

- Reach for the debugger when reading source can't validate the root cause — observe what *does* happen.
- Two strikes, rethink: if two hypotheses fail at the same spot, your mental model is wrong — form a *different* theory.
- Escalate gradually: `dap eval` for quick checks → conditional breakpoints to cut noise → full breakpoints + stepping last.
- Mimic the user journey: if `compute()` is never called, the bug is in the caller, not `compute()`.
- When you want to print something, set a breakpoint instead.

## Know your state

Every execution command returns: current location, source, locals, call stack, output. At each stop ask:
do locals have expected values? Is the call stack the path I expected? Does output reveal anything?

Trace causation up the stack: if a value is wrong at frame 0, check `dap eval "<expr>" --frame 1`,
then `--frame 2`, etc., until you find the frame where it first went wrong — that's the origin.

If the program exits before the breakpoint, move breakpoints earlier or use `--stop-on-entry`.

## Breakpoints

Break where the problem *begins*, not where it *manifests*. Exception at line 80 → root cause is
usually upstream. Uncertain? Bisect: `--break f:20 --break f:60`, halve the search space each time.

Good spots: data/format/module boundaries, the line that mutates the corrupted value, the condition
that chose the wrong branch. Antipatterns: don't break inside library code (break at the call site);
don't use unconditional breaks in tight loops (use conditions).

Mid-session management:
```bash
dap continue --break app.py:50          # add deeper, then continue
dap continue --remove-break app.py:20   # drop one you're done with
dap break add app.py:42 app.py:60       # add multiple
dap break list                          # see what's set
dap break clear                         # start fresh
```

Conditional breakpoints (quote `"file:line:condition"`) — for loops, hot paths, specific inputs,
and runtime-assertion "invariant" breaks:
```bash
dap debug app.py --break "app.py:42:i == 100"
dap debug app.py --break "bank.py:68:balance < 0"     # catch the overdraft the moment it happens
```

## Navigating execution

If stepping more than 3 times in a row, set a breakpoint instead.
```bash
dap step                    # step over
dap step in                 # suspect what's inside this call
dap step out                # wrong place, return to caller
dap continue                # next breakpoint
dap continue --to file:line # disposable breakpoint, stops once
dap context                 # re-inspect without stepping
dap output                  # drain buffered stdout/stderr
dap inspect <var> --depth N # expand nested objects
dap pause                   # interrupt a hanging program
dap restart                 # re-run, same args + breakpoints
dap threads / dap thread <id>
```

Probe live state without stepping:
```bash
dap eval "len(items)"
dap eval "expected == actual"
dap eval "self.config" --frame 1   # caller frame
```
Avoid eval expressions that call methods with side effects — they mutate state and corrupt the session.

## Verify your fix

While paused at the bug, test the fix expression with `eval` against live state. If it works in eval,
it'll work in code. Then edit and `dap restart` to confirm end-to-end at the same breakpoint where you
found the bug — don't trust a fix until you've observed correct behavior.

## Cleanup

Sessions auto-terminate on program exit or idle timeout. If the app was killed mid-debug, run `dap stop`.

## References (in source repo, not copied here)

- `skills/debugging-code/references/installing-debuggers.md` — fixing missing/failing backends
- `skills/debugging-code/references/advanced-techniques.md` — hangs, concurrency, deep state, loop bisection
- `skills/debugging-code/scripts/install-dap.sh` — installer
