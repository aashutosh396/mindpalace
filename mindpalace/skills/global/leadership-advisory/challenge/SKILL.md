---
name: Pre-Mortem Plan Challenge
description: Use before committing significant resources, presenting to a board, or when feedback has been one-sidedly positive — imagine the plan failed in 12 months and work backwards to surface assumptions, rate them by confidence × impact, map the dependency chain, and define kill switches.
tags: [pre-mortem, plan-challenge, assumptions, vulnerability-map, dependency-chain, kill-switch, reversibility]
source: alirezarezvani/claude-skills
derived_from: executive-mentor/challenge
---

# Challenge — Pre-Mortem Plan Analysis

Most plans fail for predictable reasons — bad assumptions, not bad luck. The pre-mortem: imagine it's 12 months from now and this plan failed spectacularly; work backwards. Not to kill the plan — to make it survive contact with reality.

## When to Run
Before committing significant resources; before board/investors; when you only hear positive feedback; when the plan needs multiple external dependencies to align; under pressure to "move fast and figure it out later"; when you're excited (excitement = scrutinize harder).

## Framework

**1. Extract core assumptions.** Per section: what must be true? Categories — market (size, growth, willingness to pay, buying cycle), execution (capacity, velocity, no major hires needed), customer (has the problem, knows it, will pay), competitive (incumbents won't respond, moat holds), financial (burn, revenue timing, CAC/LTV), dependency (partner delivers, API stable, regulation stable).

**2. Rate each assumption on two axes.** Confidence: High (verified) / Medium (directional) / Low (untested) / Unknown. Impact if wrong: Critical (plan fails) / High (major delay/cost) / Medium (rework) / Low (manageable).

**3. Map vulnerabilities.** Vulnerability = Low/Unknown confidence × Critical/High impact. These are the bets you're making — the question is whether you're making them consciously.

**4. Find the dependency chain.** Plans often fail because multiple assumptions must hold simultaneously. Does B depend on A? If the first breaks, how many downstream break? What's the critical path with zero slack?

**5. Test reversibility.** For each critical vulnerability: if wrong at month 3, can you pivot/cut scope? Is money spent, commitments made? Less reversible → validate harder before committing.

## Output Format
```
CORE ASSUMPTIONS: [assumption] — Confidence [H/M/L/?] — Impact [Crit/High/Med/Low]
VULNERABILITY MAP: critical risks (act before proceeding) / high risks (validate before scaling) — why it might be wrong + what breaks
DEPENDENCY CHAIN: A → B → C; weakest link
REVERSIBILITY: reversible bets / irreversible commitments
KILL SWITCHES: continue if [30/60/90-day criteria] / kill-pivot if [criteria]
HARDENING ACTIONS: validations, alternatives, contingencies
```

## The Hardest Questions (the ones people skip)
"What's the bear case, not the base case?" / "If a team we don't trust ran this exact plan, would it work?" / "What are we not saying out loud because it's uncomfortable?" / "Who has incentives to make this sound better than it is?" / "What would an enemy of this plan attack first?"

The output isn't permission to stop — it's a vulnerability map. Unknown risks are dangerous; known risks are manageable.
