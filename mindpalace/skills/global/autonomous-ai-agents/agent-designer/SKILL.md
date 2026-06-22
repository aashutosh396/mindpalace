---
name: Agent Designer
description: Use when designing a multi-agent system, picking an orchestration pattern (supervisor/swarm/pipeline), generating tool schemas, or evaluating agent run logs for cost/latency/failure bottlenecks.
tags: [multi-agent, orchestration, supervisor, swarm, pipeline, tool-schema, agent-evaluation, bottleneck, anthropic, openai]
source: alirezarezvani/claude-skills
derived_from: agent-designer
---

# Agent Designer

Design, schema-generate, and evaluate multi-agent systems deterministically. Don't freehand an architecture when you can score one from requirements. (NOT for single-agent prompt scaffolds → agent-workflow-designer; NOT for runtime fan-out → agenthub.)

## Pattern decision table
| Pattern | When | Watch out for |
|---|---|---|
| Single agent | One bounded task, <~5 tools | Don't add agents you don't need |
| Supervisor | Central decomposition, specialists report back | Supervisor becomes bottleneck |
| Pipeline | Strictly sequential stages with handoffs | Rigid order; slowest stage gates throughput |
| Hierarchical | Multiple layers, >~8 agents | Communication overhead per level |
| Swarm | Parallel peers, fault tolerance over predictability | Hard to debug; needs consensus rules |

## Workflow (each step's JSON feeds the next)
1. **Design architecture** from a requirements JSON (`goal`, `tasks[]`, `constraints{max_response_time, budget_per_task, concurrent_tasks}`, `team_size`) → architecture (pattern, agents, comms links), Mermaid diagram, implementation roadmap. Present the diagram + per-agent roles.
2. **Generate tool schemas** from plain tool descriptions → Anthropic + OpenAI formats. **Gate: every tool prints ✓ Valid.** Never hand an agent an unvalidated schema.
3. **Evaluate execution logs** → summary, per-agent metrics, bottleneck analysis, error analysis, cost breakdown, SLA compliance, optimization recommendations.
4. **Verification loop**: schema validation reports 0 invalid; pilot run reports 0 critical issues (else apply top recommendation, re-run, re-evaluate).

## References worth knowing
Agent architecture pattern trade-offs; tool design (schema, idempotency, error handling); evaluation metric definitions (success rate, latency distribution, cost, bottlenecks).
