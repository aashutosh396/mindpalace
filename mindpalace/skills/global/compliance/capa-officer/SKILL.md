---
name: CAPA Officer
description: Use when running CAPA investigations, root cause analysis (5-Why, fishbone, FMEA), corrective/preventive action planning, effectiveness verification, or CAPA program metrics — medical device QMS (ISO 13485 §8.5).
tags: [capa, root-cause-analysis, 5-why, fishbone, corrective-action, preventive-action, effectiveness-verification, nonconformance, iso-13485, capa-metrics]
source: alirezarezvani/claude-skills
derived_from: ra-qm-team/skills/capa-officer
---

Corrective and Preventive Action management: systematic root cause analysis, action implementation, effectiveness verification. Authority = ISO 13485:2016 §8.5.2 (corrective) / §8.5.3 (preventive) under the FDA QMSR (legacy QSR 820.100 retired 2026-02-02 — cite the ISO clauses).

## Investigation workflow
Document trigger with objective evidence → assess significance + CAPA necessity → form team → collect data → select RCA method → identify root cause(s) with evidence → develop actions. *Validation: root cause explains all symptoms; if eliminated, problem won't recur.*

**CAPA necessity:** safety complaint = yes · quality complaint = evaluate · major audit finding = yes · minor = recommended · recurring NC (3+ times) = yes · isolated NC = evaluate · external audit finding = yes.
**Team by severity:** Critical = CAPA officer + process owner + QA mgr + SME + mgmt rep · Major = + SME · Minor = officer + process owner.

## RCA method selection
Safety-critical/reliability → Fault Tree. Human error suspected → Human Factors. Else by factor count: 1-2 (linear) → 5-Why · 3-6 (systemic) → Fishbone · unknown/proactive → FMEA.

**5-Why** (linear single-cause): state problem → 5× "why did [prior cause] occur? BECAUSE [cause] + EVIDENCE" → root cause. Each level needs objective evidence.
**Fishbone 6M:** Man (training, fatigue) · Machine (calibration, wear) · Method (procedures) · Material (specs, suppliers) · Measurement (instrument error) · Mother Nature (environment).

**Root cause validation:** verifiable with evidence · elimination prevents recurrence · within org control · explains all symptoms · no significant causes left unaddressed.

## Action planning
Containment (24-72h, stop impact) → Correction (1-2wk, fix the occurrence) → Corrective (30-90d, eliminate root cause) → Preventive (60-120d, extend to similar processes). Each action: type, responsible person, due date, resources, measurable success criteria, verification method. *Validation: actions directly address root cause; criteria measurable.*
Effectiveness indicators — scope addresses root cause (not symptoms) · specific deliverables · aggressive-but-achievable timeline · resources allocated · permanent (not temporary fix).

## Effectiveness verification
Wait the implementation period (Critical 30d / Major 60d / Minor 90d) → collect post-implementation data → compare to baseline → evaluate vs success criteria → verify no recurrence → document → determine effectiveness.
Decision: recurrence during verification → INEFFECTIVE (re-investigate). No recurrence + all criteria met → EFFECTIVE (close). Criteria gap: minor → extend/accept with justification · significant → INEFFECTIVE (revise actions).
Methods: data trend analysis (quantifiable) · process audit (procedure compliance) · record review · testing/inspection · interview/observation.

## Metrics
CAPA cycle time <60d avg · overdue rate <10% · first-time effectiveness >90% · recurrence rate <5% · 100% root causes validated. Aging: 0-30d on track · 31-60 monitor · 61-90 escalate · >90 management intervention.

## Decision discipline
Tools structure investigations and track status — they don't certify closure. Effectiveness/closure decisions are signed by the named CAPA owner + Quality; route reportability questions (21 CFR 803 MDR, recall 21 CFR 806) to Regulatory Affairs.
