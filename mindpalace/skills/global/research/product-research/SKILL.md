---
name: Product / User Research
description: Use when planning or synthesizing product/user research — matching method to goal (generative vs evaluative vs validation), sizing samples by saturation with a stated confidence, and synthesizing coded observations into insights while flagging single-source anecdotes.
tags: [user-research, ux-research, jtbd, usability, saturation, insight-synthesis, research-repository, product-discovery]
source: alirezarezvani/claude-skills
derived_from: research-ops/skills/product-research
---

# Product / User Research

Method-and-repository discipline. Core rules: **method must match the goal**, and **an insight requires recurrence across independent participants** — a single quote is an anecdote.

## Workflow
1. **Frame the study** — research questions, method rationale, participant criteria, analysis plan, repository tagging scheme.
2. **Pick the method** — map (goal × product stage) to a method and emit a plan skeleton:
   - goal: discovery (generative interviews) / evaluative (usability test) / validation (concept test)
   - stage: concept / prototype / beta / live
   - Route live A/B to an experiment-design tool, NOT here.
3. **Size it** — method-based sample with explicit confidence:
   - Nielsen problem-discovery: ~5/segment
   - Guest et al. thematic saturation: ~12
   - Never claim a prevalence rate from a small-n usability test.
4. **Synthesize** — code observations, cluster by tag, count DISTINCT participants, rank by cross-participant recurrence. Anything below the source threshold (default 3) is flagged ANECDOTE, never promoted to insight.
5. **File in repository** — tag insights to the atomic schema at synthesis time, with evidence + confidence.

## Anti-patterns
- Mismatching method to goal (a usability test can't discover unmet needs; an interview can't measure task success).
- Reporting usability problems as percentages (small-n surfaces problems, not population rates).
- Promoting an anecdote to an insight (one participant = signal to probe).
- Framing interview questions as feature reactions (probe the job-to-be-done and recent real behavior).
- Synthesizing without a repository scheme (tag now, or insights rot unfindable).

## Forcing questions (one at a time, recommended answer + canon)
1. Generative or evaluative? → name it first; method follows the goal. (Rohrer, NN/g)
2. Sample size + saturation rationale at what confidence? → 5/segment usability, ~12 thematic. (Nielsen; Guest, Bunce & Johnson; Faulkner)
3. How many independent participants per insight? → require ≥3; flag singletons. (atomic research; Braun & Clarke)
4. Tasks framed as jobs or as feature reactions? → jobs + recent real behavior. (Christensen/Ulwick JTBD; Portigal)
5. Where does it land in the repository, tagged how? → atomic schema at synthesis time. (Sharon, *Polaris*)

Distinct from: persona/journey artifacts, discovery-sprint planning, live A/B (those are product-team work), and market sizing/surveys (that studies the market, this studies users).
