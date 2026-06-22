---
name: Compliance OS (Multi-Framework Orchestrator)
description: Use when standing up a multi-framework compliance program, planning an annual audit calendar, or preparing for certification — picks which of 12 frameworks apply, computes cross-framework control overlap/evidence reuse, simulates internal audits, and consolidates a unified evidence pool.
tags: [compliance, grc, multi-framework, cross-framework-mapping, evidence-reuse, audit-simulation, iso-27001, soc2, iso-13485, gdpr, framework-selector, certification]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/compliance-os
---

# Compliance OS — Meta-Orchestrator

Multi-framework compliance program orchestration across 12 frameworks (ISO 27001/13485/42001/14971, EU AI Act, EU MDR 745, GDPR, SOC 2, FDA QSR, NIST CSF 2.0, NIS2, HIPAA). Four decisions — does NOT replace per-framework deep-dive skills; it orchestrates them. NOT a substitute for binding legal advice; review novel cross-walks with counsel.

## Decision 1 — Which frameworks apply?

Score the company profile (industry, geography, AI use, medical, financial, headcount, customers, PHI, NIS2 entity status, US-gov-contractor) → applicable frameworks + dependency graph. Deterministic rules:
- Medical device → ISO 13485 + ISO 14971 + (EU MDR 745 if EU) + (FDA QSR if US)
- Customer-facing AI → ISO 42001 + EU AI Act (if EU users) + GDPR (if personal data)
- B2B SaaS with enterprise customers → SOC 2 + ISO 27001 (procurement-driven)
- EU customers + personal data → GDPR mandatory
- Highly regulated industry → sectoral overlays (NYDFS, FINMA, HIPAA)

**Key question:** name *every* applicable framework — forgetting one means rebuilding the audit program later.

## Decision 2 — Cross-framework overlap

Parse each framework's control library; compute control-level overlap. Per merged control: mapping confidence (HIGH = same evidence / MEDIUM = existing + overlay / LOW = new artefact), evidence-reuse opportunity (one artefact satisfies N controls), per-framework citation. **Densest overlap:** ISO 27001 Annex A ↔ SOC 2 TSC ≈ 75% shared. ISO 42001 adds AI controls; GDPR adds privacy. Without overlap analysis you collect the same access-review records 3×.

## Decision 3 — Audit simulation

Generate a realistic mock internal audit per ISO 19011 + IIA IPPF: 8-15 finding scenarios, severity distribution ≥40% observations/OFI and ≤15% critical/major (healthy program), 3-5 interview questions per scoped control, doc-review request list, walkthroughs. All-critical = destructive audit or genuinely failing; all-observation = audit too superficial.

## Decision 4 — Evidence pool

Consolidate evidence requirements across enabled frameworks: artefact list (access-review log, supplier risk register, incident log) → per artefact list (framework, control) tuples it satisfies → reuse-leverage score (build HIGH-leverage ≥5-mapping artefacts first) → acquisition cost. Each artefact needs one accountable owner; stale evidence is an effective gap even if the artefact existed historically.

## Workflows

- **Program bootstrap (4-8 wk):** framework selector → per-framework gap analysis → cross-framework mapper → evidence pool generator → prioritized backlog with owners + dates.
- **Annual audit calendar:** refresh selector → per-framework audit-plan tools → coordinate calendar (auditor independence + capacity, no surveillance stacking) → simulate per framework to prep auditors.
- **Pre-certification (6-12 wk):** gap analysis for new framework → map against already-certified frameworks → reuse HIGH-confidence evidence, build MEDIUM/LOW → mock audit → close gaps before external Stage 1.
- **Evidence consolidation (quarterly):** refresh pool → surface HIGH-reuse artefacts → confirm freshness within retention → audit the pool itself (no orphan controls, no stale evidence).

## Key questions (ask first)

Have you named every applicable framework? What certificate/regulation do you already operate (your reuse anchor)? What's the audit calendar (auditor independence + capacity)? Where is evidence stored (index it)? What's the management-review cadence (one integrated review per Annex SL satisfies all)? Who owns the meta-program?

## Output

Bottom line (multi-framework picture + biggest reuse opportunity) → Decision (framework-set / overlap-map / audit-plan / evidence-consolidation) → Evidence (framework names + control IDs, not adjectives) → 3 next steps with owners + dates → the call only the compliance officer can make.
