---
name: Clinical Study Design
description: Use when designing a prospective clinical study before submission — selecting/classifying endpoints (primary/key-secondary/exploratory with surrogate flagging), estimating sample size & power (means/proportions/survival), and scoring feasibility for a GO/REDESIGN/NO-GO phase gate.
tags: [clinical-research, study-design, endpoint, sample-size, statistical-power, phase-gate, biostatistics, ich-e9, survival]
source: alirezarezvani/claude-skills
derived_from: research-ops/skills/clinical-research
---

# Clinical Study Design

Prospective study DESIGN: endpoints, sample size/power, phase-gate feasibility. **Every output is an ESTIMATE with stated assumptions, routed to a named human owner** (clinician / biostatistician / regulatory). Never clinical fact; never a finished protocol; never a substitute for a biostatistician. (Regulatory submission — ISO 13485, EU MDR, FDA 510(k)/PMA/QSR — is a separate discipline.)

## Workflow
1. **Draft the synopsis** — objectives, design, population, endpoints, statistical-plan placeholder, owners-to-sign.
2. **Select the endpoint** — score candidates across 5 weighted dimensions (clinical relevance, measurability, regulatory acceptance, sensitivity-to-change, burden) → classify PRIMARY / KEY-SECONDARY / EXPLORATORY. Penalize unvalidated surrogates. If >1 primary, plan multiplicity control. Profile by drug/device/biologic/diagnostic/digital-therapeutic.
3. **Estimate sample size** — closed-form power for two-arm:
   - means → Cohen's d
   - proportions → normal approximation
   - survival → Schoenfeld events
   Inflate for dropout: n ÷ (1 − dropout). Trace the effect/difference/HR to a published or anchor-based MCID — never a convenience effect size.
4. **Score feasibility** — 0-100 across recruitment feasibility, endpoint readiness, statistical power, operational complexity, budget fit → GO / GO-WITH-CONDITIONS / REDESIGN / NO-GO + named owners who must sign.
5. **Route for sign-off** — assemble synopsis + estimates into the gate packet. It is a recommendation.

## Anti-patterns
- Presenting a power estimate as fact.
- Powering for a convenience effect size instead of a published/anchor-based MCID.
- Anchoring a primary endpoint on an unvalidated surrogate.
- Ignoring multiplicity (>1 primary needs pre-specified alpha allocation).
- Skipping dropout inflation.

## Forcing questions (one at a time, recommended + canon)
1. Primary endpoint clinical or surrogate — if surrogate, on FDA's validated table? → clinical unless validated. (FDA Surrogate Endpoint Table; BEST glossary)
2. What MCID are you powering for, and where did the number come from? → published/anchor-based, cited. (ICH E9; Cohen)
3. Dropout rate assumed, and is n inflated for it? → inflate by 1/(1−dropout). (Chow, Shao & Wang; ICH E9(R1))
4. Single or multiple primary — multiplicity control? → pre-specify alpha allocation. (FDA Multiple Endpoints 2022)
5. Who is the named biostatistician / medical monitor / regulatory owner signing? → name them now. (ICH E6(R2) GCP)

Sample-size formulas use normal approximations — first-pass estimates; a biostatistician produces the final justification (may use simulation/adaptive/exact methods).
