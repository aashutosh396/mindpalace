---
name: Senior Security — Threat Modeling & Router
description: Use for STRIDE threat modeling, DREAD risk scoring, data-flow-diagram threat analysis, a quick secret scan, or routing a security request to the right specialist lane.
tags: [security, threat-modeling, stride, dread, dfd, secret-scanning, risk-scoring, security-routing, owasp, mitigation]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-security
---

# Senior Security — Threat Modeling & Router

Owns exactly one job — **STRIDE/DREAD threat modeling** (plus a quick secret scan) — and routes every other security request to the specialist lane that owns it. Never duplicate sibling content; route instead.

## Routing table (read first)
| User wants | Route to |
|---|---|
| Vulnerability assessment, pen-test methodology, OWASP Top 10 | security-pen-testing |
| Incident triage, SEV classification, forensics, containment | incident-response |
| Production outage command (non-security) | incident-commander |
| Security monitoring, CVE SLAs, compliance (SOC 2), headers | senior-secops |
| Hostile/adversarial code review | adversarial-reviewer |
| Secure code review within general review | code-reviewer |
| Cloud IAM escalation, S3 exposure, security groups | cloud-security |
| Threat hunting, IOC sweeps, anomaly detection | threat-detection |
| Red-team engagement planning, ATT&CK kill chains | red-team |
| LLM/AI attack surface (prompt injection, poisoning) | ai-security |

For multi-lane requests ("secure this architecture"), do the threat model here first — its prioritized threats + mitigations tell you which siblings to load next. Never bulk-load security skills speculatively.

## STRIDE threat modeling workflow
1. **Scope** — assets to protect, trust boundaries, data flows (external entities, processes, data stores, flows).
2. **Generate the model per component** — per-threat STRIDE category + DREAD score (Damage, Reproducibility, Exploitability, Affected users, Discoverability — each 1-10) + suggested mitigations. Repeat per DFD element.
3. **Consume output** — sort by DREAD descending; everything ≥7 average needs a named mitigation owner before the design ships. Map each mitigation to the responsible sibling lane (IAM threats → cloud-security; injection → code-reviewer).
4. **Quick secret sweep** while the codebase is open — 20+ patterns (AWS keys, GitHub tokens, private keys, generic creds). Any critical/high finding blocks merge until rotated and moved to a secret manager.
5. **Verification gate** — every DFD element has ≥1 STRIDE row considered, every threat with DREAD ≥7 has owner + mitigation, secret scan exits zero high/critical. Re-run both tools after mitigations land — that re-run is the done signal, not the document.

## STRIDE-per-element matrix
| DFD Element | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | X | X | X | |
| Data Flow | | X | | X | X | |

S=Spoofing→authn · T=Tampering→integrity · R=Repudiation→audit logs · I=Info Disclosure→encryption/access control · D=DoS→rate limiting/redundancy · E=Elevation→least privilege.

## Owned references
Security architecture patterns (Zero Trust, defense-in-depth, authN patterns, API security) and cryptography implementation (AES-GCM, Ed25519, Argon2id password hashing, key management) live here because no sibling ships them. For *operating* controls (scanning, compliance, monitoring), route to senior-secops.
