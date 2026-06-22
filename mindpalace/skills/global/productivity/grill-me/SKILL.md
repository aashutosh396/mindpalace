---
name: Grill Me (Plan Interrogator)
description: Use when the user wants a plan or design stress-tested — interview them relentlessly, one question at a time, walking each branch of the decision tree with a recommended answer per question.
tags: [grill-me, plan-review, stress-test, decision-tree, interrogation, design-review, matt-pocock, forcing-questions]
source: alirezarezvani/claude-skills
derived_from: engineering/grill-me/skills/grill-me (Matt Pocock, MIT)
---

# Grill Me

Interview the user relentlessly about every aspect of this plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one. For each question, provide your recommended answer.

## Rules
1. **One question per turn.** Never bundle.
2. **Recommended answer with each question.** Defaulting to "what do you think?" is lazy.
3. **Explore the codebase before asking.** If `grep`/`Read` resolves it, do that first — saves a turn.
4. **Walk the tree depth-first.** Finish a branch before opening another.
5. **Track dependencies.** If decision B depends on A, ask A first.

## Workflow
1. User provides a plan/design (or a path to one).
2. Extract the decision branches from it.
3. Produce the question list with a recommendation each.
4. Walk the tree one question at a time, recording answers.
5. When all branches resolved → report "shared understanding reached" + the locked-in decisions.

## Output pattern per turn
```
Q[i]/[total]: [question]
Recommended answer: [your call + 1-sentence rationale]

(Or: I explored the codebase and found [evidence]. Confirm?)
```
