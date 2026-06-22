---
name: Board Meeting Protocol
description: Use when running structured multi-perspective executive deliberation on a strategic decision — a 6-phase protocol that prevents groupthink, captures minority views, and produces a clean decision.
tags: [board-meeting, deliberation, strategic-decision, multi-agent, groupthink, decision-extraction, founder-review]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/skills/board-meeting
---

# Board Meeting Protocol

Structured multi-agent deliberation that prevents groupthink, captures minority views, produces actionable decisions.

## The 6 phases

### Phase 1 — Context gathering
Load company context. Load only **approved** prior decisions (never raw transcripts). Reset session state (no bleed). Present agenda + activated roles, wait for confirmation. Select relevant roles by topic — not everyone every time (e.g. market expansion → CEO/CMO/CFO/CRO/COO; pricing → CMO/CFO/CRO/CPO; technology → CTO/CPO/CFO/CISO).

### Phase 2 — Independent contributions (ISOLATED)
No cross-pollination. Each role runs before seeing others' outputs. Each uses its own reasoning technique (CEO: tree of thought; CFO: chain of thought/show math; CMO: draft→critique→refine; CPO: first principles; CRO: pipeline math; CISO: risk P×I; etc.). Contribution format (max 5 points, self-verified):
```
## [ROLE] — [DATE]
• [Finding] — [VERIFIED/ASSUMED] — 🟢/🟡/🔴
Recommendation: [position]   Confidence: High/Med/Low
Source: [where data came from]   What would change my mind: [condition]
```

### Phase 3 — Critic analysis
A critic receives ALL Phase 2 outputs at once; adversarial reviewer, not synthesizer. Checks: where did they agree too easily (suspicious consensus)? what shared assumption is unvalidated? who's missing (customer voice? front-line)? what risk did nobody mention? who operated outside their domain?

### Phase 4 — Synthesis
Decision required (one sentence) · perspectives (one line/role) · where they agree / disagree · critic's uncomfortable truth · recommended decision + action items (owners, deadlines) · your call (options if you disagree).

### Phase 5 — Human in the loop (FULL STOP)
Wait for the founder. Options: Approve / Modify / Reject / Ask follow-up. User corrections OVERRIDE agent proposals — no pushback. 30-min inactivity → auto-close as pending.

### Phase 6 — Decision extraction
After approval: write full transcript to raw layer; write approved decision record to approved layer + append to index. Mark rejected proposals DO_NOT_RESURFACE. Confirm count of decisions logged, actions tracked, flags added.

## Two-layer memory rule

Raw transcripts = reference only, never auto-loaded. Approved decisions only feed future meetings. This prevents hallucinated consensus from past debates.

## Failure modes → fix

Groupthink → re-run Phase 2 isolated, force "strongest argument against" · analysis paralysis → cap at 5 points, force a recommendation even at low confidence · bikeshedding → log as async item · role bleed → critic flags, exclude from synthesis · layer contamination → Phase 1 loads approved only (hard rule).
