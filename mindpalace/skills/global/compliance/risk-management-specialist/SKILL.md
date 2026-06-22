---
name: Risk Management Specialist (ISO 14971)
description: Use when running medical-device risk management — building the risk management plan, hazard/risk analysis (FMEA/FTA/HAZOP), risk evaluation against an acceptability matrix, risk control hierarchy, residual/benefit-risk, and post-production monitoring under ISO 14971:2019.
tags: [iso-14971, risk-management, fmea, fta, hazard-analysis, risk-matrix, benefit-risk, residual-risk, afap, medical-device, post-market]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/risk-management-specialist
---

# Risk Management Specialist (ISO 14971:2019)

Risk management across the medical-device lifecycle.

## 1. Risk management plan

Define scope (device, lifecycle stages, standards) → set acceptability criteria (P1-P5 probability, S1-S5 severity, risk matrix with thresholds) → assign responsibilities (lead, SMEs, approvers) → define verification methods + acceptance → plan production/post-production monitoring → approve → establish the risk management file.

5x5 matrix (P × S): Improbable→Frequent vs Negligible→Catastrophic, cells = Low / Medium / High / Unacceptable. Actions: Low = document + accept (still reduce); Medium/High = reduce AFAP, document why further reduction impossible; Unacceptable = design change mandatory.

> **EU MDR — AFAP not ALARP:** CE-marked devices must reduce risk *as far as possible* with NO economic weighing (MDR Annex I GSPR 1-4; EN ISO 14971:2019/A11:2021). ALARP (cost-benefit weighing) is not acceptable under EU MDR and ISO 14971:2019 removed it from normative text. If used outside the EU, flag the deviation.

## 2. Risk analysis

Define intended use + reasonably foreseeable misuse (indication, patient/user population, environment) → select methods (FMEA components, FTA system-level, HAZOP process deviations, Use Error Analysis interaction, PHA early phase) → identify hazards by category (electrical, mechanical, thermal, radiation, biological, chemical, software, use error, environment) → determine hazardous situations (event sequences, misuse, single-fault) → estimate P (P5 >10⁻³ … P1 <10⁻⁶) and S (S5 death … S1 negligible) → document in hazard worksheet.

## 3. Risk evaluation

Compute initial risk (P × S) → compare to criteria → per risk: Low = accept+document; Medium/High = reduce AFAP; Unacceptable = mandatory control → document rationale → flag benefit-risk where needed → compile summary. AFAP demonstration (EU): all control options considered per hierarchy, evidence further reduction infeasible, state-of-the-art comparison, stakeholder input. Economic considerations must NOT enter the acceptability decision. Benefit-risk required when residual stays high, no feasible reduction, novel device, or unacceptable risk with clinical benefit.

## 4. Risk control

Identify options → select per hierarchy: (1) inherent safety by design — highest, (2) protective measures in device, (3) information for safety — lowest → analyze for new hazards introduced → document in design requirements → implement → verification protocol (test / inspection / analysis / review) → execute + document → evaluate residual risk → confirm no unaddressed new hazards. New-hazard check: if control introduces a new hazard higher than original → reject the option; if controllable → add control.

## 5. Post-production

Information sources: complaints (continuous), service reports (monthly), vigilance/serious incidents (immediate), literature (quarterly), regulatory feedback (as received), PMCF (per plan). Review triggers: serious incident → immediate full review; new hazard → 30-day analysis update; trend increase → 60-day trend analysis; design change → impact assessment before implementation; standards update → gap analysis. Periodic review: file completeness + control effectiveness + benefit-risk annual; post-market info quarterly.

## Tool support

A risk-matrix calculator computes ISO 14971 5x5 levels and FMEA RPN (Risk Priority Number = Severity × Occurrence × Detection) for ranking.
