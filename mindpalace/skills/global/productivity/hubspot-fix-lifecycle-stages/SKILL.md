---
name: hubspot-fix-lifecycle-stages
description: "Use when fixing HubSpot lifecycle stages — backfill missing stages, correct disallowed values, and add prevention workflows, handling HubSpot's forward-only progression (clear then set). Triggers: HubSpot lifecycle stage, lifecyclestage missing, funnel reporting broken, stuck lifecycle stage, backfill lifecycle, lifecycle prevention workflow."
version: 1.0.0
license: MIT
tags: [hubspot, crm, lifecycle, data-quality, marketing-ops, workflows, reporting, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/fix-lifecycle-stages
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [Bulk edit permissions, Workflows access, Phase 1 hygiene done]
---

# Fix HubSpot Lifecycle Stages

Ensure every contact and company has an appropriate lifecycle stage: backfill missing, correct disallowed values, and add prevention workflows. Records without a stage are invisible in pipeline reports and excluded from stage-based workflows; lifecycle data is a prerequisite for lead scoring.

## Critical: forward-only progression
Default order: Subscriber > Lead > MQL > SQL > Opportunity > Customer > Evangelist. To move a record to an **earlier** stage you must (1) clear `lifecyclestage` (set to `""`), then (2) set the new value, as **two separate API calls**. A direct set to an earlier stage is **silently rejected** — no error, value unchanged. This is the most common gotcha.

```python
# WRONG — silently fails if current stage is later than target
update(contact_id, {"properties": {"lifecyclestage": "lead"}})
# CORRECT — clear, then set
update(contact_id, {"properties": {"lifecyclestage": ""}})
update(contact_id, {"properties": {"lifecyclestage": "lead"}})
```

## Plan
Audit missing/disallowed stages → define disallowed→correct mapping → fix disallowed (clear+set) → set missing with company context → fix stuck records → add prevention workflows → verify 100% coverage.

## Before state
Use `NOT_HAS_PROPERTY` to count contacts and companies with no stage; count contacts at each stage (`subscriber`, `lead`, `marketingqualifiedlead`, `salesqualifiedlead`, `opportunity`, `customer`, `evangelist`, `other`).

Define your disallowed stages and mappings (business-specific). Common examples: blank → Lead; Subscriber → Lead (if not newsletter-only); Other → Lead; Evangelist → Customer or Lead.

## Execute
1. **Fix disallowed stages** — for each disallowed value, paginate and apply clear-then-set (two calls; batch API 100/call where possible).
2. **Set missing contact stages with context** — contacts at Customer companies → Customer; at Opportunity companies → Opportunity; else → Lead. (Manual: build lists by associated-company stage and bulk edit.)
3. **Fix companies without a stage** — closed-won deals → Customer; open deals → Opportunity; else → Lead.
4. **Fix stuck records** — read current stage; if later than target, clear first, then set.
5. **Prevention workflows** — Contact-based: trigger `lifecyclestage` is unknown, re-enroll ON, action set to Lead, enroll existing. Company-based: same pattern. Optionally add disallowed-stage correction workflows.

## After state
Re-run the audit: missing-stage counts should be 0 for both contacts and companies; spot-check context-assigned records match their company stage.
