---
name: hubspot-quarterly-cleanup
description: "Use when running a recurring HubSpot CRM health review — quarterly (or monthly) audit of list health, bounce trends, data quality, scoring calibration, engagement, and property cleanup, with quarter-over-quarter trend comparison. Triggers: HubSpot quarterly cleanup, CRM data drift, scoring calibration, recurring CRM audit, quarter-over-quarter CRM report."
version: 1.0.0
license: MIT
tags: [hubspot, crm, maintenance, data-quality, audit, marketing-ops, scoring, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/quarterly-database-cleanup
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [HubSpot API token, Python hubspot-api-client]
---

# HubSpot Quarterly Database Cleanup

A structured recurring audit that catches data drift before it becomes a crisis. Run at the start of each quarter (or monthly for large/fast-growing databases). Read-only — action items are executed via their respective skills.

## Prerequisites
HubSpot API token in `.env`; Python with `hubspot-api-client` via uv; the previous period's report for trend comparison (optional on first run).

## Audit checklist
1. **List health** — active/static/unused (zero-member) lists; lists not referenced by any workflow or email; duplicate/overlapping lists.
2. **Bounce monitoring** — contacts with 1, 2, 3+ bounces; hard bounce rate vs last quarter; contacts flagged by the bounce-monitoring workflow.
3. **Data quality** — missing email/company/industry/country/lifecycle; compare % to last quarter; flag any completeness drop > 5 points.
4. **Scoring calibration** — lead score distribution; MQL conversion rate (are high scorers converting?); adjust the model if conversion is below 10% or above 50%.
5. **Engagement metrics** — active (engaged last 90 days) % of total; zombie (no engagement 6+ months) % of total; open/click rate trends.
6. **Property cleanup** — custom properties with zero populated records; properties unused in any list/workflow/form; test/temp properties to archive.

## Stages
1. **Before — baselines**: locate the previous report in `reports/`; run the audit logic for fresh numbers across all dimensions.
2. **Execute — deep review**: per checklist item, pull current metrics (reuse audit script patterns), compare to last quarter, flag anything that worsened by > 5 points, and document specific contacts/lists/properties needing action.
3. **After — report**: save `reports/quarterly-cleanup-{YYYY-Q#}.md` with a Summary trend table (last quarter vs this quarter vs change), Action Items (with owner + deadline), and Detailed Findings (one section per checklist item).
4. **Rollback**: none — read-only audit.

## Scheduling
Recurring reminder for the first Monday each quarter. Assign an owner per action item. Before starting a new audit, review whether last quarter's action items were completed.
