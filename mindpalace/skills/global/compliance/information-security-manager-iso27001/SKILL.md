---
name: Information Security Manager (ISO 27001)
description: Use when designing an ISMS, running security risk assessments, implementing/auditing ISO 27001/27002 controls, pursuing certification, or responding to security incidents — especially HealthTech/MedTech.
tags: [iso-27001, isms, information-security, security-risk-assessment, soa, iso-27002, security-controls, incident-response, certification, healthcare-security]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/information-security-manager-iso27001
---

Implement and manage an ISMS aligned with ISO 27001:2022 + healthcare regulatory requirements.

## Workflow 1: ISMS implementation
1. **Scope & context** — interested parties + requirements, ISMS boundaries, internal/external issues. *Validation: scope approved by management.*
2. **Risk assessment** (Clause 6.1.2) — identify assets, assess threats/vulnerabilities, calculate risk, choose treatment. *Validation: register has all critical assets with owners.*
3. **Select & implement controls** — map risks to ISO 27002 (Organizational / People / Physical / Technological). *Validation: Statement of Applicability documents every control with justification.*
4. **Monitoring** — metrics: incident count/severity, control effectiveness, training completion, finding closure rate. *Validation: real-time compliance dashboard.*

## Workflow 2: security risk assessment
1. **Asset inventory** — Information (patient records, source code = Confidential) / Software (EHR, APIs = Critical) / Hardware / Services / People; all with owners + classification.
2. **Threat analysis** per asset category (cover top-10 industry threats).
3. **Vulnerability assessment** — technical (unpatched, weak configs), process (missing procedures), people (training, insider).
4. **Evaluation & treatment** — `Risk = Likelihood × Impact`:
| Level | Score | Treatment |
|---|---|---|
| Critical | 20-25 | Immediate |
| High | 15-19 | Plan within 30 days |
| Medium | 10-14 | Plan within 90 days |
| Low | 5-9 | Accept or monitor |
| Minimal | 1-4 | Accept |

## Workflow 3: incident response
1. **Detect & report** (breach, malware, leakage, compromise, policy violation) — log within 15 min.
2. **Triage** — Critical (breach/down) immediate · High 1h · Medium 4h · Low 24h.
3. **Contain & eradicate** — isolate systems, preserve evidence, block vectors, remove artifacts.
4. **Recover & learn** — restore from clean backups, verify integrity, document timeline, post-incident review, update controls. *Report within 5 business days.*

## Certification readiness
**Before Stage 1:** scope approved · ISP published · risk assessment done · SoA finalized · internal audit conducted · management review done · nonconformities addressed.
**Before Stage 2:** controls implemented + operational · evidence of effectiveness · staff trained · incidents logged/managed · metrics collected 3+ months.

## Validation checkpoints
Scope (signed doc) · Risk (register with owners) · Controls (SoA) · Operation (dashboard) · Audit (report). Run periodic compliance checks (monthly) + gap analysis (quarterly) with remediation recommendations.
