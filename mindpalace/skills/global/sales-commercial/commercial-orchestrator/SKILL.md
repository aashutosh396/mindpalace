---
name: Commercial Orchestrator
description: Use when a commercial request (pricing, deal review, discount approval, partnerships, channel economics, commercial policy, RFP response, bookings forecast) needs routing to the right discipline — deterministic two-signal routing with grill-first discipline.
tags: [commercial, orchestrator, routing, pricing, deal-desk, partnerships, rfp, forecast, channel]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/commercial-skills
---

# Commercial Orchestrator

Routes a commercial inquiry (per-deal economics and packaging) to one of seven disciplines, then returns a digest. Distinct from sales execution and strategic CRO judgment.

## Signal table
| Signal | Keywords | Route to |
|---|---|---|
| PRICING | pricing, packaging, tier, WTP, Van Westendorp, value pricing | pricing strategist |
| DEAL | deal, discount, approval, margin, T&Cs, redline, exception, MSA | deal desk |
| PARTNERSHIP | partner, reseller, OEM, co-sell, revenue share, channel agreement | partnerships architect |
| CHANNEL_ECON | channel mix, cost to serve, channel ROI, direct vs partner | channel economics |
| POLICY | commercial policy, discount matrix, T&C library, exception policy | commercial policy |
| RFP | RFP, RFI, RFQ, proposal request, security questionnaire | rfp responder |
| FORECAST | forecast, bookings, billings, ARR, NRR forecast, pipeline math | commercial forecaster |

## Routing logic
1. **Explore before asking** — workspace artifacts resolve the lane (`pipeline-Q4.csv` → forecast; `MSA-redline.docx` → deal). Route silently if resolved.
2. **Two-signal threshold** — single weak signal → ONE clarifying question with a recommended answer naming the two candidate lanes. Never bundle.
3. **Multi-lane** (e.g., "this RFP wants a discount we don't normally give" = RFP + DEAL + POLICY) → highest-confidence lane first → digest → ask before chaining the next. Never silently chain.
4. **Digest** ≤200 words: analyzed, top-3 findings (canon-anchored), top-3 next actions (named approver where applicable), artifact path, ONE grill challenge.

## Lane-defining forcing questions
- PRICING: paying for outcomes, seats, or usage? → outcomes (value-based) if measurable. (Ramanujam: seat pricing on usage-variable product caps TAM at ~20% of WTP)
- DEAL: gross margin at full discount AND next quarter's pipeline at the same terms? → model both. (Tunguz: one 40% precedent reshapes 3 quarters)
- FORECAST: stage-conversion from last 4Q or last 12Q? → last 4 weighted heavier. (Skok/OpenView)
- PARTNERSHIP: does the partner have independent demand or reselling our pipeline? → insist on independent-demand evidence. (Forrester)

## Hard rules
- Pricing = model + range, never a single number.
- Deals = score + named human approver, never auto-approve (even at 0% discount).
- Forecasts = surface the conversion assumption explicitly.
- RFP responses = never invent claims; surface GAPs, leadership decides bid/no-bid.
- Partnerships = independent-demand evidence required for STRATEGIC tier.
