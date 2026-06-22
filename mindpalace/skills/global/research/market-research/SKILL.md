---
name: Market Research Methodology
description: Use for upstream market-research methodology — sizing TAM/SAM/SOM both top-down AND bottoms-up (never a single unsourced number), planning survey sample size with finite-population correction and per-segment minimums, and scoring segments against Kotler's criteria.
tags: [market-research, tam-sam-som, market-sizing, survey, sampling, segmentation, competitive-intelligence, kotler]
source: alirezarezvani/claude-skills
derived_from: research-ops/skills/market-research
---

# Market Research Methodology

The discipline is **method + assumptions**: a TAM is never a single number, a survey is never powered only in aggregate, a segment is never a demographic slice. (This is evidence-building, NOT live-campaign analytics/attribution/demand-gen.)

## Workflow
1. **Write the brief** — objective, the decision this informs, sizing approach, sampling plan, assumptions register.
2. **Size the market** — compute TAM/SAM/SOM by BOTH top-down and bottoms-up, side by side; report divergence; flag failed triangulation. Reconcile the delta before quoting anything. Profile by b2b-saas/consumer/enterprise/marketplace/hardware/services.
3. **Plan the survey** — sample size from confidence + margin of error + expected proportion (use conservative p=0.5 / max variance unless you have a prior), with finite-population correction AND per-segment minimums. Fund the per-segment floors, not just overall n.
4. **Score segments** — against Kotler's 5 criteria (measurable, substantial, accessible, differentiable, actionable); enforce a substantiality + accessibility gate; drop slices too small or unreachable.
5. **Assemble the evidence pack** — every number carries its method + assumptions + confidence.

## Anti-patterns
- A single TAM number with no method — always triangulate top-down vs bottoms-up.
- Spurious precision ("$3.7142B" implies false confidence) — size to the decision's tolerance.
- Powering only the total — each reported segment needs its own sample floor.
- Leading / double-barreled survey questions — pre-test wording against the bias literature.
- Calling a demographic slice a segment — it must be substantial AND accessible.

## Forcing questions (one at a time, recommended + canon)
1. TAM top-down or bottoms-up — computed both ways? → both; reconcile delta. (Bessemer/a16z; Fermi)
2. What decision will this size drive, at what precision? → size to tolerance. (Gartner/Forrester conventions)
3. Target MoE + confidence — clears per segment, not just overall? → power each reported segment. (Cochran; AAPOR)
4. Survey questions free of leading/double-barreled wording? → pre-test; cite the bias source. (Schuman & Presser; Dillman)
5. Segments pass measurable/substantial/accessible/actionable — or just slices? → drop failures. (Kotler)

Competitive intelligence follows the SCIP code of ethics — no misrepresentation, no protected information.
