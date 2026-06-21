---
name: manage-backlog
description: "Use when creating or maintaining a product/project backlog — writing user stories with acceptance criteria, MoSCoW or value/effort prioritization, backlog grooming, splitting oversized items, and status tracking. Triggers: backlog, user story, acceptance criteria, grooming, prioritize, MoSCoW, story points, ready for sprint."
version: 1.0.0
license: MIT
tags: [backlog, user-stories, prioritization, grooming, moscow, agile, scrum, project-management]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/manage-backlog
derived_from: awesomeclaude
---

# Manage a Product Backlog

Create, prioritize, and maintain a backlog that is the single source of truth for what needs to be done. Works for agile or classic.

## When to Use

- Converting project scope into actionable items
- Ongoing grooming before sprint planning
- Re-prioritizing after stakeholder feedback or scope change
- Splitting oversized items; archiving completed/cancelled items

## Inputs

- Required: project scope (charter, WBS, or stakeholder input)
- Optional: existing BACKLOG.md, prioritization framework, estimation scale, sprint feedback

## Procedure

### Step 1 — Create or load structure
BACKLOG.md with a summary block (totals by status) and an item table: `ID | Title | Type | Priority | Estimate | Status | Sprint`.

### Step 2 — Write or refine items
User story: "As a [role], I want [capability] so that [benefit]". Each item needs a unique ID (B-NNN), imperative title, type, and at least 2 testable (binary pass/fail) acceptance criteria. Items without criteria stay Status: New and cannot enter a sprint.

### Step 3 — Prioritize
MoSCoW (default): Must / Should / Could / Won't. Or value/effort matrix (quick wins → big bets → fill-ins → money pits). Sort the backlog Must-first, by value within each band. Escalate Must-vs-Should disputes to the sponsor.

### Step 4 — Groom (split, estimate, refine)
For each item: split if estimate > 8 points (into 2-4 independently deliverable children), estimate on the chosen scale, refine vague criteria into testable conditions, and mark Ready when it has title + criteria + estimate + no blockers. Items that can't be estimated get a time-boxed Spike.

### Step 5 — Update summary and archive
Move Done/Cancelled items to an Archive section. Recount statuses and update the summary so counts match reality.

## Validation

- [ ] BACKLOG.md with standard structure
- [ ] Every item has unique ID, title, type, priority, status
- [ ] All Must/Should items have acceptance criteria
- [ ] Sorted by priority; no >8-point item left unsplit
- [ ] Summary accurate; Done/Cancelled archived

## Common Pitfalls

- No acceptance criteria (can't verify "done").
- Everything is Must — force-rank if >50% are Must.
- Zombie items lingering for months.
- Estimates without a reference item.
- Splitting into non-deliverable fragments.
- Backlog as a dumping ground; missing dependency notes.

## Related

- draft-project-charter — charter scope seeds the backlog
- conduct-retrospective — improvement actions feed back into the backlog
