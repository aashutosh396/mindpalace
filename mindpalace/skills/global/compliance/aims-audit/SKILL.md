---
name: AIMS Audit (ISO 42001) Interrogation
description: Use before ISO 42001 Stage 1 certification, an annual AIMS internal-audit cycle, or onboarding a new AI system into an existing AIMS — six forcing questions that pressure-test an AI Management System.
tags: [iso-42001, aims, ai-management-system, ai-risk-register, annex-a, internal-audit, certification, ai-governance, compliance]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/aims-audit
---

# AIMS Audit (ISO 42001) — Forcing Questions

Six questions before any ISO 42001 certification commitment, internal audit cycle, or new-system onboarding. Run also when: AI risk register unrefreshed >6 months, after material model change (re-evaluate per Clause 6.1.2), or when findings hint at AIMS/ISMS/QMS duplication.

## The six questions

1. **Does the AIMS scope statement name every AI system?** Scope omission = certification finding. Include embedded models, third-party AI services, "experimental" production systems, and AI features added by SaaS vendors (in scope if they affect your services). Verify Clause 4.3 evidence.
2. **Does the AI policy commit to lawful use AND beneficial purpose AND human oversight AND continual improvement?** Missing any of the four = critical nonconformity at Stage 1. The AI policy is NOT the info-sec policy — separate substantive content (Annex A.2.2 + Clause 5.2). Marketing-copy "AI ethics" doesn't pass.
3. **What's the risk-register coverage, and which Annex A controls treat each risk?** Risk identification without control mapping fails Clause 6.1.3. Build per ISO 23894 methodology. Every high/critical risk links to ≥1 Annex A control. "Additional treatment required" must be closed before Stage 1.
4. **Has the risk assessment been re-run since the last material model change?** Concept drift is not one-time. Article 9 EU AI Act + Clause 6.1.2 require iterative assessment. Material change = retraining on new data, fine-tuning, architecture change, deployment-context change. "Did it 18 months ago" = broken AIMS.
5. **What's the Clause 9.2 internal-audit plan, and is auditor independence respected?** Audit every clause + applicable Annex A control over a rolling 3-year cycle. Same auditor cannot audit own work. Cross-check with the 13485 audit programme if integrated.
6. **Has the AIMS been integrated with existing ISMS/QMS, or built in parallel?** Parallel systems = ~5× ongoing maintenance. ~60% of Clauses 4-10 evidence reuses ISO 27001/13485 with AI scope appended. CAPA should be ONE loop with AI-tagged nonconformities.

## Output

Decision (gap-closure / risk-treatment / audit-scope / new-system-onboarding) → gap analysis Clauses 4-10 (weighted coverage %, critical/major gaps, readiness: ready / stage_2_candidate / not_ready) → AI risk register (totals by severity, requires-additional-treatment count, top risk) → Clause 9.2 audit plan (12-month coverage, independence, prior-year follow-up) → cross-framework reuse (% ISO 27001/13485 reused, net-new for AIMS = mostly Annex A) → verdict 🟢 STAGE-1-READY / 🟡 CLOSE-CRITICALS-FIRST / 🔴 NOT-READY → top 3 actions with owner + date.
