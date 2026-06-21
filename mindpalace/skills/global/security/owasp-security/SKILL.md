---
name: owasp-security
description: "Use when reviewing or writing code for security vulnerabilities, implementing authentication/authorization, handling user input, doing a security review, or building LLM/AI-agent systems — covers OWASP Top 10:2025, ASVS 5.0, LLM Top 10 (2025), and Agentic AI Top 10 (2026)."
version: 1.0.0
license: MIT
tags: [security, owasp, vulnerability, authentication, authorization, injection, llm-security, prompt-injection, code-review, appsec]
source: https://github.com/agamm/claude-code-owasp
derived_from: awesomeclaude
---

# OWASP Security Best Practices

Apply these standards when writing or reviewing code. Think like a senior security
researcher: deny by default, fail closed, treat all external/LLM output as untrusted.

## When to use
- Writing or reviewing auth, authorization, crypto, or password storage code
- Handling user input or external data; designing API endpoints
- Reviewing a diff/PR for security vulnerabilities
- Building AI agents or integrating LLMs, RAG pipelines, function-calling tools
- Configuring app security settings or handling errors/exceptions

## OWASP Top 10:2025 — quick reference

| # | Vulnerability | Key Prevention |
|---|---------------|----------------|
| A01 | Broken Access Control | Deny by default, enforce server-side, verify ownership |
| A02 | Security Misconfiguration | Harden configs, disable defaults, minimize features |
| A03 | Software Supply Chain Failures | Lock versions, verify integrity, audit deps |
| A04 | Cryptographic Failures | TLS 1.2+, AES-256-GCM, Argon2/bcrypt for passwords |
| A05 | Injection | Parameterized queries, input validation, safe APIs |
| A06 | Insecure Design | Threat model, rate limit, design security controls |
| A07 | Authentication Failures | MFA, check breached passwords, secure sessions |
| A08 | Data Integrity Failures | Sign packages, SRI for CDN, safe serialization |
| A09 | Logging/Alerting Failures | Log security events, structured format, alerting |
| A10 | Mishandling Exceptions | Fail-closed, hide internals, log with context |

## Code review checklist

**Input** — validate server-side; parameterized queries (no string concat); length limits; allowlist over denylist.
**Auth/Sessions** — Argon2/bcrypt (never MD5/SHA1); session tokens 128+ bit entropy; invalidate on logout; MFA for sensitive ops.
**Access control** — check for framework auth middleware (Next.js `middleware.ts`, Express middleware) before flagging missing per-route auth; authorize every request; non-manipulable object refs; deny by default; review privilege-escalation paths.
**Data** — encrypt at rest; TLS in transit; no secrets in URLs/logs; secrets in env/vault, not code.
**Errors** — no stack traces to users; fail closed (deny on error); log all exceptions with context; consistent responses (no enumeration).

## Key secure patterns

```python
# SQL injection — SAFE
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
# Command injection — SAFE
subprocess.run(["convert", filename, "output.png"], shell=False)
# Passwords — SAFE
from argon2 import PasswordHasher; PasswordHasher().hash(password)
# Fail-closed auth check
def check_permission(user, resource):
    try:
        return auth_service.check(user, resource)
    except Exception as e:
        logger.error(f"Auth check failed: {e}")
        return False  # deny on error
```
Access control: gate routes with `@login_required` and verify ownership
(`if current_user.id != user_id and not current_user.is_admin: abort(403)`).
Error handler: log with a uuid, return generic `{"error":..., "id":...}` to the user.

## OWASP LLM Top 10 (2025) — for apps calling LLMs

| # | Risk | Mitigation |
|---|------|------------|
| LLM01 | Prompt Injection | Separate trusted instructions from untrusted data; isolate privileges |
| LLM02 | Sensitive Info Disclosure | Strip PII from context; restrict per-user retrieval |
| LLM03 | Supply Chain | Verify model provenance; pin model + adapter versions |
| LLM04 | Data/Model Poisoning | Validate training sources; integrity tests |
| LLM05 | Improper Output Handling | Treat all LLM output as untrusted before SQL/shell/HTML/eval/tool calls |
| LLM06 | Excessive Agency | Minimize tools/permissions; human approval for destructive actions |
| LLM07 | System Prompt Leakage | No secrets/keys/auth logic in system prompt — assume extractable |
| LLM08 | Vector/Embedding Weaknesses | Tenant-isolate vector stores; access-control retrieval |
| LLM09 | Misinformation | Cite sources; require grounding for high-stakes answers |
| LLM10 | Unbounded Consumption | Rate-limit per user/key; cap tokens/tool-calls; timeouts; cost monitoring |

LLM checklist highlights: never blind-concat user input into a system prompt (use
delimiters/roles); treat output as untrusted before any sink; minimal least-privilege
tool surface; human approval for side-effecting tools; per-user token/cost budgets;
hard timeouts; redact PII before sending to model or logs.

## OWASP Agentic AI Top 10 (2026) — for AI agent systems

ASI01 Goal Hijacking · ASI02 Tool Misuse · ASI03 Identity/Privilege Abuse ·
ASI04 Agentic Supply Chain · ASI05 Unexpected Code Execution · ASI06 Memory/Context
Poisoning · ASI07 Insecure Inter-Agent Comms · ASI08 Cascading Failures ·
ASI09 Human-Agent Trust Exploitation · ASI10 Rogue Agents.

Agent checklist: sanitize all inputs; least-privilege tools; short-lived scoped
credentials; verify+sandbox third-party plugins/MCP; isolated code execution; auth+encrypt
inter-agent comms; circuit breakers; human approval for sensitive ops; behavior/anomaly
monitoring; kill switch.

## ASVS 5.0 levels
- **L1 (all apps):** passwords 12+ chars, check breached lists, rate-limit auth, 128+ bit session tokens, HTTPS everywhere.
- **L2 (sensitive data):** + MFA, key management, comprehensive logging, input validation on all params.
- **L3 (critical):** + HSM for keys, threat-model docs, advanced monitoring, pentest validation.

## Deep analysis mindset (any language)
For languages not covered in the reference, examine: memory model, type system (coercion/
type confusion), serialization (pickle/Marshal equivalents — all dangerous), concurrency
(races, TOCTOU), FFI boundaries, std-lib CVE history, package ecosystem (typosquatting,
dependency confusion), build-system injection, debug-vs-release behavior, and failure mode
(silent? stack trace? fail-open?).

## Reference files (load on demand from source repo)
- `.claude/skills/owasp-security/reference/languages.md` — per-language unsafe/safe
  examples and dangerous functions for 20+ languages (JS/TS, Python, Java, C#, PHP, Go,
  Ruby, Rust, Swift, Kotlin, C/C++, Scala, R, Perl, Shell, Lua, Elixir, Dart, PowerShell, SQL).
- `.claude/skills/owasp-security/reference/owasp-report.md` — full deep-dive on every
  OWASP 2025–2026 standard.

Fetch via: `https://raw.githubusercontent.com/agamm/claude-code-owasp/main/<path>`
