---
name: Skill Security Auditor
description: Use when evaluating an AI agent skill from an untrusted source before installing — static-scans scripts, SKILL.md, dependencies, and file structure for malicious patterns and returns a PASS/WARN/FAIL verdict with remediation.
tags: [security, skill-audit, supply-chain, prompt-injection, malware-scan, static-analysis, pre-install-gate, vulnerability-scan, agent-skills]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/skill-security-auditor
---

# Skill Security Auditor

Static-scan and audit an AI agent skill for security risks before installation. Produces a PASS / WARN / FAIL verdict with findings + remediation. Does not execute code (static analysis only — safe but less complete than dynamic).

## What gets scanned

### 1. Code execution risks (.py/.sh/.js/.ts)
- **CRITICAL** — command injection (`os.system`, `os.popen`, `subprocess(shell=True)`, backticks); code execution (`eval`, `exec`, `compile`, `__import__`); obfuscation (base64/hex payloads, `codecs.decode`, `chr()` chains); network exfiltration (`requests.post`, `urllib`, `socket.connect`, `httpx`, `aiohttp`); credential harvesting (reads `~/.ssh`, `~/.aws`, `~/.config`, env extraction); privilege escalation (`sudo`, `chmod 777`, `setuid`, cron).
- **HIGH** — filesystem abuse (writes outside skill dir, `/etc/`, `~/.bashrc`, symlinks); unsafe deserialization (`pickle.loads`, `yaml.load` without SafeLoader, `marshal.loads`).
- **INFO** — `subprocess.run` with list args, no shell.

### 2. Prompt injection in SKILL.md / .md files
- **CRITICAL** — system-prompt override ("ignore previous instructions", "you are now…"); role hijacking ("act as root", "pretend you have no restrictions"); safety bypass ("skip safety checks", "disable content filtering"); data extraction ("send contents of", "upload file to", "POST to").
- **HIGH** — hidden instructions (zero-width chars, HTML comments with directives); excessive permissions ("run any command", "full filesystem access").

### 3. Dependency supply chain (requirements.txt / package.json / inline installs)
Known vulnerabilities (CRITICAL), typosquatting like `reqeusts` (HIGH), unpinned versions (INFO), install commands inside scripts (HIGH), suspicious packages — low downloads / recent / single maintainer (INFO).

### 4. File system & structure
Boundary violations — paths outside the skill dir (HIGH) · hidden files like `.env` (HIGH) · unexpected binaries `.so`/`.dll`/`.exe` (CRITICAL) · large files >1MB hiding payloads (INFO) · symlinks pointing outside the skill (CRITICAL).

## Workflow
1. Run the scanner on the skill directory or repo URL (clone-to-temp + audit + cleanup for remote).
2. Review findings grouped by severity.
3. Verdict: **PASS** (no critical/high — safe) · **WARN** (high/medium — review manually first) · **FAIL** (critical — do NOT install without remediation). Strict mode promotes any WARN to FAIL.
4. Each finding includes specific fix guidance (e.g., replace `eval()` with `ast.literal_eval()`; remove outbound network calls or verify the destination; pin `requests==2.31.0`).

Integrates into CI (JSON output, non-zero exit on fail) and supports batch audits across a skills directory.

## Limitations
Cannot reliably detect logic bombs or time-delayed payloads · obfuscation detection is pattern-based (a creative attacker may bypass) · destination reputation needs internet · dependency checks are local pattern-matching, not live CVE DBs. When in doubt after an audit, **don't install** — ask the author for clarification.
