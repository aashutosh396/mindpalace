---
name: Scrum Master — Sprint Analytics & Coaching
description: Use when working on sprint planning, velocity forecasting, retrospectives, burndown, story points, blocker resolution, or agile team health from Jira-style sprint exports.
tags: [scrum, agile, sprint-planning, velocity, retrospective, monte-carlo, team-health, burndown, story-points, jira]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/scrum-master
---

# Scrum Master — Sprint Analytics & Coaching

Data-driven Scrum Mastery: probabilistic forecasting, multi-dimension health scoring, and team development. Input is sprint JSON (Jira-style export mapped to a common schema).

## Input schema
```json
{
  "team_info": {"name":"", "size":0, "scrum_master":""},
  "sprints": [{"sprint_number":0,"planned_points":0,"completed_points":0,
               "stories":[],"blockers":[],"ceremonies":{}}],
  "retrospectives": [{"sprint_number":0,"went_well":[],"to_improve":[],"action_items":[]}]
}
```

## Three analyses

**1. Velocity / Monte Carlo** — rolling averages + linear-regression trend + Monte Carlo simulation. Outputs: trend (improving/stable/declining), coefficient of variation (CV), 6-sprint forecast at 50/70/85/95% confidence, anomaly flags. Needs ≥3 sprints (6+ for significance). If <3, stop and ask for more data.

**2. Sprint health (0-100, 6 weighted dimensions)**:

| Dimension | Weight | Target |
|---|---|---|
| Commitment Reliability | 25% | >85% goals met |
| Scope Stability | 20% | <15% mid-sprint changes |
| Blocker Resolution | 15% | <3 days avg |
| Ceremony Engagement | 15% | >90% participation |
| Story Completion Distribution | 15% | high ratio fully-done |
| Velocity Predictability | 10% | CV <20% |

Needs 2+ sprints with ceremony + story data; report which dimensions can't be scored if data missing.

**3. Retrospective analysis** — action-item completion by priority/owner, recurring-theme persistence, team maturity (forming/storming/norming/performing), improvement-velocity trend. Needs 3+ retros with action-item tracking.

## Sprint workflows

**Planning** — run velocity analysis; use the 70% confidence interval as the commitment ceiling. Check Commitment Reliability + Scope Stability scores to calibrate PO negotiation. If CV >20%, give stakeholders ranges, not point estimates. Document capacity assumptions.

**Standup** — track participation; log each blocker with date opened; escalate any blocker unresolved after 2 days.

**Review** — present velocity trend + health score with the demo; capture scope-change requests as events for next scoring cycle.

**Retro** — run all three analyses first; open with the health score + top-flagged dimensions; cap new action items at ≤3 if completion rate <60%; assign owner + measurable criterion to each.

## Team development

Map maturity output to stage, then apply stage-specific facilitation:

| Stage | Focus |
|---|---|
| Forming | Structure, process education, trust |
| Storming | Conflict facilitation, psychological safety |
| Norming | Autonomy, process-ownership transfer |
| Performing | Challenge, innovation support |

Supplement with an anonymous psychological-safety pulse (Edmondson 7-point). If forming/storming, prioritize safety over process optimization. Re-run health scorer per sprint (target +5/quarter); escalate if scores plateau/regress 2 consecutive sprints.

## Key targets
Health >80/100 · Psych safety >4.0/5.0 · Velocity CV <20% · Commitment >85% · Scope changes <15% · Blocker resolution <3d · Ceremony engagement >90% · Retro action completion >70%.

## Limitations
<6 sprints reduces Monte Carlo confidence — always state intervals, not points. Missing fields suppress dimensions — report gaps. Metrics don't replace qualitative observation. Optimized for 5-9 member teams.
