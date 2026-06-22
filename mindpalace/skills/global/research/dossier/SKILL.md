---
name: Decision-Grade Entity Dossier
description: Use when the user wants background research, diligence, or meeting prep on a specific company/person/nonprofit/gov org ("prep me for a meeting with X", "due diligence on X") — forces a hypothesis upfront and tests it (not a generic profile), then delivers a verdict + conversation hooks + provenance audit.
tags: [dossier, due-diligence, entity-research, meeting-prep, hypothesis-testing, competitive-intel, background]
source: alirezarezvani/claude-skills
derived_from: research/dossier (Decision-Grade Entity Research)
---

# Dossier — Decision-Grade Entity Research

Refuses to be "tell me about Microsoft". The forcing hypothesis question (Q4) is the non-generic anchor: the dossier **tests** the user's belief rather than confirming it. Uses WebSearch + WebFetch + free APIs (SEC EDGAR, GitHub, ProPublica); optional BYOK MCPs enhance.

## Phase 1: Intake (6 forcing questions, one at a time)
1. **Subject identity** — exact name + a second identifier (URL/LinkedIn/affiliation). Refuse ambiguous names.
2. **Subject type** — person / company / nonprofit / gov / other. Routes the source matrix.
3. **Purpose** — sales/partnership, investment diligence, acquisition diligence, journalism, interview prep, competitive intel, personal vetting, other.
4. **Hypothesis — MANDATORY.** "What do you already believe, and what do you want to verify or disprove?" If refused, push back once; if still refused, fall back to "most surprising thing I could find" and flag in audit.
5. **Depth** — 5-min brief (~10 searches, skips network/reputation) or 15-min decision-grade.
6. **Sensitivities** (only journalism/personal-vetting) — topics to exclude.

## Phase 3: Source Matrix (by subject type)
- **Person** — LinkedIn, personal site, X (degrade gracefully), GitHub, Scholar, news, talks/podcasts.
- **Company** — official site, SEC EDGAR (public), Crunchbase free, news, GitHub, Glassdoor, LinkedIn.
- **Nonprofit** — ProPublica 990s, site, news.
- **Gov** — .gov sites, news, ProPublica.
Mark BYOK-MCP findings in audit.

## Phase 4: Hypothesis-Driven Search (≥30% disconfirming)
Every search classified supporting OR disconfirming. **At least 30% of budget on disconfirming queries** — this is what makes the dossier decision-grade vs confirmation-biased. Apply a source tier (primary/secondary/tertiary) to each result.

## Phases 5-8
- **12-month timeline** — news, funding, hires/departures, controversies; reverse chronological, hyperlinked + tiered.
- **Network** — investors/customers/partners (companies); co-founders/advisors/board (people). 5-10 ranked by hypothesis relevance.
- **Reputation** — news sentiment, Glassdoor, peer mentions; tier (noisy).
- **Red flags** — litigation, regulatory actions, unusual departures, going-concern notes; each tiered, not sensationalized.
- **Conversation hooks** — 3-5 tied to actual findings (not "ask about their roadmap"). Each = hook + finding (hyperlink+tier) + suggested verbatim framing.

## DOCX (9 sections)
Executive Summary with **hypothesis verdict** (SUPPORTED / PARTIALLY / DISPROVEN / INCONCLUSIVE) → Identity Facts → Hypothesis Test (supporting + disconfirming + verdict) → Timeline → Network → Reputation → Red Flags → Conversation Hooks → Source Provenance + Audit (three counts + per-tier + classification + BYOK flag).

## Agent Integrity Rules
Sequential searches (1 q/sec etiquette). Cite only this-session sources; Wikipedia/training tagged "[Background — verify]". Three-count + per-tier breakdown. Retry once after 3s; stop after 3 consecutive failures.

## Anti-Patterns
No forcing hypothesis; <30% disconfirming budget; accepting ambiguous names; generic hooks; sensationalized/untiered red flags; confirmation-biased verdict; including Q6-excluded topics; unflagged BYOK data.
