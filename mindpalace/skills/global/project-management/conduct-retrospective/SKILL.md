---
name: conduct-retrospective
description: "Use at the end of a sprint, phase, or milestone (or after a notable success/failure) to run a structured, evidence-backed retrospective — what went well, what needs improvement, and owned improvement actions with due dates. Triggers: retrospective, retro, sprint review, lessons learned, continuous improvement."
version: 1.0.0
license: MIT
tags: [retrospective, agile, scrum, continuous-improvement, lessons-learned, sprint, project-management]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/conduct-retrospective
derived_from: awesomeclaude
---

# Conduct a Retrospective

Turn raw project data into evidence-backed learnings with specific actions, owners, and due dates.

## When to Use

- End of a sprint, phase, or milestone
- After a significant incident, failure, or success
- Quarterly review of ongoing processes
- Before starting a similar project (lessons learned)

## Inputs

- Required: period under review (sprint number, date range, milestone)
- Optional: status reports, velocity/completion data, previous retro actions, team feedback

## Procedure

### Step 1 — Gather data
Read STATUS-REPORT-*, SPRINT-PLAN, BACKLOG, and previous RETRO-* files. Extract planned vs completed, velocity trend, blockers and resolution time, unplanned work, and open actions from the last retro.

### Step 2 — What went well (3-5 items)
Each item gets evidence (metric, example, artifact). Focus on practices to continue ("daily standups kept blockers visible"), not just outcomes ("we delivered on time").

### Step 3 — What needs improvement (3-5 items)
Be specific and factual with stated impact. Not "estimation was off" but "3 of 5 items exceeded estimates by >50%, adding 8 unplanned days". If the team claims all is fine, compare planned vs actual — gaps reveal issues.

### Step 4 — Improvement actions (2-4)
For each improvement, create an action that is specific, owned (one accountable person), time-bound (within 1-2 sprints), and verifiable (success criteria). Apply the "how would you verify this was done?" test.

### Step 5 — Review previous actions and write report
Check prior actions for closure; flag recurring issues (same item in 3+ retros) for escalation. Write `RETRO-[YYYY-MM-DD].md` with: Period Summary (metrics), What Went Well, What Needs Improvement, Improvement Actions, Previous Action Review.

## Validation

- [ ] Date-stamped retro file created
- [ ] Period summary has quantitative metrics
- [ ] 3-5 evidence-backed positives and improvements
- [ ] Actions have owners, due dates, success criteria
- [ ] Previous actions reviewed; recurring issues flagged

## Common Pitfalls

- Blame game — review processes, not people.
- Actions without follow-through (always review prior actions first).
- Too many actions — 2-4 focused beats 10 vague.
- No evidence — attach data, not feelings.
- Skipping positives — celebrating wins reinforces good practice.

## Related

- manage-backlog — improvement actions feed back into the backlog
- conduct-post-mortem — incident-specific variant
