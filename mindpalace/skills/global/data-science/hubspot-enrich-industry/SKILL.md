---
name: hubspot-enrich-industry
description: "Use when backfilling contact-level industry in HubSpot from associated company records via a workflow — enables industry/vertical segmentation when company Industry is well-populated but contact Industry is empty. Triggers: HubSpot enrich industry, copy industry from company, contact industry missing, vertical segmentation, industry_name property, B2B segmentation enrichment."
version: 1.0.0
license: MIT
tags: [hubspot, crm, enrichment, segmentation, data-quality, marketing-ops, workflows, saas]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/enrich-industry
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [Marketing or Sales Hub Pro for Workflows, company Industry populated]
---

# Enrich HubSpot Contact Industry from Company

Copy industry from company records to associated contacts. In typical B2B CRMs companies have industry at 80–90% while contacts have almost none — this workflow bridges the gap so you can segment email by vertical and feed ICP tiers + lead scoring.

## Prerequisites
Marketing Hub or Sales Hub Pro (Workflows); run company-name enrichment first (it may create new company associations); access to Settings > Properties.

## Plan
Verify the contact Industry property exists and is compatible with company Industry → audit enrichable contacts → build the copy workflow → verify.

## Before state
### Check property compatibility (most important pre-step)
Contacts may have **two** industry properties: `industry` and `industry_name`. Find ALL industry-related contact properties, determine which one your lists/reports/workflows actually use, and confirm compatibility with the company Industry property:
- Both **dropdown select**: option values must match exactly (same spelling and case).
- Contact property is **single-line text**: accepts any value (safest).
- Unsure → use single-line text to avoid copy failures.

If no contact Industry property exists, create one (Contact, group Contact information, label Industry) as a dropdown copying all company Industry values, or single-line text.

### Audit opportunity
Count contacts missing industry with `NOT_HAS_PROPERTY` on `industry`. Build a list (Contact Industry unknown AND Associated company Industry known) to estimate how many will actually be enriched.

## Execute — create the workflow
Automation > Workflows > Create > Contact-based > Blank. Name `AUTO-ENRICH: Copy Industry from Company`.
- **Enrollment trigger**: Contact Industry **is unknown** AND Associated company Industry **is known**.
- **Re-enrollment**: ON (so contacts later associated with a company also get enriched).
- **Action**: Copy property FROM Company Industry TO Contact Industry.
- Activate → Yes, enroll existing contacts.
No delay needed (the trigger already confirms the company has industry data).

## After state
Wait 1–2 hours, then re-count contacts missing industry (should jump from near-zero to many enriched; the enrichment list should be ~0). Spot-check 20+ contacts vs their company. Check workflow history for failures — most common is a dropdown value mismatch.

## Key learnings
- Two industry properties can exist — write to the authoritative one or lists/reports won't see the data.
- Dropdown matching is exact and case-sensitive ("Healthcare" != "healthcare").
- Consider an "Industry Group" property to consolidate overlapping values for cleaner segmentation.
- This never overwrites existing values (trigger requires "is unknown").
- Text field works but loses exact dropdown filtering.
- Run after company-name enrichment (it creates new associations → more eligible contacts).
- Clone the company-name enrichment workflow and swap property references to save time.
