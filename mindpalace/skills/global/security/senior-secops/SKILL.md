---
name: Senior SecOps Engineer
description: Use when running a security audit, responding to a CVE, hardening infra, checking OWASP Top 10, enforcing compliance (SOC2/PCI/HIPAA/GDPR), or adding security gates to CI/CD — SAST/DAST, dependency scanning, compliance verification.
tags: [secops, security-audit, cve, owasp, sast, dast, compliance, soc2, pci-dss, secrets-scanning, supply-chain, sbom]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-secops
---

# Senior SecOps Engineer

Vulnerability management, compliance verification, secure coding, security automation.

## Three Scan Capabilities
- **Code scan**: hardcoded secrets (API keys, AWS creds, GitHub tokens, private keys), SQLi (concat/f-string/template), XSS (innerHTML/unsafe DOM/React), command injection (shell=True/exec/eval), path traversal.
- **Dependency/CVE scan**: npm (package-lock), Python (requirements/pyproject), Go (go.mod) → CVE IDs + CVSS + fixed versions + risk score.
- **Compliance check**: SOC2 / PCI-DSS / HIPAA / GDPR — access control, encryption at rest+transit, audit logging, auth strength (MFA, hashing), docs, CI/CD controls.

Exit codes for gates: 0 = clean, 1 = high, 2 = critical. Block deploy on critical.

## Workflows
- **Security audit**: code scan (medium) → dependency scan (high) → compliance (all) → combined JSON reports. STOP on exit 2 at each stage.
- **CI/CD gate**: run all three on PR; each fails pipeline on its exit code.
- **CVE triage**: (1) assess affected systems + active exploitation + environmental CVSS — STOP if 9.0+ internet-facing, escalate. (2) prioritize: Critical(9.0+ internet-facing) 24h, High(7-8.9) 7d, Med(4-6.9) 30d, Low 90d. (3) remediate: update dep, re-scan (must be clean), test regressions, deploy + monitor. (4) verify CVE gone.
- **Incident response**: detect+classify SEV1-4 (0-15m) → contain + rotate creds + preserve evidence (15-60m) → eradicate + patch (1-4h) → recover from clean backup (4-24h) → post-incident RCA + lessons (24-72h).

## Secure Coding Checklist
Server-side input validation + allowlists + context-specific sanitization · HTML/URL/JS output encoding · bcrypt/argon2 + MFA + strong policy · secure random session IDs + HttpOnly/Secure/SameSite + 15-min idle timeout · log without secrets + generic user errors + no stack traces in prod · env vars / secrets manager + no committed secrets + rotation.

## Compliance Anchors
SOC2 CC6/CC7/CC8 (access/ops/change mgmt) · PCI-DSS Req3/4 (TLS1.2+), 6 (secure dev), 8 (MFA), 10/11 (logging/testing) · HIPAA 164.312 (unique IDs, audit, MFA, TLS) · GDPR Art25/32 (privacy-by-design), 33 (72h breach notice), 17/20 (erasure/portability).

## OWASP Top 10 Quick-Check (15 min)
A01 role checks every endpoint + horizontal priv-esc · A02 TLS1.2+ no secrets in logs · A03 parameterized queries · A04 threat model exists · A05 no defaults, generic errors · A06 zero critical CVEs · A07 MFA on admin + brute-force protection · A08 signed artifacts · A09 audit logs + alerts · A10 SSRF block 169.254.169.254. Deep dive → pen-testing skill.

## Secret Scanning + Supply Chain
detect-secrets pre-commit + gitleaks in CI. SBOM via syft (CycloneDX/SPDX). Sign artifacts with cosign (keyless OIDC). SLSA L1 (provenance) → L4 (two-party review, hermetic). Bad: `API_KEY = "sk-..."`; good: `os.environ.get` or vault.
