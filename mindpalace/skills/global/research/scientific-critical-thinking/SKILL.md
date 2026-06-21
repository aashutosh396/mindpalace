---
name: scientific-critical-thinking
description: "Use when evaluating the quality of a claim, study, or piece of evidence — judging methodology, spotting bias and confounding, and grading how much to trust a conclusion. Triggers: 'is this study valid', 'evaluate this evidence', 'how strong is this claim', 'what's wrong with this methodology', 'identify the bias', 'is this causal or correlational', 'confounding', 'p-hacking', 'GRADE', 'risk of bias', 'should I trust this finding', 'critique this research'. Helps make evidence-based decisions."
version: 1.0.0
license: MIT
tags: [critical-thinking, evidence-evaluation, bias-detection, confounding, methodology-critique, grade, validity, decision-making, research-quality]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/scientific-critical-thinking
derived_from: awesomeclaude
---

# Critical Evidence Evaluation

## What it does
A systematic process for judging how much to trust a claim or study: assess methodology and design, test the validity of causal claims, surface biases and confounders, and grade evidence quality using established frameworks (GRADE, Cochrane Risk of Bias). Use it to decide whether a finding should change a decision — applies to research papers, vendor claims, internal experiment readouts, blog statistics, and "data says X" assertions.

## When to use
- Evaluating a study's methodology and design
- Assessing statistical validity and evidence quality
- Identifying bias and confounding
- Reviewing claims and conclusions before acting on them
- Systematic reviews / weighing conflicting evidence
- Applying GRADE or risk-of-bias assessment

## 1. Methodology critique
**Study design:** Is the design appropriate for the question? Can it support the causal claim being made? Are comparison groups adequate? (experimental vs quasi-experimental vs observational — observational supports association, not causation.)

**Four validities:**
- **Internal** — can we trust the causal inference? Check randomization, confounding control, selection bias, attrition.
- **External** — do results generalize? Sample representativeness, setting realism, match to target application.
- **Construct** — do the measures capture what's claimed? Validation, operational definitions, proxy vs direct.
- **Statistical conclusion** — adequate power, assumptions met, correct test.

**Control & blinding:** proper randomization (sequence + allocation concealment), blinding of participants/providers/assessors, appropriate controls (placebo/active/none).

**Measurement:** validated, reliable, objective where possible, standardized outcome assessment.

## 2. Bias detection
- **Researcher/cognitive:** confirmation bias, HARKing (hypothesizing after results), publication bias, cherry-picking. Look for pre-registration and analysis-plan transparency.
- **Selection:** sampling bias, volunteer bias, differential attrition, survivorship bias. Check participant-flow diagrams and baseline balance.
- **Measurement:** observer bias, recall bias, social desirability, instrument bias. Look for blinding and validation.
- **Analysis:** p-hacking, outcome switching, selective reporting. Check whether all planned analyses are reported.

## 3. Grading evidence quality (GRADE-style)
Start from the design (RCT = high, observational = low), then adjust:
- **Downgrade** for: risk of bias, inconsistency across studies, indirectness, imprecision (wide CIs / small n), publication bias.
- **Upgrade** (observational only) for: large effect, dose-response, all plausible confounding would reduce the observed effect.
Land on a confidence rating: High / Moderate / Low / Very Low.

## How to deliver a critique
1. State the claim precisely and whether the evidence is causal or associational.
2. Walk the four validities; name the single biggest threat.
3. List concrete biases present and their likely direction of distortion.
4. Give an overall evidence grade with a one-line justification.
5. Say what it would take to trust the claim more (the missing study/control).

Be specific and fair: identify the strongest version of the work, then its real weaknesses — not nitpicks.
