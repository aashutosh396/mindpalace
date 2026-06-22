---
name: Deal Desk
description: Use when reviewing a specific inbound deal before close — scores margin + risk across 5 dimensions, routes discount approval to a named human approver chain, and redlines T&Cs for contract landmines (uncapped indemnity, MFN, missing DPA). Never auto-approves.
tags: [commercial, deal-desk, discount, margin, approval-routing, redline, msa, contract-landmines, indemnity]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/deal-desk
---

# Deal Desk

Per-deal review + discount-approval routing. Scores deal margin + risk, routes to the right human, redlines T&Cs. **Never auto-approves** — every output is a score + routing recommendation to a named human. Assumes the commercial policy already exists (this applies it).

## Workflow
1. **Intake** — ARR, term, discount, payment terms, customer tier, strategic flags, any customer-flagged term redlines.
2. **Score margin + risk** — 0-100 across 5 dimensions (margin 30%, risk 20%, strategic 15%, commercial 20%, term 15%) → verdict APPROVE / REVIEW / ESCALATE / DECLINE, each tied to a named approver chain. Profile by saas/enterprise-software/services/marketplace.
3. **Route the discount** — discount % + deal-size + tier → named approver chain (AE → Manager → Director → VP → CFO/CRO) + estimated cycle days. Modifiers (enterprise floor, SMB fast-lane) surfaced explicitly. Stop at the lowest-authority hop that can sign — don't over-escalate.
4. **Flag the redlines** — scan for 10 seller-killer patterns (uncapped indemnity, MFN, perpetual license-back, missing DPA, NET-60+, broad non-solicit, etc.) → CRITICAL/HIGH/MEDIUM/LOW + standard counter + named legal/commercial approver.
5. **Assemble the packet** — three outputs + the named approver chain. It is a recommendation, not an approval.

## Key margin fact
A 30% discount on an 80%-gross-margin product loses **37.5% of margin dollars**, not 30% (fixed COGS). Always model margin-after-discount in dollars.

## Anti-patterns
- Auto-approving deals (every verdict, even APPROVE, names the human(s) who sign).
- Skipping the redline scan because the score is high (a high composite with UNCAPPED_INDEMNITY is still DECLINE — critical signals override composite).
- Routing every deal to CFO (over-escalation slows the funnel and trains AEs to over-discount).
- Hand-editing the chain to skip a hop (defeats the audit trail).
- Treating the discount router as a discount calculator (it routes what's proposed; pricing logic lives in the pricing strategist).

## Forcing questions (one at a time, recommended + canon)
1. Gross margin at full discount AND next quarter's pipeline at the same terms? → model both. (Skok; Tunguz — one 40% precedent reshapes 3 quarters)
2. Inside or outside the standard discount matrix? → if outside, surface the exception and route to the named exception approver. (OpenView; RevOps Co-op)
3. Strategic value beyond ARR — logo, reference, expansion? → require a named, verifiable commitment in writing. (SaaStr; Winning by Design)
4. Indemnity cap, liability cap, DPA (if EU data) signed? → required; uncapped indemnity blocks APPROVE regardless of margin. (WorldCC; GC100)
5. Payment terms — NET-30/45/60+? → prefer NET-30; every 15 days costs ~2% of effective deal value. (KeyBanc; Pacific Crest)
6. Multi-year prepay or annual auto-renew? → multi-year prepay > annual prepay > auto-renew; auto-renew without 60-day notice is a redline. (Salesforce Deal Desk; OpenView)
7. Named human approver at each hop? → surface the name. "Maria Singh, VP Sales" not "VP Sales". (Bridge Group — named approval cuts precedent drift 50%+)
