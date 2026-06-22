---
name: ISMS Audit Expert
description: Use when running an ISO 27001 ISMS internal or certification audit — risk-based audit planning, evidence collection, Annex A control testing, finding classification/corrective action, and Stage 1/Stage 2/surveillance preparation.
tags: [iso-27001, isms-audit, annex-a, statement-of-applicability, nonconformity, internal-audit, surveillance-audit, certification, security-controls]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/isms-audit-expert
---

# ISMS Audit Expert

Internal and external ISMS audit management for ISO 27001 compliance verification and certification.

## Risk-based audit schedule

| Risk | Frequency | Examples |
|---|---|---|
| Critical | Quarterly | Privileged access, vuln mgmt, logging |
| High | Semi-annual | Access control, incident response, encryption |
| Medium | Annual | Policies, awareness training, physical security |
| Low | Annual | Documentation, asset inventory |

Annual planning: review prior findings + risk results → identify high-risk controls + recent incidents → scope to ISMS boundaries → assign independent auditors → schedule with resources → management approval. **Validation:** plan covers all Annex A controls within the certification cycle. Auditor competency: ISO 27001 Lead Auditor (preferred), no operational responsibility for audited processes, understands technical controls + applicable regs (GDPR, HIPAA).

## Audit execution

Pre-audit: review ISMS docs (policies, SoA, risk assessment) → analyze prior reports + open findings → audit plan + interview schedule → notify auditees → checklists for in-scope controls.

Conduct: Opening meeting (confirm scope/objectives/methodology) → Evidence collection (interview owners/operators, review docs+records, observe processes, inspect configs) → Control verification (test design — does it address the risk? + test operation — working as intended? + sample transactions, document evidence) → Closing meeting (preliminary findings, clarify inaccuracies, agree classification + timelines). **Validation:** all in-scope controls assessed with documented evidence.

## Control assessment

Identify control objective (ISO 27002) → choose testing method (inquiry / observation / inspection / re-performance) → set sample size by population + risk → execute + document → evaluate effectiveness. **Validation:** evidence supports the conclusion.

## Finding management

| Severity | Definition | Response |
|---|---|---|
| Major NC | Control failure creating significant risk | 30 days |
| Minor NC | Isolated deviation, limited impact | 90 days |
| Observation | Improvement opportunity | Next cycle |

Finding template: ID (ISMS-YEAR-NUMBER), control ref (A.X.X), severity, evidence (observed / records / interviews), risk impact, root cause, recommendation.

Corrective action: auditee acknowledges → root cause within 10 days → CAP with target dates → implement → auditor verifies effectiveness → close with evidence. **Validation:** root cause addressed, recurrence prevented.

## Certification support

Stage 1 checklist: ISMS scope statement, signed information-security policy, Statement of Applicability, risk-assessment methodology + results, risk-treatment plan, internal-audit results (past 12 mo), management-review minutes.

Stage 2: all Stage 1 findings addressed, ISMS operational ≥3 months, control-implementation evidence, awareness-training records, incident-response evidence, access-review docs.

Surveillance cycle: Y1Q2 high-risk controls + Stage 2 follow-up; Y1Q4 continual improvement + control sample; Y2Q2 full surveillance; Y2Q4 re-certification prep. Target: no major NCs at surveillance.

KPIs: audit-plan completion 100%, finding closure >90% within SLA, major NCs 0 at certification.
