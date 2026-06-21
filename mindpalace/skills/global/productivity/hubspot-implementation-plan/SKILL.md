---
name: hubspot-implementation-plan
description: "Use when turning a HubSpot audit into a phased cleanup roadmap — sequence prioritized CRM cleanup/enrichment/automation tasks into 5 phases with effort estimates, dependencies, and automation feasibility. Triggers: HubSpot implementation plan, CRM cleanup roadmap, HubSpot phased plan, after hubspot-audit, HubSpot workflow build options."
version: 1.0.0
license: MIT
tags: [hubspot, crm, planning, roadmap, marketing-ops, sales-ops, automation, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/hubspot-implementation-plan
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [Completed audit report from hubspot-audit]
---

# HubSpot Implementation Plan Generator

Read an audit report and produce a phased, prioritized cleanup/optimization roadmap with dependencies, effort, and automation feasibility per task.

## Prerequisites
A completed `reports/hubspot-audit-*.md`. If none exists, run `hubspot-audit` first.

## Steps
1. **Load the audit** — read the most recent `reports/hubspot-audit-*.md`; extract grades, counts, and priority recommendations. Skip/deprioritize any dimension graded A.
2. **Build the phased plan** — only include tasks justified by findings.

### Phase 1 — Immediate hygiene (week 1–2; billing/deliverability impact)
Delete no-email contacts (fully scriptable), suppress hard bounces / global unsubscribes / ghost contacts (hybrid), merge duplicate companies (scriptable), reassign deactivated-owner records (scriptable).
**Constraint:** `hs_marketable_status` is read-only via API. Suppression = hybrid: script sets a custom flag property, then a HubSpot workflow triggers on that flag to flip marketing status. Build that workflow in the UI first.

### Phase 2 — Data enrichment (week 3–4)
Enrich company name → industry (industry comes from company), standardize geo → backfill geo, fix lifecycle stages, assign unowned contacts.
**Constraint:** lifecycle stage is forward-only — to set an earlier stage, clear the property first, then set the target (two API calls).

### Phase 3 — Segmentation & scoring (week 4–6)
ICP tiers → lead scoring → smart lists → segment lists.
**Constraint:** the new Lead Scoring tool is UI-only (no API to configure scoring rules).

### Phase 4 — Automation (week 6–8)
New-contact hygiene, engagement suppression, lifecycle progression, bounce monitoring workflows.
**Constraint:** Workflows API v4 is beta/unstable — do not create workflows via API. Build each workflow via one of three options: (1) **Manual UI build** (most reliable); (2) **HubSpot Breeze AI** — generates a skeleton from a natural-language prompt but creates event-based (OR) triggers instead of filter-based (AND); you MUST manually fix triggers, and Breeze can't do "is unknown" branches, copy associated-object properties, or re-enrollment; (3) **Claude Chrome extension** — drives the workflow builder UI directly, often more accurate than Breeze for nested/multi-condition logic.

### Phase 5 — Ongoing maintenance
Weekly cleanup routine; monthly list/form/workflow cleanup + bounce review; quarterly dashboards/deals/properties cleanup + full audit.

3. **Dependency graph** — Phase 1 tasks are parallel; Phase 2 depends on Phase 1; within Phase 2 company-name→industry and geo-standardize→backfill; Phase 3 is a strict chain (ICP→scoring→smart lists→segments); Phase 4 can start after Phase 2; Phase 5 runs indefinitely.
4. **Effort summary** — sum hours by category: fully scriptable, hybrid, manual UI, ongoing.
5. **Technical constraints summary** — always include: (1) `hs_marketable_status` read-only; (2) Workflows API v4 beta; (3) lifecycle forward-only; (4) Search API 10K cap → segment & sum; (5) rate limit 100 req/10s → backoff on 429.

## Output
Save to `reports/implementation-plan-{YYYY-MM-DD}.md`: Executive Summary, one section per phase (each task with why / count from audit / automation type / skill / dependencies / est. time / status checkbox), Dependency Map, Technical Constraints, Effort Summary table, Tracking Checklist.

## Gaps
For findings with no matching skill, add a "Custom Skills Needed" section, offer to create each skill, and optionally contribute upstream.

## After running
Print the file path, highlight Phase 1 as immediate, remind the user to build the suppression workflow in the UI before hybrid tasks, and suggest starting with delete-no-email-contacts.
