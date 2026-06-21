---
name: hubspot-lead-scoring
description: "Use when building a HubSpot lead scoring model — create separate Fit and Engagement scores in HubSpot's new Lead Scoring tool (the deprecated HubSpot Score property is frozen). Triggers: HubSpot lead scoring, Fit score, Engagement score, MQL threshold, score decay, prioritize leads, Marketing Hub scoring."
version: 1.0.0
license: MIT
tags: [hubspot, crm, lead-scoring, marketing-ops, segmentation, mql, saas, sales-ops]
source: https://github.com/TomGranot/hubspot-admin-skills/tree/main/skills/build-lead-scoring
derived_from: awesomeclaude
platforms: [hubspot]
prerequisites: [Super Admin, Marketing Hub Pro/Enterprise, ICP Tier property populated]
---

# Build HubSpot Lead Scoring Model

Create a two-score model in **Marketing > Lead Scoring**: a **Fit** score (ICP company fit + persona match) and an **Engagement** score (behavioral signals with time decay). Fit tells you WHO to talk to; Engagement tells you WHEN.

## Critical: old vs new
The old "HubSpot Score" property is **deprecated** — stopped being editable July 2025, stopped updating August 2025. Never reference it in workflows, lists, or reports. The new Lead Scoring tool supports score groups with max limits, engagement decay, separate Fit/Engagement types, and up to 5 scores per portal.

## Prerequisites
Super Admin; Marketing Hub Pro/Enterprise; ICP Tier property created and processed (run the ICP-tiers skill first); access to Marketing > Lead Scoring.

## Interview first
- Q1 valuable personas/titles (default: C-suite & VP highest, then Director, then Manager).
- Q2 engagement actions that matter (default: form submit +30, click +25, visit +20, open +15).
- Q3 negative signals (default: global unsubscribe -100, hard bounce -50, no activity 6+ mo -20, missing company -10).
- Q4 MQL threshold (default: Fit > 30 AND Engagement > 20).

## Execute — Fit score
Create score → type **Fit**, object **Contact**, descriptive name.
- **Group 1 — ICP company tier** (associated company property ICP Tier): Tier 1 +25..+35, Tier 2 +15..+25, Tier 3 +5..+15, Not ICP -10..-20.
- **Group 2 — persona/job title** (contains any of): C-suite +20..+30, VP +20..+30, Director +15..+25, Manager +10..+20, other relevant +5..+10. Customize titles to your buyer personas.
- **Group 3 — negative fit**: missing company -10, hard bounced -50, globally unsubscribed -100.
Set max ~100, save, turn ON.

## Execute — Engagement score
Create score → type **Engagement**, object **Contact**.
- Positive (with decay): opened email (last 30d) +15 monthly decay; clicked email +25 monthly; visited website (sessions>0) +20 quarterly; submitted form +30 quarterly.
- Negative: no email activity 6+ months -20.
Set max ~100, save, turn ON.

These point values are starting points — calibrate against real conversion data after 30 days.

## After state
Allow **4–6 hours** for async recalculation across the database (do not panic at initial zeros). Then in Contacts add both score columns; sort Fit descending and confirm top 20 are target personas at Tier 1/2 companies; sort ascending and confirm bottom are unsubscribed/bounced/Not ICP. Spot-check 3 random contacts by hand vs actual scores.

## Key learnings
- Two scores beat one — combining obscures both WHO and WHEN.
- Enable decay so a click from two years ago doesn't look like yesterday's.
- Limit of 5 scores per portal — reserve slots.
- Tune after 30 days on real conversion data; scoring is iterative.
- Negative signals matter as much as positive — heavy weights push dead contacts to the bottom.
- ICP Tier is the highest-leverage Fit input; without it Fit has no company signal.
- For lifecycle progression, build a separate workflow on a combined threshold (e.g. Fit>30 AND Engagement>20) — not part of the scoring model itself.
