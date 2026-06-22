---
name: SOC 2 Type II Audit Prep Interrogation
description: Use before a SOC 2 Type II observation period begins, at a mid-period checkpoint, or pre-field-test (month 10) — six observation-period-disciplined forcing questions on TSC scope, control consistency, exceptions, evidence sampling, and the ISO 27001 cross-walk.
tags: [soc2, soc-2-type-ii, trust-services-criteria, observation-period, exception-log, evidence-tracking, iso-27001, aicpa, audit-readiness, compliance]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/soc2-audit-prep
---

# SOC 2 Type II Audit Prep — Forcing Questions

Six observation-period-disciplined questions. Run pre-observation (months 1-2), mid-period (month 6), pre-field-test (month 10), post-report, after scope change, or after a major in-period incident.

## The six questions

1. **What's the scope, and which TSC categories are in?** Security/Common Criteria (CC1-CC9) always required; others elective by customer ask — Availability (A1) for SLA SaaS, Processing Integrity (PI1) for transactional/financial, Confidentiality (C1) for proprietary data, Privacy (P1-P8) for personal data (overlaps GDPR). AICPA AT-C 205 system description complete + accurate + clear boundaries.
2. **Did any control skip a cycle during the observation period?** Type II requires consistent operation — a single skipped cycle is likely an exception. Quarterly controls: all 4 quarters; monthly: all months; continuous (logging): no gaps; annual (BCP, training): within period.
3. **Show change-management evidence for any control implemented mid-period.** Mid-period changes = high audit risk. New/modified/removed controls documented with change-management + rationale + effective date + impact on prior samples. Strategy: avoid mid-period changes, defer to next cycle.
4. **Where's the exception log, and what's the materiality assessment?** Real-time logging, not retroactive. Per exception: what/when/impact/remediation/owner. Audit-firm threshold typically 1-2 exceptions per control acceptable; 3+ = finding.
5. **Show sample evidence from each TSC criterion in the FIRST month.** Not the last week. Front-loaded evidence shows operational discipline; back-loaded (last 30 days) signals scrambling. Sample IDs reproducible from operational systems.
6. **What's the cross-walk to ISO 27001, and which evidence reuses?** ~75% control overlap — the canonical pair. Each shared artefact cited by both audits (one collection, two reports). Coordinate audit calendar; avoid duplicate evidence files.

## Output

Decision (scoping / pre-observation / observation-status / pre-field / report-response) → TSC scope → observation-period status (months elapsed, controls operated consistently %, cycle skips, mid-period changes documented?) → exception log (total, per-control max vs tolerance, material exceptions, remediation) → sample-evidence coverage by quarter → ISO 27001 cross-walk reuse (high-confidence overlap, shared artefacts, duplicate collection avoided %) → audit-firm readiness (scoping, AT-C 205 description, walkthrough rehearsal, sample prep) → verdict 🟢 ON-TRACK / 🟡 NEEDS-ATTENTION / 🔴 MATERIAL-RISK → top 3 actions with observation-period timing.
