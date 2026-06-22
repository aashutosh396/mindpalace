---
name: UX Researcher & Designer
description: Use when conducting user research, creating personas, mapping user journeys, planning usability tests, or synthesizing interview findings — data-driven personas, journey maps, and research synthesis frameworks.
tags: [ux-research, persona, journey-map, usability-test, research-synthesis, empathy-map, user-research, ux]
source: alirezarezvani/claude-skills
derived_from: product-team/ux-researcher-designer
---

# UX Researcher & Designer

Generate personas from research, map journeys, plan usability tests, synthesize findings into actionable recommendations.

## Workflow 1 — Generate Persona

From user data (analytics/surveys/interviews) generate a research-backed persona with: archetype, demographics, psychographics, behaviors, needs/goals, frustrations (with frequency counts), scenarios, design implications, data points (sample size + confidence). Archetypes: power_user (daily, 10+ features → efficiency/customization), casual_user (weekly, 3-5 features → simplicity/guidance), business_user (work context → collaboration/reporting), mobile_first (→ touch/offline/speed). **Validate** by showing to 3-5 real users ("Does this sound like you?") and cross-checking support tickets + analytics.

## Workflow 2 — Journey Map

Define scope (persona, goal, start trigger, success criteria, timeframe). Gather from interviews ("walk me through…"), session recordings, funnel analytics, support tickets. Map stages (B2B SaaS: Awareness → Evaluation → Onboarding → Adoption → Advocacy). Per stage fill: Actions, Touchpoints, Emotions (1-5), Pain Points, Opportunities. Priority Score = Frequency × Severity × Solvability.

## Workflow 3 — Usability Test

Turn vague goals into testable questions ("Is it easy?" → "Can users complete checkout in <3 min?"). Select method: moderated remote (5-8, 45-60min, deep insight); unmoderated remote (10-20, 15-20min, quick validation); guerrilla (3-5, 5-10min, rapid). Design tasks as scenarios (SCENARIO/GOAL/SUCCESS), progression warm-up → core → secondary → edge → free exploration. Success metrics: completion >80%, time <2× expected, error <15%, satisfaction >4/5. Moderator guide: think-aloud, non-leading prompts, post-task questions.

## Workflow 4 — Synthesize Research

1. **Code data** — tag `[GOAL]`, `[PAIN]`, `[BEHAVIOR]`, `[CONTEXT]`, `[QUOTE]`. 2. **Cluster** similar patterns. 3. **Calculate segment sizes** (% + viability). 4. **Extract findings** — finding statement, evidence, frequency (X/Y participants), business impact, recommendation. 5. **Prioritize** by Frequency × Severity × Breadth × Solvability.

## Reference Tables

- **Method by question** — "what do users do?" analytics/observation (100+ events); "why?" interviews (8-15); "how well?" usability test (5-8); "what prefer?" survey/A-B (50+); "what feel?" diary/interviews (10-15).
- **Persona confidence** — 5-10 users Low (exploratory); 11-30 Medium (directional); 31+ High (production).
- **Usability severity** — 4 Critical (prevents completion, fix now); 3 Major (significant difficulty, fix before release); 2 Minor (hesitation); 1 Cosmetic.

## Validation Checklists

- **Persona** — ≥20 users, ≥2 data sources, actionable goals, frequency-counted frustrations, confidence stated.
- **Journey** — scope defined, real data not assumptions, all layers filled, pain points per stage, opportunities prioritized.
- **Usability test** — testable questions, realistic-scenario tasks, 5+ participants/design, success metrics, severity ratings.
- **Synthesis** — consistent coding, patterns on 3+ data points, findings include evidence, actionable recommendations, justified priorities.
