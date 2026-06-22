---
name: FDA QSR/QMSR Audit Prep Interrogation
description: Use before an annual internal QSR audit, pre-FDA-inspection readiness, a Form 483 response, an MDR-reportable decision, or a recall — six sample-driven forcing questions on 21 CFR 820 (QMSR, harmonized with ISO 13485 post-Feb 2026).
tags: [fda, qsr, qmsr, 21-cfr-820, form-483, mdr-reporting, dhr, capa, process-validation, inspection-readiness, medical-device]
source: alirezarezvani/claude-skills
derived_from: compliance-os/skills/fda-qsr-audit-prep
---

# FDA QSR/QMSR Audit Prep — Forcing Questions

Six sample-driven questions before any internal audit, FDA inspection, Form 483 response, or recall. Post-Feb 2026, 21 CFR 820 is substantially harmonized with ISO 13485.

## The six questions

1. **Show complaint files from last quarter — and the matching MDR reports.** (21 CFR 820.198 + 803 — most-cited inspection area.) Complaint log complete (who/what/when/device/batch), investigation closure timely, MDR decision tree applied (death OR serious injury OR malfunction-that-could-cause = MDR), 30-day timeline most reports / 5 days certain serious events, complaint trending feeds management review.
2. **When was process validation (IQ/OQ/PQ) last revalidated?** (820.75; cross-walks ISO 13485 §7.5.6.) Initial at process introduction; revalidate on process/equipment/material change or periodic schedule; statistical techniques per 820.250 where applicable.
3. **Show DHRs for products commercially distributed in last 2 years.** (820.180 — 2-year retention.) Each unit/lot/batch DHR includes dates + quantity made/released, acceptance records, primary ID label, device ID, control number. Sample stratified by product class; verify closeness to DHF.
4. **Show CAPAs from last 6 months with effectiveness verification.** (820.100 = ISO 13485 8.5.2.) Root cause depth (5 Why min), effectiveness = measurable evidence (not "we updated the procedure"), containment/correction/corrective-action distinction, closure approval, aging CAPAs >90 days flagged.
5. **Show labeling review for the most recent product launch.** (21 CFR 801 — FDA overlay not in ISO 13485.) Plus device-type 800-series overlays, UDI per 21 CFR 830, promotional materials accurate + non-misleading.
6. **If a Form 483 issued in last 3 years, show closure status.** Response within 15 working days; each observation has documented corrective + preventive action + timeline + effectiveness evidence. Warning Letters: separate response track + possible FDA meeting.

## Output

Decision (programme-plan / inspection-readiness / 483-response / MDR-decision / recall) → complaint+MDR posture → process-validation status (820.75) → DHR completeness (820.180) → CAPA health (820.100) → labeling (801) → Form 483/Warning Letter history + thematic pattern → ISO 13485 cross-walk (post-Feb 2026; FDA-specific overlays = labeling + complaint handling + MDR reporting + recall) → verdict 🟢 INSPECTION-READY / 🟡 GAPS / 🔴 NOT-READY → top 3 actions with FDA-cited timelines → outside-counsel flags (Warning Letter response, recall decisions, 510(k)/PMA strategy disputes).
