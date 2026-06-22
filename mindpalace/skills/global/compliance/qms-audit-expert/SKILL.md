---
name: QMS Audit Expert (ISO 13485)
description: Use when planning or executing internal audits, classifying nonconformities, verifying CAPA, or preparing for external/certification audits of a medical device QMS — ISO 13485 internal audit methodology.
tags: [iso-13485, internal-audit, qms-audit, nonconformity, capa-verification, audit-planning, audit-checklist, certification-audit, mock-audit, medical-device]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/qms-audit-expert
---

ISO 13485 internal audit methodology for medical device QMS.

## Audit planning (risk-based)
List QMS processes → assign risk (High/Med/Low) → review prior findings/trends → set frequency by risk → assign independent qualified auditors → annual schedule → communicate to owners. *Validation: all ISO 13485 clauses covered within the cycle.*
Frequency: High (design control, CAPA, production validation) quarterly · Medium (purchasing, training, doc control) semi-annual · Low (infrastructure, mgmt review if stable) annual.
**Auditor independence:** not responsible for the area · no direct reporting to auditee · not involved in recent activities under audit · documented qualification for scope.

## Audit scope by clause
4.2 Document Control · 5.6 Management Review · 6.2 Training · 7.3 Design Control · 7.4 Purchasing · 7.5 Production · 7.6 Calibration · 8.2.2 Internal Audit · 8.3 NC Product · 8.5 CAPA.

## Execution
Prepare plan (scope, criteria, schedule) → review docs → opening meeting → collect evidence → classify findings → closing meeting with preliminary findings → report within 5 business days. *Validation: all scope items covered, findings evidence-backed.*
Evidence methods: document review (number, version, date) · interview (name, role, summary) · observation (what/where/when) · record trace (IDs, dates, linkage).
**Finding documentation:** Requirement (specific clause/procedure) → Evidence (observed/reviewed/heard) → Gap (how evidence fails the requirement). Example: "Clause 7.6 requires calibration at intervals. EQ-042 last calibrated 2024-01-15, 12-month interval, today 2025-03-20 → 2 months overdue."

## Nonconformity management
Evaluate vs criteria → assign severity → document with objective evidence → communicate to owner → initiate CAPA for Major/Minor → track to closure → verify effectiveness. *Validation: finding closed only after effective CAPA.*
| Category | Definition | CAPA | Timeline |
|---|---|---|---|
| Major | Systematic failure or absence of element | Yes | 30 days |
| Minor | Isolated lapse / partial implementation | Recommended | 60 days |
| Observation | Improvement opportunity | Optional | As appropriate |
**Classification decision:** required element absent/failed? → systematic (multiple instances) or affects safety → MAJOR, else MINOR. Procedure deviation? → recurring → MAJOR, else MINOR. Neither → OBSERVATION.
CAPA depth: Major = full RCA (5-Why/Fishbone), verify next audit or within 6mo · Minor = immediate cause ID, verify next audit · Observation = noted next audit.

## External audit prep
Complete scheduled internal audits → verify findings closed with effective CAPA → review doc currency → management review with audit as input → prepare facility/personnel → mock audit (full scope) → brief personnel. *Validation: mock-audit findings addressed before external audit.*
Mock audit: external or qualified internal auditor, full upcoming scope, simulate real conditions, document findings, address all Major/Minor before external, brief management on readiness.

## Program metrics
Schedule compliance >90% · finding closure rate >95% · repeat findings <10% · CAPA effectiveness >90% · auditor utilization ~4 days/month.
