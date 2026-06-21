---
name: write-incident-runbook
description: "Use when creating or improving an incident runbook — diagnostic steps, resolution procedures, escalation paths, and communication templates for an alert or recurring incident. Triggers: runbook, on-call, MTTR, incident response, alert annotation, escalation, tribal knowledge to docs."
version: 1.0.0
license: MIT
tags: [runbook, incident-response, diagnostics, escalation, on-call, mttr, documentation, sre]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/write-incident-runbook
derived_from: awesomeclaude
---

# Write Incident Runbook

Create actionable runbooks that guide responders through diagnosis and resolution, reducing MTTR.

## When to Use

- Documenting response for a recurring alert or incident
- Standardizing response across an on-call rotation
- Reducing MTTR with clear diagnostic steps
- Onboarding new responders; migrating tribal knowledge to docs
- Linking alerts to resolution procedures

## Procedure

### Step 1 — Choose a template structure
Minimum sections: Overview / Severity / Symptoms, Diagnostic Steps, Resolution Steps, Escalation, Communication, Prevention, Related. Add Metadata (service, owner, on-call, last-updated) for SRE-grade runbooks. Start basic and iterate from real incident patterns.

### Step 2 — Document diagnostic procedures
Make each step specific with the actual query and an expected-vs-actual value:
1. Verify service health (health endpoint, `up{job=...}`)
2. Check error rate (5xx ratio, expect < 1%)
3. Analyze logs (recent errors, top messages)
4. Check resource utilization (CPU < 70%, memory, connection pool)
5. Review recent changes (deploys, commits, infra)
6. Examine dependencies (downstream health, DB/API latency)
Include a failure-pattern decision tree: service down vs error spike; started after deploy (rollback), gradual (leak), or sudden (traffic/dependency). Test every query before documenting it.

### Step 3 — Define resolution procedures
Document remediation with verification and rollback for each option:
1. Rollback deployment (fastest, post-deploy errors)
2. Scale up resources (CPU/memory, pool exhaustion)
3. Restart service (memory leak, stuck connections)
4. Feature flag / circuit breaker (specific feature or external dep)
5. Database remediation (kill slow queries, resize pool)
Universal verification checklist: error rate < 1%, P99 latency under threshold, throughput at baseline, healthy resources, healthy deps, user tests pass, no active alerts. Always include a rollback path so a fix can't trap responders in a worse state.

### Step 4 — Establish escalation paths
Define escalate-immediately criteria (customer outage > 15 min, error budget burn, data loss/security, no root cause in 20 min, mitigation failing). Five levels: primary on-call → secondary → team lead → incident commander → executive. Maintain a current contact directory (Slack, phone, PagerDuty) including external vendors. Never go silent — update every 15 min.

### Step 5 — Create communication templates
Pre-write internal updates (declaration, progress every 15-30 min, mitigation complete, resolution, false alarm) and external/status-page messages (initial, progress, resolution) plus a customer email template. Templates cut cognitive load during the incident.

### Step 6 — Link runbook to monitoring
Add `runbook_url`, `dashboard_url`, `incident_channel` annotations to alerts. Embed pre-filled diagnostic links (dashboard, error-rate query, recent logs, recent deploys). Ensure links work without VPN/SSO and test them quarterly.

## Validation

- [ ] Consistent template structure
- [ ] Diagnostics include specific queries + expected values
- [ ] Resolution steps actionable with rollback
- [ ] Escalation criteria and contacts current
- [ ] Communication templates for internal + external
- [ ] Linked from alerts and dashboards
- [ ] Tested in simulation or real incident; revision history tracked
- [ ] Accessible without auth (or cached offline)

## Common Pitfalls

- Too generic ("check the logs" with no query).
- Outdated commands/systems — review quarterly.
- No verification ("how to confirm it's fixed").
- Missing rollback procedures.
- Written for experts only — write for the least experienced person on rotation.
- No owner; hidden behind auth during an SSO outage.

## Related

- conduct-post-mortem — feeds new runbooks from incident findings
