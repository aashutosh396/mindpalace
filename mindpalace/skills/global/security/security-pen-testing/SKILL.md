---
name: Security Penetration Testing
description: Use when performing security audits, penetration testing, vulnerability scanning, OWASP Top 10 checks, or offensive assessments — static analysis, dependency/secret scanning, API/web/infra testing, pen-test reporting.
tags: [pentest, owasp, vulnerability-scanning, sast, idor, jwt, sqli, xss, ssrf, secret-scanning, responsible-disclosure, api-security]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/security-pen-testing
---

# Security Penetration Testing

Offensive testing to find exploitable vulnerabilities. (Not compliance checking; not policy writing.) **Written authorization required** — signed scope/RoE before starting.

## OWASP Top 10 Key Tests
A01 Access Control: IDOR, vertical escalation, CORS, JWT claim manipulation, forced browsing · A02 Crypto: TLS version, password hashing, hardcoded keys, weak PRNG · A03 Injection: SQLi, NoSQLi, command, template, XSS · A04 Insecure Design: rate limiting, business-logic abuse · A05 Misconfig: defaults, debug mode, headers, dir listing · A06 Vulnerable Components: dep audit, EOL, CVEs · A07 Auth: brute force, cookie flags, session invalidation, MFA bypass · A08 Integrity: unsafe deserialization, SRI, CI/CD integrity · A09 Logging: auth events, sensitive data in logs · A10 SSRF: internal IPs, cloud metadata, DNS rebinding.

## Static Analysis
CodeQL (custom queries), Semgrep (rule + auto-fix), ESLint security plugins. Detect: SQLi via concat, hardcoded JWT secrets, unsafe YAML/pickle deserialization, missing security middleware (Express without Helmet).

## Dependency CVE Triage
Tools: `npm audit`, `pip audit`, `govulncheck`, `bundle audit`. Flow: collect → dedupe by CVE across direct+transitive → prioritize (critical + exploitable + reachable = fix now) → remediate → verify (rerun, update lock files).

## Secret Scanning
TruffleHog (`--only-verified`, git history + filesystem), Gitleaks (`.gitleaks.toml` custom rules + allowlists for fixtures). Integrate: pre-commit hooks + CI/CD gates.

## API Security
- **Auth bypass**: JWT `alg:none`, RS256→HS256 confusion, claim mod (`role:admin`, `exp:9999999999`); session fixation.
- **Authz**: IDOR/BOLA (change resource IDs across users, test read/update/delete), BFLA (user hits admin endpoints, expect 403), mass assignment (add `role`/`is_admin`).
- **Rate limiting**: rapid-fire auth endpoints, expect 429. **GraphQL**: introspection off in prod, query depth attacks, batch mutations bypassing limits.

## Web Vulnerabilities
XSS reflected/stored/DOM (innerHTML + location.hash) · CSRF (replay without token, SameSite) · SQLi error/union/time-blind/boolean-blind · SSRF (internal IPs, metadata, IPv6/hex/decimal bypass) · path traversal (`../../../etc/passwd`, encoding).

## Infra
S3 public access (`aws s3 ls --no-sign-request`) · headers (HSTS, CSP no unsafe-inline, X-Content-Type-Options, X-Frame-Options) · TLS (`testssl.sh`, reject TLS1.0/1.1/RC4/3DES) · port scan (`nmap -sV`, flag FTP/Telnet/Redis/MongoDB).

## Reporting
Findings JSON: title, severity, cvss_score + vector, category, description, evidence, impact, remediation, references. Report structure: exec summary → scope → methodology → findings table (by severity) → detailed findings → remediation priority matrix → appendix.

## Responsible Disclosure
Mandatory. Standard timeline: report day 1, follow-up day 7, status day 30, public day 90. Never exploit beyond PoC, encrypt comms, don't access real user data, timestamp everything.

## Anti-Patterns
Testing prod without authorization · ignoring low-severity (chains become critical) · skipping disclosure · relying only on automated tools (miss business-logic + chained exploits) · no defined scope · no remediation guidance · insecure evidence storage · one-time testing.
