---
name: conduct-post-mortem
description: "Use when running a blameless post-mortem after a production incident, service degradation, outage, near-miss, or recurring issue — reconstruct the timeline, find contributing factors (Five Whys), and produce trackable action items focused on systemic fixes, not blame."
version: 1.0.0
license: MIT
tags: [post-mortem, incident-review, blameless, timeline, action-items, root-cause, sre, reliability]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/conduct-post-mortem
derived_from: awesomeclaude
---

# Conduct Post-Mortem

Lead a blameless post-mortem to learn from incidents and improve resilience. Focus on systems, not people.

## When to Use

- After any production incident or service degradation
- Following a near-miss or close call
- When investigating recurring issues
- To share systemic learnings across teams

## Inputs

- Required: incident details (start/end time, services affected, severity)
- Required: access to logs, metrics, alerts for the incident window
- Optional: runbook used, communication logs (Slack, PagerDuty)

## Procedure

### Step 1 — Collect raw data
Export logs, metrics, and alert history covering the full incident window. Note any gaps; if retention is short, fix retention for next time. Ensure all sources log in UTC with NTP sync.

### Step 2 — Build the timeline
Create a minute-by-minute table: `Time (UTC) | Event | Source | Actor`. Capture first symptom, alert fire, page, ack, diagnosis, mitigation, resolution. A clear sequence is the backbone of the report.

### Step 3 — Identify contributing factors
Use Five Whys or fishbone. Separate:
- Immediate cause (the proximate trigger)
- Contributing factors (monitoring gap, testing gap, runbook gap, capacity planning)
- Systemic issues (process gaps that allowed the failure)

If analysis stops at "an engineer made a mistake", dig deeper — ask what allowed the mistake.

### Step 4 — Generate action items
Each item gets an ID, owner, deadline, and priority. Make them concrete and trackable: "Add metric X to dashboard Y by date Z", never "improve monitoring".

### Step 5 — Write and distribute the report
Template sections: Summary, Impact (requests/customers/revenue), Root Cause, Timeline, Contributing Factors, Action Items, What Went Well, Lessons Learned, Prevention. Use blameless language (what/why, not who). Distribute within 48 hours — stale insights lose value.

### Step 6 — Track action items
Create tickets/issues from each action item with owner and deadline. Review open items weekly in standup or retro until closed. Schedule a follow-up review ~4 weeks out.

## Validation

- [ ] Timeline complete and chronologically accurate
- [ ] Multiple contributing factors identified (not just one)
- [ ] Action items have owners, deadlines, priorities
- [ ] Report uses blameless language
- [ ] Distributed to stakeholders within 48 hours
- [ ] Action items tracked in ticketing system
- [ ] Follow-up review scheduled

## Common Pitfalls

- Blame culture: "who" language instead of "what/why".
- Shallow analysis: stopping at the first cause.
- Vague action items that never get done.
- No follow-through: items created but never reviewed.
- Hiding incidents, which kills learning.

## Related

- write-incident-runbook — runbooks referenced during incidents
