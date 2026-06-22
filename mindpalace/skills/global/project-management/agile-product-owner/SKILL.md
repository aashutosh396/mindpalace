---
name: Agile Product Owner
description: Use when writing user stories, creating acceptance criteria, planning sprints, estimating story points, breaking down epics, or prioritizing a backlog — Scrum backlog and sprint execution toolkit with INVEST, Given-When-Then, and capacity math.
tags: [user-story, acceptance-criteria, sprint-planning, story-points, epic, backlog, invest, given-when-then, velocity, scrum]
source: alirezarezvani/claude-skills
derived_from: product-team/agile-product-owner
---

# Agile Product Owner

Backlog management and sprint execution for product owners. Not for Kanban-only, waterfall, or SAFe/LeSS without adaptation.

## User Story Generation

1. Identify persona → 2. Define action/capability → 3. Articulate benefit → 4. Write Given-When-Then AC → 5. Estimate points (Fibonacci) → 6. Validate against INVEST → 7. Add to backlog with priority. **Validate:** passes all INVEST; AC are testable.

Template: `As a [persona], I want to [action], So that [benefit].`

Story types: Feature (`...I want to X so that Y`), Improvement (`...I need X to Y`), Bug Fix (`...I expect X when Y`), Enabler (`As a developer, I need to [technical task] to enable [capability]`).

## Acceptance Criteria

Given-When-Then: `Given [precondition], When [action], Then [expected outcome].`
Each story should cover: Happy Path, Validation, Error Handling, Performance, Accessibility.

Minimum AC by size: 1-2 pts → 3-4 criteria; 3-5 pts → 4-6; 8 pts → 5-8; 13+ pts → **split the story**.

## Epic Breakdown

1. Define epic scope/success → 2. Identify personas → 3. List capabilities per persona → 4. Group into stories → 5. Validate each ≤8 pts → 6. Identify dependencies → 7. Sequence for incremental delivery. **Validate:** each story delivers standalone value; total covers epic.

Splitting techniques: by workflow step (linear process), by persona (multiple user types), by data type (multiple inputs), by operation (CRUD), happy-path-first (risk reduction).

## Sprint Planning

1. Calculate capacity (velocity × availability) → 2. Review sprint goal → 3. Select from prioritized backlog → 4. Fill to 80-85% (committed) → 5. Add 10-15% stretch → 6. Identify dependencies/risks → 7. Break complex stories into tasks. **Validate:** committed ≤85% capacity; all stories have AC.

Capacity = Average Velocity × Availability Factor. Factors: full sprint 1.0; one member out 50% → 0.9; holiday → 0.8; multiple out → 0.7.

## Backlog Prioritization

Priority levels: Critical (blocking/security/data-loss → immediate), High (core → this sprint), Medium (next 2-3 sprints), Low (backlog).

Weighted factors: Business Value 40% · User Impact 30% · Risk/Dependencies 15% · Effort 15%.

INVEST validation before adding to sprint:
- **I**ndependent — no blocking dependencies
- **N**egotiable — multiple approaches possible
- **V**aluable — clear benefit in the "so that"
- **E**stimable — understood well enough to size
- **S**mall — ≤8 story points
- **T**estable — clear acceptance criteria

## Sprint Metrics

Velocity (points/sprint, stable ±10%); Commitment Reliability (completed/committed >85%); Scope Change (<10%); Carryover (<15%).

## Definition of Done

Code complete + peer reviewed; unit tests passing; AC verified; docs updated; deployed to staging; PO accepted; no critical bugs.
