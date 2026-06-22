---
name: ISO 27001 ISMS Audit Prep Interrogation
description: Use before an annual Clause 9.2 internal audit, surveillance audit prep, or Stage 1/2 certification readiness — six sample-driven forcing questions on ISMS scope, risk register, access reviews, supplier management, incident response, and management review.
tags: [iso-27001, isms, clause-9.2, annex-a, access-review, supplier-management, incident-response, risk-register, surveillance-audit, certification]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/iso27001-audit-prep
---

# ISO 27001 ISMS Audit Prep — Forcing Questions

Six sample-driven questions before any internal audit, Stage 1/2, or surveillance audit. Run also after material ISMS-scope change, post-incident, or quarterly during high growth.

## The six questions

1. **What's the audit scope, and is rolling 3-year coverage on track?** Every Clause 4-10 + every applicable Annex A control audited at least once per 3-year cycle. Confirm auditor independence — no self-audit on any sample.
2. **When was the risk register last refreshed, and are treatments linked to Annex A controls?** Quarterly refresh expected, annual minimum. Every high/critical risk links to ≥1 treating Annex A control. Residual-risk acceptance documented + signed.
3. **Show access-review records — quarterly, last 4 quarters.** (Most-cited finding.) A.5.15 + A.8.2 + A.8.3. Sample real records from Okta/IAM, not curated prep packs. Each terminated employee in last 90 days: deprovisioning evidence within 24h SLA. Privileged access reviewed at finer granularity.
4. **Supplier inventory + last review evidence.** (Second-most-cited.) A.5.19-A.5.21. Critical SaaS suppliers reviewed ≥annually. DPAs signed for personal-data sub-processors. AI-specific contract clauses where third-party AI services are used.
5. **Incident-response evidence + post-incident review.** A.5.24-27 + A.6.8. Severity definitions documented + consistently applied. Last 5 incidents have PIR within 30-day SLA. GDPR Art. 33/34 notification timing aligned with A.5.24. Blameless retro, not punitive.
6. **Management-review cadence + inputs.** Clause 9.3 required inputs (audit results, risks, performance, nonconformities, opportunities) — prescriptive, easy to miss. Annual minimum, quarterly for mature programs. Outputs tracked to closure. Integrated cross-framework review preferred.

## Output

Decision (programme-plan / finding-severity / cert-readiness / incident-followup) → audit-programme status (clauses + Annex A scheduled, rolling 3-year coverage, independence) → risk-register health (last refresh, high/critical without control link, residual acceptance) → high-stakes controls (A.5.15/A.8.2/A.8.3, A.5.19-21, A.5.24-27/A.6.8, A.8.15-16 logging — pass/fail with sample) → management review (last date, 9.3 inputs present, overdue actions) → cross-framework impact (SOC 2 ~75% overlap, ISO 42001, GDPR Art. 32) → verdict 🟢 READY / 🟡 CLOSE-CRITICALS / 🔴 NOT-READY → top 3 actions with corrective-action timeline.
