---
name: hubspot-merge-duplicate-companies
description: "Use when finding and merging duplicate HubSpot company records — API discovers duplicates by domain and name and exports prioritized audit CSVs; merging is manual UI or third-party tools (HubSpot has no bulk merge API). Triggers: HubSpot duplicate companies, merge companies, deduplicate CRM, company dedup, duplicate domain, Dedupely Insycle, irreversible merge."
version: 1.0.0
license: MIT
tags: [hubspot, crm, deduplication, data-quality, companies, marketing-ops, sales-ops, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/merge-duplicate-companies
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [HubSpot token with companies.read, Super Admin for UI merge]
---

# Merge Duplicate HubSpot Companies

Duplicate company records fragment contacts, deals, and history, corrupting reporting and breaking associations. Identify duplicates by domain and name, export prioritized audit CSVs, and guide merging.

## Key constraints
- **No bulk merge API** — merging happens one pair at a time in the UI or via third-party tools. The API is for discovery, analysis, and audit trail only.
- **Merging is irreversible** — records cannot be un-merged; property values from the deleted record may be lost if both had the field filled.
- **HubSpot's built-in Duplicates tool is plan-tier dependent** — check Settings > Data Management > Duplicates availability first.

## Stages (Plan → Before → Execute → After)

### 1. Plan
Confirm intentional duplicates (e.g. regional offices) and exclude them. Stress irreversibility. Recommend prioritization: Customer-stage companies first, then Opportunity, then the rest. Budget 2–4 hours for critical dupes, 8–12 hours total.

### 2. Before state
Fetch all companies via `GET /crm/v3/objects/companies` with pagination (properties: name, domain, lifecyclestage, num_associated_contacts, num_associated_deals, hubspot_owner_id, createdate). Group duplicates by **domain** (lowercase + strip) and by **name** (lowercase). Report unique dup groups + affected records + top offenders for each, and export `data/audit-logs/duplicate-companies-by-domain.csv` and `...-by-name.csv` with a `duplicate_count` column. Present findings; wait for explicit confirmation.

### 3. Execute (manual)
- **Option A — built-in Duplicates tool** (if available): Settings > Data Management > Duplicates > Companies; for each suggested pair pick the surviving "primary" (most contacts/deals, recent activity, has owner, most complete) and Merge; process ~50 pairs/batch. Prioritize Customer → Opportunity → rest.
- **Option B — manual search-and-merge** for big offenders (4+): search by name, open the winner, Actions > Merge, select duplicate, choose property values, Merge; repeat.
- **Option C — third-party tools** for scale: Dedupely, Insycle, Koalify.
- **Prevention**: Settings > Data Management > Companies → enable "Create and associate companies with contacts" with unique identifier = company domain (domain-based matching beats name-based).

### 4. After state
Re-run the Before analysis; dup domain/name group counts should drop and top offenders resolve. Spot-check: search top offenders (should show 1 record each), open merged records (contacts + deals from both originals present), check the Duplicates tool count.

## Gotchas
- No bulk merge API; merging is irreversible (skip when in doubt).
- Property conflicts: primary record's value wins — review phone/address/industry before confirming.
- List companies with `GET .../companies` + pagination, not Search (faster for full export).
- Always normalize domains (lowercase + strip); `Example.com` == `example.com`.
- Name-based dupes have higher false positives (e.g. "State University") — domain is more reliable.
- Spot-check that contacts from both records appear under the survivor after merge.
