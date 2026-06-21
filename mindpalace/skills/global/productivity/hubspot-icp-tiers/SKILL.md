---
name: hubspot-icp-tiers
description: "Use when classifying HubSpot companies into Ideal Customer Profile tiers — create an ICP Tier custom property via API and build 4 classification workflows by industry + employee count with size-based demotion. Triggers: HubSpot ICP, ideal customer profile tiers, firmographic segmentation, company tiering, ICP workflow, buyer tier property."
version: 1.0.0
license: MIT
tags: [hubspot, crm, icp, segmentation, firmographics, marketing-ops, workflows, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/create-icp-tiers
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [Super Admin, Workflows access, company Industry + Number of Employees populated 80%+]
---

# Create HubSpot ICP Tier Property & Workflows

Classify every company into an ICP tier from firmographics (industry + employee count). Create a custom dropdown property and 4 workflows that continuously classify companies. ICP Tier is also the top input to lead scoring.

## Prerequisites
Super Admin; Automation > Workflows (Marketing Hub Pro+); run data enrichment first so Industry and Number of Employees are 80%+ populated (missing data → Not ICP, intentional and conservative).

## Interview first
- Q1 industries defining your ideal customer (no default — business-specific).
- Q2 employee-count ranges per tier (default: T1 1,000+, T2 200–999, T3 50–199, Not ICP <50).
- Q3 other firmographic criteria (revenue, geo, tech, funding — default none).

## Define tiers + size-based demotion
A company in a higher-tier industry but below that tier's employee threshold is **demoted one tier down**, never dropped to Not ICP for size alone. Only sub-50-employee companies, or non-ICP industries, become Not ICP.

## Execute
### Step 1 — Create the property (API)
Pick a name (`company_segment`/`buyer_tier`/`icp_tier`), object `companies`, type `enumeration`/`select`, group `companyinformation`, four options: `tier_1_primary`, `tier_2_secondary`, `tier_3_tertiary`, `not_icp`. Use `properties.core_api.create(...)`. (UI alt: Settings > Properties > Company > Create > Dropdown.)

### Step 2 — Build 4 classification workflows
Company-based, **filter-based triggers** (AND logic), three options to build:
1. **Manual UI build** — most reliable, full control.
2. **HubSpot Breeze AI** — paste a per-tier prompt, but Breeze creates **event-based (OR) triggers** instead of filter-based (AND) — you MUST manually rebuild triggers; Breeze also can't reliably do "is unknown" guards, re-enrollment, or multi-group OR-between/AND-within logic needed for demotion.
3. **Claude Chrome extension** — drives the builder UI directly; usually more accurate for the multi-group filter logic.

Specs:
- **Tier 1**: employees >= T1 threshold AND industry in primary verticals → set Tier 1. Re-enroll ON. Include ALL industry label variants (e.g. "Manufacturing" / "Industrial Automation" / "Machinery").
- **Tier 2**: Group A (employees >= T2 AND secondary industries AND ICP Tier unknown); Group B (T2 <= employees <= T1-1 AND primary industries AND unknown) → set Tier 2.
- **Tier 3**: multiple groups for tertiary at threshold + primary/secondary demoted below T2, each AND ICP Tier unknown → set Tier 3.
- **Not ICP (catch-all)**: trigger ICP Tier is unknown → **delay 30–90 min** (let tiered workflows run first) → set Not ICP. Re-enroll ON.

### Step 3 — Staggered activation
Activate Tier 1 → wait 3–10 min → Tier 2 → wait → Tier 3 → wait → Not ICP. Prevents race conditions; the "unknown" guards + Not-ICP delay add protection.

## After state
Wait 2–4 hours, then verify: 0 companies with ICP Tier unknown; distribution sanity (Tier 1 smallest, Not ICP largest); spot-check Tier 1, demotions, and Not ICP; review workflow histories for failures.

## Key learnings
- Breeze creates the wrong trigger type — always verify/rebuild triggers manually.
- Staggered activation + "unknown" guards prevent overwrites; the Not-ICP delay is critical.
- Size-based demotion is the core pattern — never lose ICP-industry companies to size.
- Missing-data companies fall to Not ICP; later enrichment + re-enrollment auto-reclassifies them.
- Don't manually edit ICP Tier; use a separate override property for exceptions.
- Include all industry label variants present in your actual data.
