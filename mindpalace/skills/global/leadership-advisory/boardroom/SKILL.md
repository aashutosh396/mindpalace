---
name: Multi-Role Boardroom Deliberation
description: Use when a decision spans multiple executive domains (e.g. a pricing change touching finance, positioning, and product) — runs a 6-phase multi-advisor deliberation with independent-thinking isolation, cross-examination, a devil's-advocate pass, and synthesis into a voted memo with dissent and kill criteria.
tags: [boardroom, deliberation, multi-role, isolation, devils-advocate, voting, dissent, board-memo, decision]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/boardroom
---

# Multi-Role Boardroom Deliberation

Runs a full board-meeting protocol across multiple advisor roles for a single strategy brief.

## The 6 phases
1. **Briefing** — distribute the brief to all advisors in "Affected Roles"; each reads company context + brief. No discussion yet.
2. **Independent Thinking (ISOLATION)** — each advisor produces their position *independently*, without seeing others': opening, recommendation, top 3 concerns, top 3 supports. This is the highest-leverage step — it surfaces dissent that anchoring/groupthink would suppress.
3. **Cross-Examination** — positions revealed simultaneously; each advisor critiques others on the dimensions they own (finance critiques the math, security the risk, product the JTBD, etc.).
4. **Devil's Advocate Pass** — challenge the leading option; surface three concerns with severity ratings.
5. **Synthesis** — synthesize which option commands majority and what dissents remain unresolved; produce the board memo.
6. **Decision Hand-off** — present to the founder; on approval route to the decision-logger.

## Output: board memo
```markdown
# Board Memo: <topic>   Status: AWAITING FOUNDER DECISION | APPROVED | REJECTED
## Question — one sentence from the brief
## Recommended Option — <name>, chosen because <synthesis>
## Vote Tally — | advisor | vote | one-sentence reason |
## Dissent — <dissenter>: <unresolved concern>
## Devil's Advocate Concerns — CRITICAL/HIGH/MEDIUM + mitigation each
## Success & Kill Criteria — from brief, refined by the panel
## Recommended Decision Path — log → execute → (optional) cross-eval / freeze
```

## Why isolation matters
If advisors see each other's positions before forming their own, they anchor. Phase-2 isolation is the single practice that turns a deliberation from theater into signal.
