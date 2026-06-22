---
name: Inter-Agent Communication Protocol
description: Use when multiple specialized agents need to query each other, coordinate cross-functional analysis, or run multi-agent deliberations — defines invocation syntax, loop prevention (no self-invoke, max depth 2, no circular calls), isolation rules, conflict surfacing, and a verification quality loop before output.
tags: [multi-agent, agent-protocol, orchestration, loop-prevention, agent-invocation, isolation, quality-loop, conflict-resolution]
source: alirezarezvani/claude-skills
derived_from: agent-protocol (Inter-Agent Protocol)
---

# Inter-Agent Protocol

How a team of specialized agents talk to each other without chaos, loops, or circular reasoning.

## Invocation
`[INVOKE:role|question]`. Invoked agents respond with a structured block: Key finding (one line) / Supporting data (2-3 points) / Confidence (high|medium|low) / Caveat (what could make this wrong).

## Loop Prevention (hard rules, no exceptions)
1. **No self-invocation** — an agent cannot invoke itself.
2. **Max depth = 2** — chains can go A→B→C; the third hop is blocked.
3. **No circular calls** — if A called B, B cannot call A in the same chain.
4. **Chain tracking** — each invocation carries its call chain `[CHAIN: a → b → c]`; agents check it before invoking.
When blocked: return `[BLOCKED: ...]` and state the explicit assumption used instead, rather than invoking.

## Isolation Rules
- **Independent-analysis phase** — NO invocations; each role forms views before cross-pollination (prevents anchoring/groupthink). Need data from another role → state `[ASSUMPTION: ...]`.
- **Critique phase** — the critic may *reference* other roles' outputs but cannot invoke them (critique must be independent of new data requests).
- **Otherwise** — invocations allowed, subject to loop prevention.

## Invoke vs Assume
Invoke when: the question needs domain data you lack, an error would materially change the recommendation, or it's inherently cross-functional. Assume when: directionally clear, in isolation phase, chain already at depth 2, or minor vs your main analysis. Always state assumptions explicitly: `[ASSUMPTION: runway ~12mo based on typical Series A burn — not verified]`.

## Conflict Resolution
When invoked agents conflict: flag it explicitly `[CONFLICT: ...]`, state resolution approach (conservative = worse case / probabilistic = weight by confidence / escalate to human). **Never silently pick one** — surface it.

## Internal Quality Loop (before anything reaches the decision-maker)
1. **Self-verify** — source attribution per data point; assumption audit (tag VERIFIED vs ASSUMED; >50% assumed → flag low confidence); confidence score (🟢/🟡/🔴); contradiction check vs known context; "so what?" test (every finding has a one-sentence business consequence or it's cut).
2. **Peer-verify** (when a recommendation touches another role's domain) — that role validates BEFORE presenting: `[PEER-VERIFY:role] Validated ✅ / Adjusted ⚠️ / Flagged 🔴`. Skip for single-domain or time-sensitive alerts.
3. **Critic pre-screen** (irreversible/high-cost/bet-the-company) — weakest point, missing perspective, quantified downside, proceed verdict. Triggers: >20% of runway, >30% of team affected, strategy change, external commitments, or suspicious unanimous consensus.
4. **Course correction** — after feedback: approve→log, modify→re-verify changed parts, reject→log with reason, follow-up→deepen + re-verify. Post-decision review at 30/60/90 days.

Verification level by stakes: Low (self only) / Medium (self+peer) / High (self+peer+critic) / Critical (all + full deliberation).

## Decision Memory (two-layer)
Layer 1 raw (full transcripts incl. rejected arguments; reference only, never auto-loaded). Layer 2 approved (only approved decisions; this is what future sessions load — prevents hallucinated consensus). Only the decision-logger / synthesis role writes decisions; individual agents never write directly.

## Output Standard
Bottom line first. Results and decisions only (no process narration). What + Why + How. Max 5 bullets/section. Actions have owners + deadlines. Decisions framed as options with a recommendation. The human decides — agents recommend. Risks concrete ("if X, Y breaks, costing $Z"). No jargon without explanation. Silence is an option if there's nothing to report.
