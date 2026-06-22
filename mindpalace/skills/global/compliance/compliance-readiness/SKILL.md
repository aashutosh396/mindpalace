---
name: Compliance Readiness Interrogation
description: Use before adopting a new compliance framework, finalizing the annual audit calendar, or signing off certification Stage 1 readiness — six forcing questions that pressure-test any multi-framework compliance program.
tags: [compliance, readiness, multi-framework, audit-calendar, certification, evidence-pool, cross-framework, management-review, grc]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/compliance-readiness
---

# Compliance Readiness — Forcing Questions

Six questions before any new-framework commitment, audit-cycle planning, or certification readiness sign-off. Run before: new framework, annual audit-calendar finalization, Stage 1 sign-off, management review. Smell signals: evidence-collection effort grew 50%+ YoY, or an audit produced >15% critical findings.

## The six questions

1. **Have you named every applicable framework?** Run a framework selector against the company profile. Forgetting one means rebuilding the audit program later. Watch industry overlays (financial: NYDFS, FINMA; healthcare: HIPAA, ISO 13485; AI: ISO 42001 + EU AI Act).
2. **Where do frameworks overlap, and what's the reuse leverage?** Single evidence → N controls is the cornerstone of efficiency. HIGH = same evidence, MEDIUM = existing + overlay, LOW = new artefact. Without overlap analysis you collect the same access-review records 3×.
3. **Who owns each artefact, and what's the reuse-leverage score?** Build HIGH-leverage artefacts (≥5 mappings) first. One accountable owner each. Stale evidence is an effective gap even if the artefact existed historically.
4. **What's the audit calendar, and is auditor independence respected?** Surveillance audits stacking the same week is a smell. Auditor cannot audit own work (Clause 9.2). Small teams: rotate + occasional external auditor.
5. **What does a mock audit produce, and is severity healthy?** Healthy: ≥40% observation, ≤15% critical. All-critical = destructive or genuinely failing; all-observation = audit too superficial.
6. **What's the management-review cadence across frameworks?** One integrated quarterly review (per Annex SL) covering all frameworks' Clause 9.3 inputs (risk-register changes, open NCs, audit findings, incidents, drift, KPIs → action items, resource decisions, scope adjustments) saves ~5× exec time vs separate reviews.

## Output

Decision being made (framework-set / audit-calendar / certification-readiness / evidence-consolidation) → framework set (applicable / binding / certifiable / missing dependencies) → cross-framework overlap (merged controls, high-leverage artefacts, top reuse) → evidence pool (catalog, high-leverage count, stale rate, unowned) → audit calendar (independence respected? conflicts?) → mock-audit results per framework → verdict 🟢 READY / 🟡 STAGE-2-CANDIDATE / 🔴 NOT-READY → top 3 actions with owners + dates.
