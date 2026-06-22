---
name: SOC 2 Compliance
description: Use when preparing for SOC 2 audits, mapping Trust Service Criteria, building control matrices, collecting audit evidence, performing gap analysis, or assessing Type I vs Type II readiness — for SaaS/cloud.
tags: [soc2, trust-service-criteria, control-matrix, audit-evidence, gap-analysis, type-i, type-ii, vendor-risk, continuous-compliance, aicpa]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/soc2-compliance
---

SOC 2 Type I/II preparation for SaaS: TSC mapping, control matrix, evidence, gap analysis, audit readiness.

## Type I vs Type II
| | Type I | Type II |
|---|---|---|
| Scope | Control design at a point in time | Design + operating effectiveness over a period |
| Window | Single date | 3-12 mo (typically 6) |
| Evidence | Descriptions, policies | + operating evidence (logs, tickets, screenshots) |
| Best for | First-time, rapid market need | Mature orgs, enterprise customers |
Journey: Gap assessment (4-8wk) → Remediation (8-16wk) → Type I audit (4-6wk) → Observation (6-12mo) → Type II audit (4-6wk) → annual renewal.

## Trust Service Criteria (Security required; others optional by business need)
- **Security (CC1-CC9, required)** — CC1 control environment · CC2 communication · CC3 risk assessment · CC4 monitoring · CC5 control activities · CC6 logical/physical access · CC7 system operations (vuln mgmt, anomaly detection, IR) · CC8 change management · CC9 vendor risk.
- **Availability (A1)** — capacity, recovery ops, recovery testing (select when uptime/SLAs matter).
- **Confidentiality (C1)** — identification, protection (encryption, DLP), disposal (select for trade secrets/confidential data).
- **Processing Integrity (PI1)** — accuracy, completeness, timeliness, authorization (select when data accuracy critical).
- **Privacy (P1-P8)** — notice, consent, collection, use/retention/disposal, access, disclosure, quality, monitoring (select for PII; complements GDPR).

## Control matrix
Per control: ID (SEC-001 / AVL-/CON-/PRI-/PRV-) · TSC mapping (CC6.1, A1.2) · description · type (preventive/detective/corrective) · owner · frequency · evidence type · testing procedure. Every selected TSC criterion needs ≥1 control.

## Gap analysis
1. Current state — inventory controls, map to TSC, collect evidence samples, interview owners.
2. Identify gaps — missing / partially implemented / design gaps / operating gaps (Type II).
3. Remediation — per gap: description, action, owner, priority, target date, dependencies.
4. Timeline by priority: Critical 2-4wk · High 4-8wk · Medium 8-12wk · Low 12-16wk.

## Evidence collection
By area: access mgmt (access reviews, provisioning tickets) · change mgmt (change tickets, approvals) · IR (tickets, postmortems) · vuln mgmt (scan reports, patch records) · encryption (configs, cert inventory) · backup/recovery (logs, DR tests) · monitoring (alert configs, dashboards) · policy (signed policies, version history) · vendor (assessments, SOC 2 reports).
Automate: access reviews (IAM+ticketing triggers) · config evidence (IaC snapshots) · scans (scheduled) · change mgmt (git audit trail) · uptime (SLA dashboards) · backup verification (automated restore tests).

## Audit readiness (4-6wk before)
All controls documented · evidence for full observation period (Type II) · gaps remediated · policies signed within 12mo · access reviews on cadence · scans current (no critical/high over SLA) · IR plan tested within 12mo · vendor assessments current · DR/BCP tested · security training complete.
Scoring: 90-100% ready · 75-89% minor gaps · 50-74% significant gaps · <50% not ready.

## Vendor management
Inventory → risk-tier by data access → due diligence (SOC 2 reports, questionnaires) → contractual protections (DPAs, breach notification) → ongoing monitoring. Tiers: Critical (processes/stores customer data) annual + continuous, SOC 2 Type II + pentest · High (accesses environment) annual · Medium annual questionnaire · Low biennial. Subservice orgs (AWS/GCP/Azure): mostly **carve-out method** + complementary user entity controls (CUECs).

## Anti-patterns
Point-in-time compliance · manual evidence collection · missing vendor assessments · copy-paste policies · security theater (controls on paper not followed) · skipping Type I · over-scoping TSC · treating audit as a one-off project. → move to continuous monitoring + automated evidence + compliance built into daily ops.
