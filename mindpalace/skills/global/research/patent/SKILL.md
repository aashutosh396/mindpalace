---
name: Patent Prior-Art + Landscape Intelligence
description: Use when the user asks for patent searching or analysis ("prior art search for X", "freedom to operate for X", "patent landscape for X") — commits to one of five sub-use-cases, searches Google Patents/Espacenet/USPTO, extracts claims, and delivers a verdict. Search signal, not legal advice.
tags: [patent, prior-art, fto, freedom-to-operate, patent-landscape, novelty, cpc, ip]
source: alirezarezvani/claude-skills
derived_from: research/patent (Prior-Art + Landscape Intelligence)
---

# Patent — Prior-Art + Landscape Intelligence

Refuses to be a generic bucket: every run commits to one sub-use-case before searching. Out of scope: trademark, copyright, trade-secret. **Disclaimer: search signal, not legal advice — always recommend a patent attorney before filing/licensing.**

| Sub-use-case | Strategy | DOCX emphasis |
|---|---|---|
| Novelty | narrow + claims-text | closest art + claim differentiation |
| Freedom-to-operate (FTO) | broad + active patents only, jurisdiction-filtered | FTO flags + claim-by-claim risk |
| Competitive landscape | breadth + filer tally + CPC trends | filer map + hotspots |
| Acquisition diligence | specific assignee + portfolio + assignment chain | portfolio + ownership |
| Litigation prior-art | target patent + art before priority date | ranked knock-out candidates |

## Phase 1: Intake (6 forcing questions, one at a time)
1. **Invention** — 2-3 sentences (what it does + what's new). Reject generic.
2. **Sub-use-case** — pick one (above). Refuse to start without it.
3. **Jurisdictions** (only FTO/landscape/diligence) — US/EP/CN/JP/KR/PCT/worldwide.
4. **Known prior art** — patent number/paper or "none".
5. **Risk tolerance** (novelty/FTO) — strict (one close hit = abandon) vs signal-gathering.
6. **Attorney status** (novelty/FTO) — triggers the legal-disclaimer footer.

## Phase 3: Multi-Source Search (sequential, 1 q/sec across all sources)
Priority: Google Patents → Espacenet → USPTO PPS → Lens.org (BYOK, citation graph). Per-sub-use-case query patterns (novelty = narrow+broad+CPC-restricted; FTO = active+jurisdiction+priority<today; landscape = CPC tally + 10-yr trend; diligence = assignee+assignment chain; litigation = priority-date cutoff + adjacent claims).

## Phase 4: Claim Extraction + Scoring
Pull independent claim 1 (broadest) + key dependent claims per closest hit. Score relevance vs invention terminology. Verdict: NOVEL/POTENTIALLY/NOT NOVEL (novelty) or CLEAR/FLAGGED/HIGH RISK per jurisdiction (FTO).

## Phase 5: Citation Graph + Family Resolution
Lens.org (if BYOK): foundational patents (cited-by >50), recent high-cite, forward citations. Family resolution: group same-invention filings across jurisdictions by family ID/priority number — never double-count.

## CPC/IPC Awareness (critical)
Keyword search alone misses adjacent art. Extract CPC/IPC classes from top-5 hits and run one class-restricted query.

## Date Discipline
Distinguish filing / priority / publication / grant dates. Surface the legally-relevant one per sub-use-case (novelty→priority; FTO→grant+status; landscape→publication; diligence→grant+assignment; litigation→target priority).

## DOCX (8 sections, emphasis by sub-use-case)
Executive Summary + verdict + disclaimer → Closest Prior Art (ranked, with claim-1 text + relevance rationale) → Landscape (filer table + trend + CPC) → Citation Graph → Geographic Coverage → FTO Flags (FTO only, with risk level) → Strategy + Recommendations + mandatory attorney disclaimer → Audit Log.

## Agent Integrity Rules
Sequential 1 q/sec. Cite only this-session patents. Three counts. Retry once after 3s; stop after 3 consecutive failures. Detect plan-tier caps (Lens 1000/mo).

## Anti-Patterns
Searching before sub-use-case commit; vague invention descriptions; keyword-only (no CPC follow-up); treating family members as separate hits; confusing date types; skipping disclaimer when legal consequences apply; verdict without claim-text evidence; fabricating Lens data when key absent.
