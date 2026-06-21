---
name: hubspot-delete-no-email-contacts
description: "Use when deleting HubSpot contacts that have no email address — fully automated discovery and batch archive via the CRM Search and Batch Archive APIs, with a safety threshold and 90-day recovery window. Triggers: HubSpot delete no-email contacts, contacts without email, reduce billed contact count, batch archive contacts, CRM dead weight cleanup."
version: 1.0.0
license: MIT
tags: [hubspot, crm, data-hygiene, cleanup, billing, marketing-ops, batch-api, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/delete-no-email-contacts
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [HubSpot token with contacts.read + contacts.write]
---

# Delete HubSpot Contacts With No Email

Contacts without an email cannot receive marketing emails, sequences, or transactional messages, and inflate the billed contact count. Identify and delete them via the API. Fully scriptable (Search + Batch Archive APIs).

## Stages (Plan → Before → Execute → After)

### 1. Plan
Confirm with the user:
- **Root cause** — is any integration (CRM sync, form tool, import) intentionally creating contacts without email? Fix the inflow first.
- **Threshold** — default safety abort at 500 contacts; raise in the execute script if the user expects more.
- **Recovery** — deleted contacts are recoverable for **90 days** via Settings > Data Management > Deleted Objects.

### 2. Before state
Count contacts with no email using the Search API with operator `NOT_HAS_PROPERTY` on `email` (a "never set" check — empty string is not the same as absent). Save the baseline count for comparison.

### 3. Execute
- Page through all matching contact IDs.
- Abort if the count exceeds the safety threshold and the user hasn't raised it.
- Delete using the **Batch Archive API** (`POST /crm/v3/objects/contacts/batch/archive`), 100 IDs per call, respecting the 100 req / 10 sec rate limit (backoff on 429).
- Keep a log of deleted IDs for the audit trail.

### 4. After state
Re-run the Before count — it should be 0 (or near 0 if new no-email contacts arrived). Remind the user of the 90-day recovery window and to fix the inflow if a root-cause integration was identified.

## Notes
- Use `NOT_HAS_PROPERTY`, not `EQ ""` — HubSpot stores "never set" as the property being absent.
- Archive (not hard delete) — recoverable for 90 days, so this is reversible within that window.
- Fully scriptable; no UI step required.
