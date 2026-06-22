---
name: CPO Review — Roadmap Forcing Questions
description: Use when committing a quarter's roadmap, deciding whether to kill a feature, or claiming PMF without a retention curve — runs six JTBD-driven forcing questions that cut the roadmap and surface what to ship vs kill.
tags: [product, roadmap, jtbd, pmf, rice, prioritization, kill-criteria, north-star, retention]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cpo-review
---

# CPO Forcing Questions

The JTBD-driven builder cuts the roadmap in half. Six questions to surface what to ship and what to kill.

## When to run
- Before quarterly roadmap commitment; before launching a new product line.
- Before adding >3 features to a release; when retention is flat or declining.
- When the team is debating "should we build X?"

## The six questions
1. **JTBD** — What job is this feature hired to do, in the user's words? Not "improve onboarding" but "help a new ops manager close their first deal in 7 days." Job ≠ feature.
2. **North Star Metric** — What user behavior does this move, and how does it ladder to the North Star? Metric must be leading, behavior-based, value-correlated. Can't trace it → don't build it.
3. **PMF Signal** — What's the retention curve for users who hire this job: flat, decaying, or smiling? Flat/smiling = PMF; decaying = none. Survey love is not a signal.
4. **RICE Score** — Reach × Impact × Confidence ÷ Effort. Where does this rank in the queue?
5. **Opportunity Cost** — What gets cut if this ships? Name the specific initiative. Headcount and time are zero-sum; the cut list is the focus list.
6. **Kill Criteria** — What signal in 90 days would tell you this was the wrong bet? Define metric + threshold in writing before launch. Can't define one → can't ship responsibly.

## Output format
```markdown
# CPO Review: <feature/plan>
## JTBD
> <one sentence in user voice>
## North Star Link — metric moved: <name>; expected delta: <%>
## PMF Signal — curve: flat/smiling/decaying; cohort N
## Score — RICE: <n>; rank #N of M
## Cut List — cut: <initiative>; reason: <why this matters more>
## Kill Criteria (90d) — metric/threshold/action
## Verdict — 🟢 SHIP | 🟡 SHARPEN | 🔴 KILL
```
