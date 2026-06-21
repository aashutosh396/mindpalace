---
name: salesforce-developer
description: "Use when developing on Salesforce — Apex code, Lightning Web Components (LWC), SOQL/SOSL, triggers, batch jobs, platform events, integrations, governor limits, Salesforce DX + CI/CD. Triggers: Salesforce, Apex, Lightning Web Components, LWC, SOQL, SOSL, Visualforce, Salesforce DX, governor limits, triggers, platform events, CRM integration, Sales Cloud, Service Cloud."
version: 1.0.0
license: MIT
tags: [salesforce, apex, lwc, soql, triggers, platform-events, salesforce-dx, crm]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/salesforce-developer
derived_from: awesomeclaude
platforms: [salesforce]
---

# Salesforce Developer

Apex, LWC, and integrations on the Salesforce platform.

## When to use

Apex code + debugging; Lightning Web Components; SOQL/SOSL optimization; triggers, batch jobs, platform events; integrations; managing governor limits and bulk processing; Salesforce DX + CI/CD.

## Core workflow

1. **Analyze** — objects, relationships, automation already present (flows/triggers).
2. **Design** — bulkified, trigger-handler pattern; one trigger per object.
3. **Implement** — Apex services + LWC; SOQL outside loops.
4. **Bulk-safe** — batch Apex for large volumes; respect governor limits.
5. **Test** — Apex tests (75%+ coverage required to deploy); use test data factories.

## Key practices

- Bulkify everything: no SOQL/DML inside loops; collect then operate on collections.
- One trigger per object delegating to a handler class.
- Selective SOQL (indexed filters); `LIMIT`; avoid querying whole objects.
- Batch/Queueable Apex for large data; Platform Events for async decoupling.
- Security: enforce CRUD/FLS (`WITH SECURITY_ENFORCED`, `stripInaccessible`), no SOQL injection.
- Salesforce DX source-driven dev; scratch orgs; CI deploy.

## Constraints

MUST: bulkify (SOQL/DML out of loops); one trigger per object + handler; respect governor limits; 75%+ test coverage; enforce CRUD/FLS; selective queries.
MUST NOT: SOQL/DML inside loops; hardcode IDs; SOQL injection (use bind variables); skip bulk testing (200+ records); ignore governor limits; logic directly in trigger body.

## Output

1. Apex classes (bulkified) + trigger handler. 2. LWC components. 3. Apex test classes (75%+). 4. Brief note on governor-limit + security handling.

## Knowledge

Salesforce, Apex, LWC, Aura, SOQL/SOSL, triggers + handler pattern, Batch/Queueable/Schedulable Apex, Platform Events, governor limits, CRUD/FLS, WITH SECURITY_ENFORCED, Salesforce DX, scratch orgs.
