---
name: Process Mapper
description: Use when a BizOps lead or COO needs to document an end-to-end business process in BPMN-style swim lanes, measure cycle time by stage, surface where work waits vs gets worked, and name the bottleneck — Lean / Six Sigma / Theory-of-Constraints applied to internal ops.
tags: [process-mapping, bpmn, bottleneck, cycle-time, value-stream, lean, six-sigma, theory-of-constraints, swim-lane, value-add-ratio]
source: alirezarezvani/claude-skills
derived_from: business-operations/process-mapper
---

# Process Mapper

BPMN-style business-process documentation, bottleneck detection, and cycle-time analysis for internal-ops leaders. Deterministic, not LLM intuition. Tactical process documentation — not sales-pipeline, not system SLOs, not strategic OKRs.

## Three Failure Modes It Fixes

Implicit process (tribal knowledge → dropped handoffs) · invisible waiting (most elapsed time is queue/wait/approval, not work — teams optimize the wrong stage) · local optimization (adding resources to non-constraint stages gains nothing).

## Workflow

1. **Intake** — capture the process as data with one entry per stage: `name`, `owner`, `type` (`value-add` | `wait` | `rework`), `duration_minutes_p50`, `duration_minutes_p90`.
2. **Map stages** — produce an ASCII swim-lane diagram (lanes by owner so cross-functional handoffs become visible) + normalized artifact.
3. **Measure cycle time** — total P50, total P90, value-add ratio (VA%), Little's-Law throughput. Verdict: VA% >25% HEALTHY, 10-25% TYPICAL (most non-manufacturing), <10% WASTE-HEAVY.
4. **Detect bottlenecks** — three rules: (a) stage P50 > 2× mean of value-add stages, (b) wait-state % > 40% of total, (c) rework % > 15%. Thresholds adjust by industry profile (saas/services/manufacturing/healthcare). Output: ranked list with severity (CRITICAL/HIGH/MEDIUM), root-cause hypothesis, one recommended action each.
5. **Recommend** — one constraint-focused intervention per Goldratt's "subordinate everything to the constraint". Never optimize a non-constraint stage.

## Assumptions

User can give stage-level cycle-time data (even rough P50/P90 — if not, instrument first) · "process" = repeatable workflow with discrete stages, not a one-off project · user can act on bottlenecks · stage `type` is honest (mis-labelling waiting as value-add is the most common data-quality failure).

## Anti-Patterns

Mapping every process at once (pick one — the constraint is a single point) · optimizing the non-constraint (speeding stage 2 when stage 4 is the bottleneck just builds inventory in front of 4) · mistaking total cycle time for processing time (VA% reveals the gap) · adding people to a wait-bound process (wait is solved by removing the handoff/batch, not headcount) · treating rework as a separate problem (rework loops belong in the map).

## Forcing Questions (one at a time, recommended answer + canon)

1. **Measured cycle times for the top-3 longest stages, or estimates?** → insist on measured data. (Goldratt 1984 — optimizing estimated bottlenecks attacks the wrong constraint.)
2. **Mapping as-is or to-be?** → as-is first; to-be after the bottleneck is identified. (Rother & Shook, *Learning to See* — VSM starts with current state.)
3. **Where do handoffs occur, and how long does each wait?** → log every handoff with median wait. (Reinertsen 2009 — wait at handoffs is the largest invisible cost.)
4. **What's your batch size per stage?** → drive toward 1. (Anderson, *Kanban* — batch size correlates 1:1 with cycle-time variance.)
5. **What's the rework rate per stage?** → surface explicitly; rework loops belong in the map. (Pyzdek — hidden rework drives 30-50% of cycle time in service processes.)

Walk depth-first. After all 5 are locked, run map → bottleneck-detect → cycle-time in sequence.
