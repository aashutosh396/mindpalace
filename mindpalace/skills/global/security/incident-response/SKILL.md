---
name: Security Incident Response
description: Use when a security incident is detected/declared and needs classification, triage, severity, escalation, or forensic evidence collection — SEV1-SEV4, incident taxonomy, NIST SP 800-61 lifecycle, regulatory deadlines.
tags: [incident-response, security-triage, sev1, forensics, chain-of-custody, nist-800-61, breach-notification, mitre-attack, escalation, dfrws]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/incident-response
---

# Security Incident Response

Classify, triage, escalate, and collect evidence for declared security incidents. (Not threat hunting; not operational outages — those are separate skills.)

## Incident Taxonomy (default severity / MITRE / SLA)
SEV1 (15 min): ransomware T1486 · data_exfiltration T1048 · apt_intrusion T1566 · supply_chain_compromise T1195 · domain_controller_breach T1078.002.
SEV2 (1h): credential_compromise T1110 · lateral_movement T1021 · malware_infection T1204 · insider_threat T1078 · cloud_account_compromise T1078.004.
SEV3 (4h): unauthorized_access T1190 · policy_violation.
SEV4 (24h): phishing_attempt T1566.001 · security_alert.

**Auto-escalate to SEV1**: ransomware note · active exfil confirmed · CloudTrail/SIEM disabled · DC access · second system compromised. SEV2 min: exfil >1GB, C-suite account accessed.

## Severity → Escalation
- SEV1: SOC Lead + CISO (15m), immediate war room → CISO→CEO→Board; legal+PR standby, regulatory clock starts.
- SEV2: SOC Lead (30m async), 1h bridge; legal if PII.
- SEV3: Security Manager (4h), async.
- SEV4: L3 analyst queue (24h).

## False Positive Filters (run before escalating)
CI/CD agents (jenkins, github-actions) · test/staging/dev tags · scheduled jobs (cron, backup_) · whitelisted svc accounts (svc_monitoring, datadog-agent) · scanners (nessus, qualys, rapid7). Recurring FPs → tune at detection layer, not at triage.

## Forensics (DFRWS, volatile-first)
Phases: Identification → Preservation (write-block, snapshot, legal hold) → Collection (volatility order) → Examination (2h) → Analysis (4h) → Presentation. **Collect first:** RAM dump → running processes + connections → logged-in users → uptime/clock → env vars + kernel modules. Chain of custody per item: SHA-256, UTC timestamp, tool provenance, investigator, transfer log.

## Regulatory Deadlines (clock starts at declaration)
GDPR 72h (up to 4% revenue) · PCI-DSS 24h to acquirer · HIPAA 60 days (>500 individuals) · NY DFS 72h · SEC 4 business days after materiality · CCPA without unreasonable delay · NIS2 24h early warning + 72h. If scope unclear, assume most restrictive deadline.

## SEV1 Timeline
T+5 classify (FP-check) · T+10 page CISO, war room, start clock · T+15 forensic collection (volatile) + containment assessment in parallel · T+30 human approval gate for containment · T+45 execute · T+60 brief Legal if PII/PHI · T+4h evidence package · T+72h regulatory submission.

## Anti-Patterns
Starting clock at investigation end · containing before collecting volatile evidence · skipping FP verification · undocumented IC decisions · treating closure as investigation-complete · single-source classification (need 2 signals for SEV1) · bypassing human approval for mutating containment.
