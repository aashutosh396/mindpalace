---
name: develop-adr
description: "Use when making a significant technical decision — record an Architecture Decision Record (Nygard format) capturing context, the decision, alternatives, and consequences. Triggers: ADR, architecture decision record, document a technical decision, why did we choose, technology selection, framework/database choice, architectural rationale."
version: 1.0.0
license: Apache-2.0
tags: [adr, architecture-decision-record, technical-decisions, nygard, rationale, technology-selection, software-architecture, documentation]
source: https://github.com/product-on-purpose/pm-skills/tree/main/skills/develop-adr
derived_from: awesomeclaude
---

# Architecture Decision Record (ADR)

An ADR documents a significant technical decision with its context and consequences, capturing the "why" so future readers understand the reasoning. Follows Michael Nygard's lightweight format.

## When to use

- Significant technical decisions affecting system architecture
- Choosing between technology options (frameworks, databases, services)
- Establishing patterns future development should follow
- Documenting rationale for constraints or non-obvious approaches
- Preserving institutional knowledge about past decisions

## When NOT to use

- It's a product/UX design choice, not architecture → design rationale
- Still exploring feasibility → time-box and record a spike summary first
- Pitching a solution to stakeholders → solution brief (an ADR records a decision, it doesn't sell one)
- Nothing is actually being decided → wait until there is a decision

## How

1. **Assign number and title.** Sequential (ADR-001…); title is a short noun phrase, e.g. "Use PostgreSQL for order data".
2. **Set status.** Proposed → Accepted / Deprecated / Superseded by ADR-XXX. Track changes.
3. **Describe context.** Circumstances that led here: problem, forces (constraints, expertise, timeline, cost). Help a reader who wasn't there understand why.
4. **State the decision.** Active voice ("We will use…"); be specific about what is and isn't included.
5. **Document consequences.** Positive, negative, and neutral outcomes. Be honest about trade-offs: what gets easier, harder, what new constraints/options arise.
6. **Record alternatives considered** and why they were rejected; add references.

## Output sections

Status; Context; Decision; Consequences; Alternatives Considered; References.

## Quality checklist

- [ ] Title is a short descriptive noun phrase
- [ ] Context explains the forces at play
- [ ] Decision stated in active voice, specific
- [ ] Consequences honest about trade-offs (good and bad)
- [ ] Alternatives considered, with rejection rationale
