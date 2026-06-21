---
name: logic-toolkit
description: "Use when you say 'is this sound', 'check my reasoning', 'find the flaw', 'fix this argument', 'find contradictions', 'map the dependencies', 'map the constraints', or want logical analysis of an argument, plan, spec, or system. Routes to logic-check, argument validation, consistency check, causality mapping, constraint mapping, or logic-fixer."
version: 1.0.0
license: MIT
tags: [logic, reasoning, argument-validation, fallacies, consistency, causality, constraints, critical-thinking]
source: https://github.com/human-avatar/skills-for-humanity/tree/main/skills/s4h-logic
derived_from: awesomeclaude
---

# Logic Toolkit

Applies logical analysis to arguments, plans, specs, reasoning, and systems. Confirm the argument and what's at stake in one sentence, then route.

## Which tool fits

| You need to... | Tool |
|---|---|
| Fast, comprehensive logic report | Logic Check |
| Validate whether premises support a conclusion | Argument Validation |
| Find internal contradictions in a document/spec | Consistency Check |
| Map causal relationships and dependencies | Causality Mapping |
| Map what's actually negotiable vs fixed | Constraint Mapping |
| Repair broken reasoning, not just diagnose | Logic Fixer |

When unclear → Logic Check (surfaces which deeper tool is needed).

## Logic Check

One-pass complete assessment: (1) Premises — stated clearly, are they true? (2) Inference — do conclusions follow? (3) Fallacies — which informal fallacies present? (4) Hidden assumptions — what unstated premises does it rely on? (5) Verdict — sound, or specifically what's wrong.
**Output:** Five-section assessment with a sound / unsound verdict and specific diagnosis.

## Argument Validation

Identify structure: premises → conclusion. Test each premise (true? assumed without justification?). Test the inference (do premises entail the conclusion, or is there a gap?). Identify fallacies. Distinguish deductive validity (structure holds) from soundness (premises also true).
**Output:** Argument map, validity assessment, soundness assessment, fallacies, and the specific repair needed.

## Consistency Check

Read for conflict, not comprehension. For each claim/requirement: does any other part contradict it? Can all requirements be satisfied simultaneously? Do edge cases expose hidden conflict? Incrementally-grown documents often hold contradictions no single author introduced.
**Output:** Contradictions inventory by severity (surface vs structural), with locations and resolutions.

## Causality Mapping

Build the chain: A causes B via [mechanism]; B enables/requires C. If X changes, what else must change? What are the causal prerequisites for the plan to work? Where are the dependencies that break everything downstream?
**Output:** Causal chain (text), key dependencies, critical path, and the assumptions the structure rests on.

## Constraint Mapping

Inventory all constraints, classify each as hard (physical/legal), soft (organizational/political), or assumed (may not be real). Find conflicts (requirements that can't coexist). Define the remaining solution space. Identify which constraints, if relaxed, most expand it.
**Output:** Constraint inventory by type, conflict map, solution-space definition, highest-value constraints to challenge.

## Logic Fixer

Diagnose the specific failure (false premise? broken inference? fallacy? circularity?), then repair: restate the argument in valid form with defensible premises and a conclusion that actually follows. If the conclusion can't be saved, state what conclusion IS supportable.
**Output:** Diagnosis of the failure(s); repaired valid+sound argument; or the supportable conclusion.
