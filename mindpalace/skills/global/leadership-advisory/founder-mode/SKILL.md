---
name: Founder-Mode Auto-Router
description: Use when a founder asks any strategic question without knowing which advisor or process fits — keyword+intent routing to the right C-role, to a multi-role boardroom, or to office-hours sharpening when the question is too vague.
tags: [routing, founder, advisory, triage, c-suite, boardroom, office-hours, intent-matching]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/founder-mode
---

# The Auto-Router

The single entry point. Routes a founder question to the right C-role, or triggers multi-role deliberation if it spans domains. Answers "I don't know which command/advisor to use."

## Routing logic (keyword + intent)
| Signal in question | Route |
|---|---|
| burn, runway, fundraise, dilution, LTV, CAC | CFO |
| pipeline, win rate, forecast, quota, ramp, sales motion | CRO |
| positioning, ICP, message, brand, channel, campaign | CMO |
| roadmap, PMF, JTBD, North Star, RICE, kill | CPO |
| cadence, OKR, scorecard, DRI, operating system | COO |
| hiring, comp, ladder, level, attrition, eNPS, equity | CHRO |
| security, threat, breach, compliance, audit, SOC 2 | CISO |
| architecture, scaling, tech debt, SLO, latency | CTO |
| contract, IP, term sheet, regulator, license | General Counsel |
| retention, GRR, NRR, churn, CSM, time-to-value, renewals | CCO |
| training data, data rights, consent, warehouse, lakehouse | CDO |
| model selection, eval, hallucination, AI risk, fine-tune | CAIO |
| DORA, cycle time, deploy frequency, team topology | VPE |
| strategy, vision, board, M&A, raise, exit | CEO |
| **2+ signals from different roles** | multi-role boardroom |
| **ambiguous / no match** | office-hours first, then route |

## Workflow
1. Parse the question for role signals.
2. Exactly one role → invoke that advisor directly (load company context first).
3. 2+ roles → build a brief, then run boardroom deliberation.
4. Ambiguous → run office-hours intake to force the founder to sharpen.
5. Log the routing decision.

## Output (one of three)
- **Single-role route:** state routing + why + invoke advisor.
- **Multi-role route:** state routing + which roles touched + build brief + run boardroom.
- **Ambiguous → office hours:** state why too broad + run six-question intake.

## Why a router
Forcing a founder to memorize every command is a cognitive tax. The router collapses it to one input — the system picks the room. With persistent company context + decision log, it also avoids re-litigating what's already decided.
