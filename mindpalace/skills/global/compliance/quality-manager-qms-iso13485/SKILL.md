---
name: Quality Manager — QMS ISO 13485
description: Use when implementing or maintaining an ISO 13485:2016 quality management system — gap analysis, document control, internal audits, process validation (IQ/OQ/PQ), supplier qualification, management review, and CAPA.
tags: [iso-13485, qms, internal-audit, process-validation, supplier-qualification, management-review, capa, medical-device, gap-analysis]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/quality-manager-qms-iso13485
---

# Quality Manager — QMS ISO 13485

ISO 13485:2016 QMS implementation, maintenance, and certification support for medical-device organizations.

## QMS implementation

Gap analysis vs ISO 13485 (clause-by-clause current vs required) → prioritize gaps by regulatory criticality, product-safety risk, resource need → roadmap with milestones → Quality Manual (Clause 4.2.2: scope + justified exclusions, process interactions, procedure refs) → create mandatory procedures → deploy with training.

QMS structure: L1 Quality Manual (QM-001) → L2 Procedures (SOP-02-001) → L3 Work Instructions (WI-06-012) → L4 Records.

Mandatory documented procedures: Document Control (4.2.3), Record Control (4.2.4), Internal Audit (8.2.4), NC Product Control (8.3), Corrective Action (8.5.2), Preventive Action (8.5.3).

## Internal audit (Clause 8.2.4)

Annual program: identify processes → risk-rate frequency (prior findings, reg/process changes, complaint trends) → assign independent qualified auditors → schedule → management approval → track completion.

Individual audit: plan (scope/criteria/schedule) → notify auditee ≥1 week → review procedures + prior results → checklist → opening meeting → collect evidence (doc review, record sampling, observation, interviews) → classify findings → closing meeting → report within 5 business days.

Finding classes: Major NC (system absence/breakdown/reg violation → 30 days CAPA); Minor NC (single lapse → 60 days CAPA); Observation (potential risk → track next audit). Auditor must be independent of the area audited.

## Process validation (Clause 7.5.6)

Validate where output can't be verified by inspection (sterilization, welding, sealing, software). Protocol (description, parameters, equipment, acceptance criteria, statistics) → IQ (equipment installed correctly) → OQ (parameter ranges, process control) → PQ (production conditions, output meets reqs) → report. Revalidation triggers: equipment change (affected phases), parameter change (OQ+PQ), material change (PQ), process failure (full), periodic (~3 yrs). Standards: EO ISO 11135, steam ISO 17665, radiation ISO 11137, packaging ISO 11607.

## Supplier qualification (Clause 7.4)

Categorize: A critical (safety/performance), B major (quality), C minor (indirect). Evaluate quality system, technical capability, quality history, financial stability. Category A → on-site audit + quality agreement. Score: >80 approved, 60-80 conditional, <60 not approved. Weighted criteria: Quality System 30% (ISO 13485=30/ISO 9001=20/documented=10), Quality History 25% (reject <1%=25), Delivery 20% (on-time >95%=20), Technical 15%, Financial 10%.

## Management review (Clause 5.6.2) — required inputs

Audit results, customer feedback/complaints, process performance, product conformity/NCs, CAPA status, prior-action follow-up, changes affecting QMS, recommendations. Outputs (5.6.3): improvement decisions, product-requirement changes, resource needs.

## Record retention (cite ISO 13485 §4.2.5 + retained 21 CFR 820.35)

Records retained at least the lifetime of the device (as defined by the organization) but not less than two years. DMR/DHR/DHF/complaints → life of device + 2 yrs; training → employment + 3 yrs; audit/CAPA → 7 yrs (best practice).

## Decision aids

Exclusions (4.2.2) need justification (e.g. 7.3 only if no design done; 7.5.5 if no sterile products). NC disposition tree: reworkable? → rework per SOP; usable as-is? → concession + MRB/customer approval; else scrap/return. CAPA auto-trigger: safety-related complaint, major NC, field failure, safety-impact deviation.

> Checklists structure conformity assessment; they do not certify compliance. Final determinations need the named QMR's sign-off; confirm current ISO 13485 / 21 CFR 820 text before relying on citations.
