---
name: hubspot-audit
description: "Use when running a HubSpot CRM database audit or health check — analyze contacts, companies, deals, deliverability, duplicates, owners, lists/workflows, and deal pipeline across a HubSpot portal, grade each dimension, and produce a prioritized cleanup report. Triggers: HubSpot audit, CRM health check, HubSpot cleanup onboarding, HubSpot private app token, hubspot-api-client."
version: 1.0.0
license: MIT
tags: [hubspot, crm, audit, data-quality, deliverability, marketing-ops, sales-ops, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/hubspot-audit
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [HubSpot private app API token, Python with hubspot-api-client]
---

# HubSpot CRM Database Audit

Run a full diagnostic of a HubSpot portal across eight dimensions, grade each, and produce a prioritized report with a concrete next-skills prescription.

## Setup
1. Get the API token. Check `.env` for `HUBSPOT_API_TOKEN`; if missing, ask the user for their private app token (`pat-na1-...`) and store it.
2. Install deps with uv: `uv pip install hubspot-api-client python-dotenv`.
3. `mkdir -p reports`.

## Audit dimensions (collect exact counts)
1. **Database size** — total contacts, companies, deals; marketing vs non-marketing contacts.
2. **Email deliverability** — hard bounced (`hs_email_hard_bounce_reason_enum` set), soft bounced, global unsubscribes (`hs_email_optout`), never-emailed (no `hs_email_last_send_date`), invalid email format, 3+ bounces.
3. **Data completeness** — missing email, company, industry, country/state, lifecyclestage, owner, jobtitle; companies missing domain/industry/geo.
4. **Engagement health** — last-activity distribution (30/90/180/365/365+/never), 90-day open & click rates, zero page views, zero form submissions.
5. **Duplicate analysis** — duplicate emails, companies sharing a `domain`, exact-name company dupes (API cannot fuzzy-match; flag for manual review).
6. **Owner health** — deactivated owners still assigned contacts/companies/deals; unowned contacts/companies.
7. **List & workflow health** — active vs static lists, empty lists, active workflows, workflows idle 90+ days, forms with zero submissions.
8. **Deal pipeline health** — deals missing `amount`/`closedate`, deals per stage, stale open deals (60+ days), average age by stage.

## API technical notes
- **Null checks**: use the `NOT_HAS_PROPERTY` operator — "never set" is stored as absent, not 0/empty.
- **Search API caps at 10,000 results**: segment by `createdate` ranges or another property and sum.
- **Deactivated owners**: Owners API needs `archived=True` to return them.
- **Rate limit**: 100 requests / 10 seconds — add delay or exponential backoff on 429.
- **Activity dating**: `hs_last_sales_activity_timestamp`, `notes_last_contacted`, `hs_email_last_open_date`, `hs_email_last_click_date`.
- **`hs_marketable_status`** is read-only via API.

## Script
Write `scripts/audit_portal.py` that loads the token, inits `HubSpot(access_token=...)`, runs each dimension sequentially (respecting rate limits), collects results into a dict, computes letter grades, renders markdown, and saves to `reports/hubspot-audit-{YYYY-MM-DD}.md`.

## Grading rubric
| Grade | Criteria (records affected) |
|---|---|
| A | < 5% |
| B | 5–15% |
| C | 15–30% |
| D | 30–50% |
| F | > 50% |

For non-percentage dimensions (e.g. Owner Health) use judgment based on affected count and business impact.

## Output
Report sections: Executive Summary (grade table + overall grade), Priority Recommendations (ranked by impact with effort + automation feasibility), Detailed Findings (one table per dimension), Next Steps.

## Skill prescription (do not just present findings)
For every finding scoring C or worse, map to the next skill and present an **ordered, numbered action list** grouped Immediate / Next / Later. Mapping:
- **Hygiene (first)**: no-email contacts, hard bounces, global unsubscribes, ghost contacts, duplicate companies, deactivated owners.
- **Enrichment (second)**: company name, industry, geo standardize/backfill, lifecycle stages, unowned contacts.
- **Segmentation & scoring (third)**: ICP tiers, lead scoring, smart lists.
- **Automation (fourth)**: new-contact hygiene, engagement suppression, lifecycle progression, bounce monitoring workflows.
- **Maintenance (last)**: cleanup lists/forms/workflows/dashboards/deals/properties.

If a finding has no matching skill, flag it clearly and offer to create one. End by suggesting `hubspot-implementation-plan` for the full phased plan.
