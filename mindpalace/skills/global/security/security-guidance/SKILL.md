---
name: Security Guidance Hook
description: Use when you want a PreToolUse safety net that catches common security anti-patterns (command/SQL/code injection, XSS, unsafe deserialization, GitHub Actions workflow injection) before an Edit/Write/MultiEdit completes.
tags: [security, pretooluse-hook, injection, xss, sql-injection, deserialization, eval, command-injection, claude-code, static-detection]
source: alirezarezvani/claude-skills
derived_from: engineering/security-guidance (David Dworken, MIT)
---

# Security Guidance Hook

A PreToolUse hook (not a slash command) that warns + blocks 12 common security anti-patterns before Claude Code writes them. Once installed, it runs automatically before every `Edit`, `Write`, or `MultiEdit`. Stdlib-only, no dependencies.

## What it catches
Scans the **file path** (GitHub Actions workflow files with risky `${{ }}` expressions) and the **content being written** (substring matches):

| Pattern | Risk |
|---|---|
| GitHub Actions workflow expressions | Workflow command injection via untrusted inputs |
| `child_process.exec`, `exec(`, `execSync(` | Node command injection |
| `new Function`, `eval(` | JS code injection |
| `dangerouslySetInnerHTML`, `document.write`, `.innerHTML =` | XSS |
| `pickle`, `yaml.load(`/`yaml.unsafe_load` | Python/YAML deserialization RCE |
| `os.system`, `from os import system` | Python command injection |
| `shell=True` (subprocess) | Python command injection |
| f-string SQL or `.format` SQL | SQL injection |

## How it works
PreToolUse fires before the edit → hook reads tool input JSON from stdin → extracts file_path + content → checks the pattern table. On first match per file+rule in a session: warn to stderr (Claude sees it), exit 2 (blocks the call), cache the warning key. Already-warned this session → allow (exit 0). No match → allow.

## Why substring, not AST
Faster (ms, no parse), cross-language (one hook for JS/TS/Python/YAML), conservative (false positives dismissed in one keystroke; false negatives are dangerous). Sufficient for 90%+ of cases; layer in semgrep/CodeQL in CI for stricter detection.

## Per-file legitimate override
When a file genuinely needs `eval`/`pickle` (sandboxed REPL, fuzzer parser), document it inline:
```python
# SAFETY: pickle is the required format for this internal tool.
# Does NOT accept untrusted input. See SECURITY.md for boundary analysis.
import pickle
```
The hook still warns on first edit per session; session-state caching allows subsequent edits.

## Disable (sparingly)
`ENABLE_SECURITY_REMINDER=0 claude` bypasses it for the session. Use only for a specific verified-safe operation — the hook is most useful exactly when you're tempted to disable it under deadline pressure.

## Anti-patterns
Disabling by default (trains you to ignore the net) · modifying the pattern list without security review (removing a pattern needs review — patterns map to real CVE classes) · treating "I dismissed it once this session" as long-term policy (use the per-file documentation pattern instead).
