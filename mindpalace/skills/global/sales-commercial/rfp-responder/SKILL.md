---
name: RFP / RFI / RFQ Responder
description: Use when an RFP, RFI, RFQ, or security questionnaire arrives and needs a structured response — parses requirements (MANDATORY/WEIGHTED/NICE-TO-HAVE), builds a Shipley proof-point matrix per requirement, articulates win-themes, estimates winrate, and gives a bid/partner-bid/no-bid verdict.
tags: [commercial, rfp, rfi, rfq, shipley, win-theme, proof-points, bid-management, winrate, security-questionnaire]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/rfp-responder
---

# RFP / RFI / RFQ Responder

Structured buyer-dictated response. **Surfaces GAPs explicitly — never invents claims.** Leadership decides close-the-gap / partner-bid / no-bid. (Not free-form proposal narrative, not post-award contract redline.)

## Workflow
1. **Parse the RFP** — extract every requirement, tag MANDATORY / WEIGHTED / NICE-TO-HAVE by cue words (must/shall = MANDATORY; should/weighted scores = WEIGHTED; may/preferred/desired = NICE-TO-HAVE). Capture section structure, scoring criteria, deadline, format constraints. Surface mandatory disqualifiers (FedRAMP/HIPAA/ISO 27001/SOC 2/data residency) on Day 1.
2. **Score fit per requirement** — proof-point matrix: STRONG / PARTIAL / GAP, each backed by a verifiable source (case study, certification, customer reference, technical attestation, benchmark). Unsourced claims become GAPs. Run a GAP audit.
3. **Apply win-theme strategy** — Shipley method: 3-5 themes that ladder across requirements (buyer-side "why us over the incumbent on the criteria they named"). A theme appearing in <2 requirements is decorative — flag it.
4. **Estimate winrate** — Shipley-derived factor model (fit %, incumbent strength, relationship, decision-criteria alignment, late-entry, competitor count, deal size) → estimate + confidence band + factor breakdown. Profile-tuned (government rewards compliance; enterprise SaaS rewards references; healthcare rewards regulatory/security depth).
5. **Decide** — BID / PARTNER-BID / NO-BID. **Estimate <20% triggers automatic no-bid.** Skill doesn't commit pursuit budget — leadership does.

## Anti-patterns
- Inventing a proof point to fill a GAP (hard-rule violation).
- Responding to every RFP without a bid/no-bid gate.
- Generic response with no win-theme (could be sent verbatim by any competitor).
- Missing a mandatory disqualifier late.
- Answering the question YOU wanted asked — answer what they asked, in their words, in their order.
- No compliance matrix mapping each requirement to a response section + page.
- Late-entry without acknowledging the relationship deficit.
- Treating WEIGHTED like MANDATORY (depth on high-weight items, not uniform mediocrity).

## Forcing questions (one at a time, recommended + canon)
1. STRONG/PARTIAL/GAP split on MANDATORY? → STRONG ≥70% before bidding; any GAP on MANDATORY = close or no-bid. (Shipley *Proposal Guide v6*)
2. Incumbent, and how strong? → strong incumbent drops base winrate ~30%; need a named displacement trigger. (Forrester)
3. Entered before or after the RFP issued? → late-entry drops ~15% and signals the RFP was scoped to someone else. (Searcy & DeVries)
4. 3-5 win-themes, each threading ≥2 requirements? → single-requirement themes are decorative. (Shipley *Capture Guide*)
5. Every claim has a verifiable source? → case study / cert / reference / attestation / benchmark. (APMP BoK)
6. Bid/no-bid threshold committed BEFORE seeing this RFP? → pre-commit (e.g., winrate ≥25%, STRONG ≥70%, named champion). (Bain)
7. What does the buyer's evaluation team score on? → weight effort proportionally; if undisclosed, ask. (Strategic Proposals)
