---
name: Product Manager Toolkit
description: Use when prioritizing features, synthesizing customer interviews, writing PRDs, or developing product strategy — RICE prioritization, interview analysis, PRD templates, and discovery-to-delivery workflows.
tags: [product-management, rice, prioritization, prd, customer-discovery, interview-analysis, jtbd, roadmap, pm]
source: alirezarezvani/claude-skills
derived_from: product-team/product-manager-toolkit
---

# Product Manager Toolkit

Frameworks for modern PM, discovery to delivery.

## Feature Prioritization

Flow: Gather → Score → Analyze → Plan → Validate → Execute.

1. **Gather** — customer feedback, sales requests, tech debt, strategic initiatives.
2. **Score with RICE** — `(Reach × Impact × Confidence) / Effort`.
3. **Analyze portfolio** — quick wins vs big bets distribution; avoid all-XL concentration; strategic alignment gaps.
4. **Generate roadmap** — quarterly capacity allocation, dependency ID, comms plan.
5. **Validate** — compare top priorities vs strategic goals; sensitivity analysis (estimates wrong by 2×?); stakeholder review for blind spots; check missing dependencies; validate effort with engineering.
6. **Execute & iterate** — track actual vs estimated effort; revisit quarterly.

## Customer Discovery

Flow: Plan → Recruit → Interview → Analyze → Synthesize → Validate.

- 5-8 interviews per segment; mix power + churned users.
- Semi-structured; focus on problems not solutions; minimal in-interview notes.
- **Analyze** extracts: pain points (severity), feature requests (priority), JTBD patterns, sentiment/themes, notable quotes.
- **Synthesize** — group pain points across interviews; 3+ mentions = pattern; map to Opportunity Solution Tree; prioritize by frequency × severity.
- **Validate solutions** before building — hypotheses, low-fi prototypes, measure actual behavior vs stated preference.

## PRD Development

Flow: Scope → Draft → Review → Refine → Approve → Track.

Template by context: Standard PRD (complex/cross-team, 6-8wk); One-Page (simple/single-team, 2-4wk); Feature Brief (exploration, 1wk); Agile Epic (sprint-based, ongoing).

Draft: lead with problem statement; define success metrics upfront; explicitly state out-of-scope; include wireframes. Review with engineering (feasibility), design (UX gaps), sales (market), support (ops impact). After launch: actual vs target metrics, user feedback, document learnings, update estimation data.

## Common Pitfalls

Solution-first (start with problem); analysis paralysis (time-box research); feature factory (define success metrics before building); ignoring tech debt (reserve 20% capacity); stakeholder surprise (weekly async + monthly demos); metric theater (tie metrics to user value).

## Best Practices

- **PRDs** — problem before solution; clear success metrics; explicit out-of-scope; visuals; tech detail in appendix; version control.
- **Prioritization** — mix quick wins + strategic bets; consider opportunity cost; account for dependencies; buffer 20%; revisit quarterly.
- **Discovery** — ask "why" 5×; focus on past behavior not future intent; avoid leading questions; interview in natural environment; watch emotional reactions (pain = opportunity); validate qual with quant.
