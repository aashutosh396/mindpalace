---
name: experimental-design
description: "Use when planning a study or experiment BEFORE collecting data — choosing a design, randomizing, blocking, and laying out treatment combinations so results are interpretable. Triggers: 'how should I set up this experiment', 'A/B test design', 'randomize', 'avoid confounding', 'control group', 'factorial design', 'DOE', 'design of experiments', 'how do I test these N factors', 'blocking', 'stratification', 'crossover', 'split-plot', 'Latin square', 'run order', 'pseudoreplication'. For sample size use statistical-power; for analyzing collected data use statistical-analysis."
version: 1.0.0
license: MIT
tags: [experimental-design, doe, randomization, ab-testing, blocking, factorial, confounding, controls, study-planning]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/experimental-design
derived_from: awesomeclaude
prerequisites: "Python 3.10+ with numpy>=1.26, pandas>=2.0, pyDOE3 (for DOE matrices)."
---

# Experimental Design

## What it does
Helps you design a study before data collection so the results can actually answer the question. The design — how units are assigned to conditions, what's held constant, what's varied, in what structure — determines what the data can prove. No analysis fixes a confounded or pseudoreplicated design afterward. Applies to product A/B/multivariate tests, marketing experiments, lab studies, and any comparative trial.

## Fisher's three principles
- **Randomization** — assign treatments at random so confounders (known and unknown) balance out. This turns a comparison into a causal claim.
- **Replication** — independent repetition at the right level. The fatal error is **pseudoreplication**: treating repeated measurements of one unit as independent replicates.
- **Blocking / local control** — group similar units (by batch, day, site, cohort) and randomize within blocks, removing nuisance variation from the error term.

## When to use
- Planning any comparative experiment and deciding how to assign units
- Randomizing to arms (simple, blocked, stratified, cluster)
- Multi-factor experiments: full / fractional factorial, screening designs
- Optimizing a response over continuous factors (response-surface)
- Within-subject / repeated-measures, crossover, split-plot, Latin-square
- Cluster/group-randomized designs
- Deciding number and level of replicates; avoiding pseudoreplication

## Choosing a design (quick map)
- Compare a few fixed conditions → **randomized (optionally blocked) design**
- Test many factors cheaply, main effects only → **fractional factorial / Plackett-Burman screening**
- All effects + interactions among a few factors → **full factorial**
- Find settings that OPTIMIZE a response (curvature) → **response-surface: central composite or Box-Behnken**
- Explore a simulation over continuous space → **space-filling: Latin hypercube**

## Generating the layout (reproducible, seeded)
Allocation schedules:
- **Simple** randomization — fine for large n, can drift to imbalance with small n
- **Block** (permuted blocks) — guarantees balance throughout enrollment; use for small n or sequential intake
- **Stratified block** — additionally balances a known prognostic factor across arms
- **Cluster** — mandatory when the intervention is delivered at a group level (the cluster is the unit)

DOE matrices return designs in real units from `{factor: (low, high)}` ranges; **run order is randomized by default** so factors aren't confounded with time/drift. Seed everything so the exact schedule can be archived and regenerated.

## Mistakes that ruin studies (structural — unfixable in analysis)
1. **Pseudoreplication** — 3 subjects x 100 measurements is n=3, not n=300, for any treatment applied at the subject level. Replicate at the level the treatment is randomized; analyze with the nesting respected (mixed model).
2. **Confounding by a nuisance variable** — all treatment on Monday, all control on Tuesday confounds treatment with day. Randomize across or block on every nuisance factor (batch, day, cohort, operator, instrument).
3. **No / broken randomization** — convenience assignment lets confounders in. Use a seeded schedule and follow it.
4. **No proper control** — without a concurrent control (and blinding where possible) you can't separate treatment from time/placebo/handling effects.
5. **Batch effects mistaken for signal** — randomize/block processing order across batches; never let batch align with condition.
6. **Aliasing ignored in fractional designs** — low-resolution fractional factorials confound main effects with interactions; know the alias structure before declaring a factor inert.
7. **Optimizing without curvature** — a two-level factorial can't detect a curved response; use a response-surface design for an interior optimum.
