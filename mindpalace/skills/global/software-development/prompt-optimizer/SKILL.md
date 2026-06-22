---
name: Prompt Optimizer (EARS + domain theory)
description: Use when given a vague prompt or loose requirement and asked to make it precise — transforms ambiguous descriptions into structured, testable specifications via EARS syntax, domain-theory grounding, concrete examples, and a Role/Skills/Workflows prompt.
tags: [prompt-engineering, ears, requirements, specification, optimization, refine, testable, domain-theory]
source: daymade/claude-code-skills
derived_from: prompt-optimizer
---

Optimize vague prompts into precise, actionable specifications using EARS (Easy Approach to Requirements Syntax). Four-layer enhancement: EARS transformation → domain-theory grounding → example extraction → structured prompt generation.

## When to use
Vague feature requests ("build a dashboard"), requirements missing conditions/triggers/measurable outcomes, natural language needing testable specs, or explicit prompt-optimization requests.

## Six-step workflow
1. **Analyze original** — flag weaknesses: overly broad, missing triggers, ambiguous actions ("user-friendly"), no constraints.
2. **Apply EARS transformation** — five patterns:
   - Ubiquitous: `The system shall <action>`
   - Event-driven: `When <trigger>, the system shall <action>`
   - State-driven: `While <state>, the system shall <action>`
   - Conditional: `If <condition>, the system shall <action>`
   - Unwanted behavior: `If <condition>, the system shall prevent <unwanted action>`
   Checklist: make implicit conditions explicit; specify triggers/states; precise verbs (shall/must); measurable criteria ("within 30 minutes", "≥8 characters"); break compound into atomic statements; remove ambiguous language.
3. **Identify domain theories** — map to established frameworks: Productivity→GTD/Pomodoro/Eisenhower; Behavior change→BJ Fogg (B=MAT)/Atomic Habits; UX→Hick's/Fitts's/Gestalt; Security→Zero Trust/Defense in Depth/Privacy by Design. Pick 2-4 complementary, apply to specific features, cite for credibility.
4. **Extract concrete examples** — realistic, specific, varied (success/error/edge), testable. Real data ("Product: 'Laptop', Price: $999, Stock: 15"), not "Example 1".
5. **Generate enhanced prompt** using the framework:
   ```
   # Role  [specific expert role + domain expertise]
   ## Skills  [5-8 capabilities aligned with domain theories]
   ## Workflows  [step-by-step phases with inputs/outputs/decision points]
   ## Examples  [concrete, real data]
   ## Formats  [precise output specs: file types, structure, constraints, deliverable checklist]
   ```
   Quality: role specificity > generic; theory grounding explicit; actionable workflows; concrete examples; measurable formats.
6. **Present results** — original requirement + identified issues → EARS transformation → domain & theories → enhanced prompt → how-to-use guidance.

## Do / Don't
Do: one EARS statement per requirement; measurable criteria; error/edge cases; ground in theories; concrete data. Don't: vague language; assume implicit knowledge; mix multiple actions in one statement; use placeholders in examples.
