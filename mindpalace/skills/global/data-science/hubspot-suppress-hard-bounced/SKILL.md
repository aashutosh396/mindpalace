---
name: hubspot-suppress-hard-bounced
description: "Use when suppressing hard-bounced HubSpot contacts to protect sender reputation — API discovers and audits hard bounces and builds an active list, then the UI sets non-marketing status (hs_marketable_status is read-only via API). Triggers: HubSpot hard bounce, suppress bounced contacts, sender reputation, hs_email_hard_bounce_reason_enum, non-marketing contact, email deliverability cleanup."
version: 1.0.0
license: MIT
tags: [hubspot, crm, deliverability, email, data-hygiene, marketing-ops, bounces, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/suppress-hard-bounced
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [HubSpot token with contacts.read + lists.read/write, Super/Marketing Admin for UI step]
---

# Suppress Hard-Bounced HubSpot Contacts

Hard-bounced contacts have permanently undeliverable addresses; every send fails and damages sender reputation. Identify them, export an audit trail, create a dynamic monitoring list, and guide manual suppression in the UI.

## Key constraint
`hs_marketable_status` is **read-only via API** — you cannot set a contact non-marketing programmatically. API does discovery/audit/list creation; the actual suppression happens in the HubSpot UI (or via a workflow triggered by a custom flag property).

## Stages (Plan → Before → Execute → After)

### 1. Plan
Confirm with the user: suppressed contacts stay in the CRM but stop counting toward marketing-contact billing and can't receive marketing email; non-marketing changes apply at the **next billing cycle** (no immediate savings); ask whether to make a separate review list for 3+ bounce contacts (deletion candidates).

### 2. Before state
Paginated Search API on `hs_email_hard_bounce_reason_enum` with operator `HAS_PROPERTY`; pull email, name, reason, `hs_email_bounce`, lifecyclestage, `hs_marketable_status`, createdate. Output: total count, bounce-reason breakdown, marketing-status split (already non-marketing vs still marketing), 3+ bounce count, and a CSV at `data/audit-logs/hard-bounced-contacts.csv`.

Bounce reasons to explain: OTHER (generic/server config), UNKNOWN_USER (mailbox doesn't exist — most common), SPAM (flagged — investigate content), POLICY (server policy), MAILBOX_FULL (soft escalated to hard).

### 3. Execute (hybrid)
- **3a API** — create a DYNAMIC active list "CLEANUP: Hard Bounced Contacts" via `POST /crm/v3/lists` (objectTypeId `0-1`, filter `hs_email_hard_bounce_reason_enum` IS_KNOWN). Handle 409 = already exists.
- **3b UI** — open the list → select all → More → Set marketing contact status → Set as non-marketing → Confirm.
- **3c optional** — create "REVIEW: 3+ Bounces - Possible Delete" (`hs_email_bounce` > 2).

### 4. After state
Re-run the Before query; `still_marketing` should be ~0 (minor drift if new bounces occurred). Always re-measure before acting — counts drift over time.

## Safety
CSV audit trail before any action; DYNAMIC list auto-captures new bounces (keep it permanently); suppression is non-destructive (status change, not delete); 3+ bounce review list, never auto-delete; confirm with user before list creation / UI actions.

## Gotchas
- Property is `hs_email_hard_bounce_reason_enum` (the `_enum` suffix is required).
- Full automation workaround: set a custom flag via API, then a workflow flips marketing status on that flag.
- `hs_email_bounce` is a string that may be decimal (`"3.0"`) — cast `int(float(value))`.
- Run monthly (or via workflow); the dynamic list keeps catching new bounces.
