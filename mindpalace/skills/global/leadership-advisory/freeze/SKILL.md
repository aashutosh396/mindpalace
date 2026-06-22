---
name: Decision Freeze (cs:freeze)
description: Use when an irreversible or high-cost-to-reverse decision was made under pressure and deserves a cooling-off lock before execution — locks the decision for a cooldown period so it can't be impulsively re-litigated.
tags: [decision-freeze, cooldown, irreversible, layoff, fundraise, pivot, founder-discipline, governance]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/freeze
---

# Cooldown Lock on a Decision

Locks a decision for a defined cooldown period. During the freeze, the router refuses to re-litigate the decision unless a kill criterion explicitly triggers.

## When to use
- After any **irreversible** or **high-cost-to-reverse** decision (fundraise, layoff, market entry).
- After a **split-vote** boardroom (preserve the call against second-guessing).
- After a **founder gut-feel override** of unanimous advisor consensus (let it run).
- During a **personnel transition** (lock the strategy so the new exec executes, not redebates).

## Default freeze periods
| Decision type | Default freeze |
|---|---|
| Fundraise round size / lead choice | 30 days |
| Pricing change | 60 days |
| Market entry / exit | 90 days |
| Layoff / RIF | 30 days |
| Strategic pivot | 90 days |
| Personnel (exec hire/fire) | 60 days |
| M&A LOI | 30 days |

## Workflow
1. Read the decision record; validate APPROVED status.
2. Apply freeze: write `freeze_until: YYYY-MM-DD` to the record.
3. Add to an active-freezes index.
4. Router now refuses to re-route this topic until the freeze expires OR a kill criterion triggers.

## Output (record updated in place)
```
**Status:** FROZEN
**Frozen until:** YYYY-MM-DD
**Reason for freeze:** <text>
**Override condition:** Kill criterion <name> triggers OR explicit unfreeze with stated reason
```

## Override and auto-override
- Early release requires an explicit unfreeze with a stated reason, logged permanently (surfaces at post-mortem).
- If a kill criterion triggers, the freeze auto-releases and routes immediately to post-mortem. The freeze protects against impulse, not against reality.

## Why this beats "just don't re-decide"
Without an explicit lock + log, every founder wobble produces a "let's discuss this again" — exhausting for advisors and erodes the value of deliberation. The freeze is a process, not a rule; it logs every override so discipline can be audited.
