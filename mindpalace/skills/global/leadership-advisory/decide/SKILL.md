---
name: Decision Logger (cs:decide)
description: Use when a founder/board has approved a strategy memo and the decision must become durable, auditable company memory — turns an approved memo into a structured decision record with binding success/kill criteria and preserved dissent.
tags: [decision-log, strategy, governance, dissent, kill-criteria, board-memo, company-memory, founder]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/decide
---

# Log the Decision

The gate where in-session deliberation becomes durable company memory.

## Two-layer memory model
1. **Raw transcripts** — every session, every advisor position, every dissent. Reference only; never feeds back automatically.
2. **Approved decisions** — only founder-signed memos. Feed into future intake and routing.

This split prevents the system from "remembering" unresolved debates as if they were decisions.

## Workflow
1. Read the memo path.
2. Verify founder approval (status: APPROVED).
3. Extract structured record: title, date decided, option chosen, success + kill criteria, dissent (preserved), review checkpoint.
4. Append to an approved-decisions store (`<YYYY-MM-DD>-<slug>.md`).
5. Update the raw transcript pointer.
6. Schedule auto-revisit (90 days default).

## Output record format
```markdown
# Decision: <title>
**Decided:** YYYY-MM-DD  **By:** <name>  **Review checkpoint:** YYYY-MM-DD (90d)

## Decision
**Chose:** <option>
**Rejected:** <other options + one-line why>

## Success Criteria (binding)
- <metric, threshold, timeframe>

## Kill Criteria (binding)
- <metric, threshold, action>

## Preserved Dissent
- **<dissenter>:** <unresolved concern>  (verbatim; never erased)

## Status History
- YYYY-MM-DD: APPROVED
```

## Why preserved dissent
The biggest risk in approved decisions is forgetting why someone disagreed. When kill criteria trigger, the dissent often turns out to have been correct. Preserve it verbatim — not summarized — to keep the company honest at post-mortem time.

## Stale-decision audit (weekly)
- Decisions > 90 days without revisit → flag for post-mortem.
- Decisions with kill criteria triggered → flag immediately.
- Decisions whose basis assumptions have changed → flag for re-examination.
