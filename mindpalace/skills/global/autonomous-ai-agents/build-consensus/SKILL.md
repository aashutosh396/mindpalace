---
name: build-consensus
description: "Use when a group (people, services, or multiple AI agents) must decide between options without a single authority, or when past decisions hit groupthink or deadlock — apply independent scouting, quality-proportional advocacy, quorum thresholds, and deadlock resolution modeled on honeybee swarm decision-making. Triggers: reach consensus, group decision, quorum, vote, deadlock, multi-agent decision, distributed agreement, tiebreak."
version: 1.0.0
license: MIT
tags: [consensus, decision-making, quorum, multi-agent, distributed-agreement, deadlock, voting, swarm]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/build-consensus
derived_from: awesomeclaude
---

# Build Consensus

Reach collective agreement without a central authority — independent evaluation, proportional advocacy, and quorum commitment.

## When to Use

- A group must choose between options without a designated leader
- Centralized decision-making is a bottleneck or single point of failure
- Stakeholders hold different information that must be integrated
- Past decisions suffered groupthink or analysis paralysis
- Designing systems that must reach consensus (distributed DBs, multi-agent AI)

## Inputs

- Required: the decision (binary, N options, or parameter), participating agents/voters
- Optional: known options with preliminary scores, urgency/time budget, acceptable error rate, current failure mode

## Procedure

### Step 1 — Generate proposals via independent scouting
Assign scouts (min 3 per serious option) to evaluate options without seeing each other's findings — prevents early herding. Each produces option ID, quality score, strengths/risks, and confidence. Aggregate all options above a minimum threshold; eliminate none by a single evaluator.

### Step 2 — Run advocacy dynamics
Scouts advocate for their top option with intensity proportional to quality, publicly and with evidence. Uncommitted agents independently inspect advocated options and join only if their own check confirms quality. Exaggerated advocacy fails verification, so the group self-corrects toward the strongest option.

### Step 3 — Set quorum and commit
Threshold by stakes: simple = 50%+1, important = 66-75%, critical/irreversible = 80%+. Track commitment transparently; disallow mid-cycle withdrawal (prevents oscillation). When quorum is reached, adopt the option and begin implementation immediately.

### Step 4 — Resolve deadlocks
Diagnose: genuine tie (flip a coin or merge), information deficit (time-boxed more scouting), faction formation (force cross-inspection of the opposing option), option proliferation (eliminate bottom 50%, re-run). If deadlocks recur, the framing may be wrong — decompose the decision or run a time-boxed experiment.

### Step 5 — Assess consensus quality
Check: was the winner verified by N agents? Was speed appropriate? Did the process surface info a single decider would miss? Track time-to-quorum, scout-to-commit ratio, and post-decision regret; feed learnings back into thresholds and scout counts.

## Validation

- [ ] Proposals from independent scouting (no herding)
- [ ] Advocacy proportional to assessed quality
- [ ] Uncommitted agents independently verified
- [ ] Quorum threshold matched the stakes; decision implemented promptly
- [ ] Deadlock mechanism available; post-decision quality assessed

## Common Pitfalls

- Skipping independent scouting (groupthink).
- Equal advocacy for unequal options (random selection).
- Allowing commitment withdrawal (oscillation).
- Confusing consensus with unanimity (permanent deadlock).
- Ignoring the losing side's information during implementation.

## Related

- conduct-retrospective — consensus-building about process improvement
- coordinate-reasoning — internal coordination of multi-path reasoning
