---
name: argumentation
description: "Use when a technical claim, design decision, PR description, ADR, code-review comment, or research point needs rigorous justification — build the hypothesis → argument → example triad, pick the right reasoning type, steelman the counterargument, and ground claims in verifiable evidence. Triggers: justify, make the case, design rationale, why this change, ADR, decision record, persuade, reasoning, critical thinking."
version: 1.0.0
license: MIT
tags: [argumentation, reasoning, hypothesis, logic, rhetoric, critical-thinking, decision-making, steelman]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/argumentation
derived_from: awesomeclaude
---

# Construct Arguments

Build rigorous arguments from hypothesis through reasoning to concrete evidence. Every persuasive claim follows a triad: a clear hypothesis (what you believe), an argument (why it holds), and examples (proof that it holds).

## When to Use

- Writing/reviewing a PR description that proposes a change
- Justifying a design decision in an ADR
- Code-review feedback that goes beyond "I don't like this"
- A research argument or technical proposal
- Challenging or defending an approach in discussion

## Procedure

### Step 1 — Formulate the hypothesis
State the claim in one falsifiable, narrowly scoped sentence. Apply the "how would I disprove this?" test. If you cannot imagine counter-evidence, it is an opinion, not a hypothesis. ("This code is bad" → "This function is O(n^2) where O(n) is achievable.")

### Step 2 — Identify the argument type
- Deductive — "must be true" (formal proofs, type safety)
- Inductive — "tends to be true" from observed cases (perf data, test results)
- Analogical — "will likely work" from similar prior cases (tech choices)
- Evidential — "fits the data better than alternatives" (research, A/B tests)
Combine types for strength; split the hypothesis if no single type fits.

### Step 3 — Construct the argument
State premises (facts/assumptions), show the logical chain from premises to conclusion, then steelman the strongest counterargument — state the best opposing case before rebutting it. Weak arguments usually come from unsupported premises, not faulty logic; find evidence for each premise or label it an assumption.

### Step 4 — Provide concrete examples
Examples are the empirical foundation, not illustrations. Give at least one positive example and one edge case/limitation. Each must be independently verifiable: specific files/lines/commits for code, specific papers/datasets/results for research. If examples are hard to find, the hypothesis is too broad — narrow it.

### Step 5 — Assemble for the context
- Code review: [Summary] → Hypothesis → Argument → Evidence → Suggestion
- PR description: ## Why → ## Approach → ## Evidence
- ADR: Context (hypothesis) → Decision (argument) → Consequences (evidence)
- Research: Intro (hypothesis) → Methods/Results (argument+examples) → Discussion (counterarguments)
Review for logical gaps, unsupported premises, unaddressed objections, and scope creep.

## Validation

- [ ] Hypothesis falsifiable and scoped (not universal)
- [ ] Argument type identified and appropriate
- [ ] Premises explicit; logical chain has no gaps
- [ ] Strongest counterargument steelmanned and addressed
- [ ] >=1 positive example and >=1 edge case, all verifiable
- [ ] Output format matches context; no logical fallacies

## Common Pitfalls

- Stating opinions as hypotheses ("this code is messy").
- Skipping the counterargument.
- Vague examples ("we've seen this before").
- Argument from authority ("Google does it this way").
- Scope creep — match conclusion scope to evidence scope.
- Conflating argument types ("tends to" for a deductive "must be").

## Tip: adversarial self-review

For high-stakes decisions, after structuring the triad, stress-test it: steelman the proposal, challenge each assumption, and flag severity (Critical = redesign, Medium = adjust, Low = note). Overexplaining signals insecurity — tighter arguments are stronger.

## Related

- conduct-post-mortem, manage-backlog — decisions that benefit from clear justification
