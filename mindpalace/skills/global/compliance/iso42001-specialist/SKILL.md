---
name: ISO/IEC 42001 AI Management System Specialist
description: Use when preparing for ISO 42001 certification, scoping internal audit cycles, building an AI risk register, or onboarding AI systems into an ISMS/QMS — gap analysis vs Clauses 4-10, Annex A control mapping, and Clause 9.2 audit planning.
tags: [iso-42001, aims, ai-management-system, ai-governance, annex-a-controls, ai-risk-register, internal-audit, iso-23894, responsible-ai, ai-compliance]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/compliance-team-iso42001/skills/iso42001-specialist
---

Internal-audit-grade operating skill for ISO/IEC 42001:2023 AIMS. **Three decisions, not executive AI strategy, not EU AI Act (binding regulation — see eu-ai-act-specialist).** ISO 42001 is the management system; ISO 23894 is the risk methodology feeding Clause 6.1; ISO 38507 is the governance lens.

## Key questions (ask first)
Does the scope statement (Clause 4.3) name every AI system incl. embedded models + third-party AI services? Does the AI policy (5.2) commit to lawful use AND beneficial purpose AND human oversight AND continual improvement (missing any = nonconformity)? Has risk assessment (6.1.2) been re-run since the last material model change? Who signs the impact assessment for high-impact systems (A.5.4)? Internal audit cadence (9.2)? Documented AI-incident procedure (A.9.3)?

## 1. Gap analysis (Clauses 4-10, Annex SL structure shared with 9001/27001/13485)
| Clause | Requires | Common gap |
|---|---|---|
| 4 Context | AI scope, interested parties | Scope omits third-party AI services |
| 5 Leadership | AI policy, roles, accountability | Policy treats AI ethics as marketing copy |
| 6 Planning | Risk + impact assessment, objectives | Risk register doesn't link to controls |
| 7 Support | Resources, competence, awareness | Competence undefined for ML engineers |
| 8 Operation | Lifecycle planning | Lifecycle not mapped to Annex A controls |
| 9 Performance | Monitoring, audit, mgmt review | Drift monitoring in code but not in review inputs |
| 10 Improvement | Nonconformity, CAPA | CAPA loop duplicated from existing 13485/9001 |
Score each full/partial/missing → prioritized remediation.

## 2. AI risk register + Annex A mapping
Clause 6.1.2 risk assessment + 6.1.3 treatment. Each risk links to ≥1 of 38 Annex A controls (categories A.2-A.10):
A.2 AI policy · A.3 internal organization (roles, reporting concerns) · A.4 resources (data, tooling, HR) · A.5 assessing impacts (impact assessment + documentation) · A.6 lifecycle (objectives, phases, V&V) · A.7 data (management, quality, provenance, preparation) · A.8 information for interested parties (docs, user info, incident comms) · A.9 use of AI (intended use, monitoring, logging) · A.10 third-party & customer relationships.
ISO 23894 = the risk-management process (methodology); Annex A = the controls; the register is the bridge. Document residual-risk acceptance with management signoff.

## 3. Clause 9.2 internal audit plan
Mature-program defaults: cover every clause + applicable Annex A control over a rolling 3-year cycle · annual full audit of Clauses 4/5/9/10 (always relevant) · quarterly/semi-annual deep dives on 6/7/8 by domain · auditor independence (nobody audits their own work; A.6 lifecycle owner can't audit Clause 8 operation).

## Workflows
**Gap closure for cert (4-8wk):** inventory evidence → gap matrix by clause → owner + due date per gap → reuse 27001/13485 artifacts → cross-check EU AI Act → prioritized plan.
**Risk register build (1-2wk):** ISO 23894 identification across lifecycle (data/model/deployment/decommission) → capture source/event/consequence/likelihood/impact → ≥1 Annex A control per high/critical risk → residual acceptance with signoff → log via mgmt review (9.3).
**Annual audit plan (1 day):** pull prior findings + cert cycle phase → schedule → confirm independence → confirm rolling 3-year coverage → mgmt review approval.
**Cross-framework reuse:** map ISO 42001 Annex A against existing 27001 + 13485 evidence; add AI overlay only where existing control doesn't cover; document in scope statement (4.3).

## Output standard
Bottom line (gap severity + one thing to close first) · the decision (gap-closure / risk-treatment / audit-scope) · evidence (clause numbers + control IDs, not adjectives) · how to act (3 steps, owners + dates) · the call only compliance officer/CAIO can make (risk acceptance, scope, cert readiness).
