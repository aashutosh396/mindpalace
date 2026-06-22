---
name: Quality Documentation Manager
description: Use when designing or auditing document control for an ISO 13485 / FDA-regulated QMS — document numbering, lifecycle, review/approval, change control, and 21 CFR Part 11 electronic-record compliance.
tags: [document-control, qms, iso-13485, 21-cfr-part-11, version-control, change-control, electronic-signature, audit-trail, sop]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/quality-documentation-manager
---

# Quality Documentation Manager

Document control for ISO 13485-compliant QMS: numbering, approval workflows, change control, electronic records.

## Document control workflow

Assign number → create from controlled template → route to required reviewers → address comments (documented responses) → obtain approval signatures → assign effective date + distribute → update Document Master List. **Validation:** accessible at point of use; obsolete versions removed.

Lifecycle stages: Draft → Review → Approved → Effective → Superseded → Obsolete (archive per retention).

Document types/prefixes: QM (Quality Manual), SOP (procedure), WI (work instruction), TF (template/form), SPEC (specification), PLN (plan).

## Numbering system

Format `PREFIX-CATEGORY-SEQUENCE[-REVISION]`, e.g. `SOP-02-001-A`. Category codes: 01 Quality Mgmt, 02 Document Control, 03 HR/Training, 04 Design & Dev, 05 Purchasing, 06 Production, 07 QC, 08 CAPA, 09 Risk Mgmt (ISO 14971), 10 Regulatory.

Revision: major → increment number; minor → sub-revision (01→01.1); administrative → letter suffix. Workflow: author requests number → DocControl verifies category + assigns next sequence → recorded in Master List → author creates doc. **Validation:** format correct, no duplicates.

## Review and approval

Author drafts → submit via routing/DMS → reviewers (by doc type) comment within 5-10 business days → author dispositions each comment (accept / accept-with-mod / reject / defer — all documented) → approvers sign + date. Approval matrix: Level 1 (Policy/QM) = CEO/delegate + QA Mgr; Level 2 (SOP) = Dept Mgr + QA Mgr; Level 3 (WI/TF) = Supervisor + QA Rep. Each signature carries name, signature, date, role.

## Change control

Identify change → Change Request Form with justification → DocControl logs + assigns change number → route for impact assessment → approve by classification → implement → update revision + change history. Classification: Administrative (no content impact → DocControl); Minor (Process Owner + QA); Major (full review cycle); Emergency (expedited + retrospective). Impact checklist: training? equipment/systems? revalidation? regulatory filings? related docs? records?

Every document carries a change-history table (Revision | Date | Description | Author | Approver).

## 21 CFR Part 11

Applies to FDA-required records, records submitted to FDA, e-signatures on required records (NOT paper or non-regulated docs).

Electronic record controls: validate system → secure audit trail for all changes → restrict access → human-readable copies → protect through retention. **Validation:** audit trail captures who/what/when.

Audit trail must be: secure (user-immutable), computer-generated, time-stamped, retains original values, records user identity.

E-signature must be: unique to individual, ≥2 components (user ID + password min), display name+date/time+meaning, linked to record (cannot be excised/copied).

System controls checklist — Access: unique IDs, password complexity, lockout, session timeout. Audit trail: log creation + modifications (old/new values) + identity + timestamps. Security: RBAC, encryption at rest + in transit, tested backup/recovery.

## Periodic review

Policy: 3 yrs; SOP: 2 yrs; WI: 2 yrs; SPEC: with product changes; Forms: 3 yrs.

Common audit findings + prevention: obsolete docs in use → distribution control; missing signatures → enforce workflow before release; incomplete change history → require with each revision; no review schedule → review calendar; inadequate audit trail → validate DMS for Part 11.

> Validators check structure/completeness — they do not certify compliance. Approval/release decisions belong to the document owner; route classification/submission-record questions to Regulatory Affairs.
