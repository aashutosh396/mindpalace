---
name: NIH Grants Funding Intelligence
description: Use when a clinical researcher asks about NIH research funding ("grants for X", "find NIH funding for my research idea", "what grants match my research") — produces a strategic funding overview with institute mapping, mechanism recommendations, and a program-officer next step.
tags: [nih, grants, funding, r01, k-award, reporter, nosi, clinical-research, mechanism]
source: alirezarezvani/claude-skills
derived_from: research/grants (NIH Funding Intelligence)
---

# Grants — NIH Funding Intelligence

NIH-only scope (flag PCORI/DOD/VA/foundations as out of scope at intake). Output: editable .docx with positioning, institute mapping, targeted grant discovery, and strategy the researcher can share with a mentor.

## Phase 1: Intake (6 forcing questions, one at a time)
1. **Research idea** — 2-3 sentences (question + what's new + clinical relevance). Reject vague ("AI for healthcare").
2. **Career stage** — pre-doc / postdoc / early-career / independent / senior PI. Filters mechanism (F→trainee, K→early, R→independent).
3. **Preliminary data** — none / pilot / strong / validated. Drives mechanism budget scale.
4. **Environment** — R01-eligible / mid-tier / resource-constrained / industry-collaborative. Affects scope realism + R15 eligibility.
5. **Submission posture** — new / resubmission (A1) / exploring. Resubmission needs reviewer-response guidance.
6. **Known institute targets** — list (NCI/NHLBI/NIMH...) or "no preference — find them".

## Phase 2A: Positioning (5 sequential Consensus searches, 1 q/sec)
Established (what's known) → Stakes (mortality/burden/cost) → Current approaches (standard of care) → Adjacent methods → Gaps (limitations/future directions). Extract 2-3 quotable findings per facet. Draft Significance/Innovation: "the field established X (refs), but Y remains unanswered (refs)".

## Phase 2B: Institute Mapping + Grant Discovery (RePORTER, POST-only via curl)
Compute fiscal-year window at runtime (current FY + 3 prior; federal FY starts Oct 1). Never hardcode years.
- **Narrow (AND) search** — direct overlap: `advanced_text_search {operator: AND, search_field: all, search_text: "<term1> <term2>"}` against `https://api.reporter.nih.gov/v2/projects/search`.
- **Broad (OR) search** — adjacent work, synonyms.
- **Tally** `agency_ic_admin` → top-3 institutes; `study_section` → top-2 sections.
- **NOSI discovery** — parse `NOT-*` numbers; fetch `https://grants.nih.gov/grants/guide/notice-files/NOT-<IC>-<YR>-<N>.html`. On fail: log + continue.

## Mechanism Matching (scope-aware)
Career stage **+** project scope **+** prelim data — never stage alone. No data → R03/R21; strong prelim → R01/U01.

## DOCX (9 sections)
Executive Summary → Research Positioning (gap quotes + narrative) → Target Institutes (ranking table) → Grant Opportunities (NOSI callout + top-3 FOAs) → Funded Overlap (top-5 projects, differentiation) → Study Sections → Strategic Recommendations + **mandatory program-officer recommendation** + submission timeline (+reviewer-response if resubmission) → References → Audit Log.

**Submission dates:** R01/R21/R03 = Feb/Jun/Oct 5; K = Feb/Jun/Oct 12; F31/F32 = Apr/Aug/Dec 8.

**Mandatory program-officer rec (Section 7, never skip):** contact PO at top institute; prepare 1-page specific aims + CV + 3 fit questions; email subject "Pre-application inquiry: <topic>".

## Agent Integrity Rules
Sequential Consensus calls (1+ s pause). Count queries sent / shown / cited separately. Cite only this-session results; training knowledge tagged + excluded. Retry once after 3s; stop after 3 consecutive failures. Audit Log section mandatory.

## Anti-Patterns
Parallelizing Consensus calls; using web_fetch for RePORTER (POST-only); hardcoded fiscal years; mechanism from career stage alone; padding thin facets with training knowledge; skipping audit log or program-officer rec; fabricating NOSI details on fetch failure.
