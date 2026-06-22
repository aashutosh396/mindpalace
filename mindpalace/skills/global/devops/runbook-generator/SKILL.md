---
name: Runbook Generator
description: Use when a service has no runbook, runbooks are inconsistent across teams, or you're onboarding on-call before a production launch — generate baseline deploy/incident/maintenance/rollback runbooks.
tags: [runbook, on-call, incident-response, sre, devops, rollback, deployment, operations, escalation]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/runbook-generator
---

# Runbook Generator

Generate operational runbooks fast from a service name, then customize for deployment, incident response, maintenance, and rollback workflows.

## When to use
- Service has no runbook and needs a baseline immediately
- Runbooks are inconsistent across teams
- On-call onboarding needs standardized ops docs
- Repeatable scaffolding for new services

## Standard sections to generate
- **Overview** — what the service does, owner, escalation contacts
- **Start / Stop / Restart** — copy-pasteable commands
- **Health checks** — how to verify the service is up after each critical step
- **Deployment** — step-by-step with expected output per step
- **Rollback** — rollback triggers (when to roll back) + rollback commands
- **Incident response** — symptom → diagnosis → action playbooks, structured escalation placeholders
- **Maintenance** — routine tasks, cadence

## Recommended workflow
1. Generate the skeleton from the service name.
2. Fill in service-specific commands and URLs.
3. Add verification checks and explicit rollback triggers.
4. Dry-run in staging.
5. Store the runbook in version control next to the service code.

## Best practices
1. Keep every command copy-pasteable.
2. Add a health check after every critical step.
3. Validate runbooks on a fixed review cadence — not only during incidents.
4. Update content after every incident/postmortem.

## Common pitfalls
- Missing rollback triggers or rollback commands
- Steps with no expected-output check
- Stale ownership/escalation contacts
- Runbooks never tested outside of incidents
