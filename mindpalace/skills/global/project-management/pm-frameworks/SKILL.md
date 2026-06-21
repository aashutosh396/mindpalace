---
name: pm-frameworks
description: "Use when doing product-management work — writing a PRD, user story, press release, or positioning statement; running discovery, JTBD, opportunity solution trees, or customer interviews; prioritizing with RICE/ICE/Kano/MoSCoW; roadmap or epic breakdown; stakeholder mapping; SaaS finance/growth metrics; TAM-SAM-SOM; PESTEL; or PM career/leadership transitions."
version: 1.0.0
license: CC-BY-NC-SA-4.0
tags: [product-management, prd, prioritization, discovery, jtbd, roadmap, user-story, stakeholders, saas-metrics, positioning]
source: https://github.com/deanpeters/Product-Manager-Skills
derived_from: awesomeclaude
---

# PM Frameworks

A library of ~52 battle-tested product-management frameworks (Dean Peters,
"Product Manager Skills", v0.80). Each framework is a self-contained procedure:
the *why*, the structure, the failure modes, and the judgment to apply it.
Goal is dual — produce professional PM artifacts AND teach the reasoning.

## When to use

Pick the framework that matches what the user is trying to accomplish, then
apply its structure. Do NOT produce generic PM output — use the right lens.
Most "advisor" skills are interactive: ask 3-5 context questions first, then
recommend/produce. Most "component" skills are templates you fill in.

## Framework index (by job-to-be-done)

**Framing & strategy**
- `problem-framing-canvas` — MITRE Look Inward / Look Outward / Reframe; stop solving the wrong problem
- `problem-statement` — crisp single-sentence problem articulation
- `positioning-statement` / `positioning-workshop` — Geoffrey Moore "For… who… our product… that… unlike…" template
- `product-strategy-session` — full arc: positioning → framing → solutions → roadmap (multi-week)
- `recommendation-canvas` — structure a build/strategy recommendation for execs
- `pestel-analysis` — macro-environment scan (Political/Economic/Social/Tech/Environmental/Legal)

**Customer discovery & research**
- `jobs-to-be-done` — functional/social/emotional jobs + pains + gains (Christensen / VPC). Separates job from solution.
- `proto-persona` — assumption-based persona before research
- `discovery-interview-prep` — plan Mom Test-style interviews from research goals
- `discovery-process` — full frame → research → synthesize → validate cycle
- `opportunity-solution-tree` — Teresa Torres OST: outcome → opportunities → solutions → experiments; pick best POC
- `customer-journey-map` / `customer-journey-mapping-workshop` — stage-by-stage experience map

**Prioritization & roadmapping**
- `prioritization-advisor` — asks context, then recommends RICE / ICE / Value-vs-Effort / Kano / MoSCoW / Weighted / Opportunity Scoring. Avoids "framework whiplash".
- `roadmap-planning` — inputs → epics → prioritize → sequence → communicate
- `epic-breakdown-advisor` / `epic-hypothesis` — split large epics (Richard Lawrence's 9 patterns)
- `user-story-mapping` / `user-story-mapping-workshop` — backbone + slices

**Writing PM deliverables**
- `user-story` — Mike Cohn "As a… I want… so that…" + Gherkin acceptance criteria + anti-patterns
- `user-story-splitting` — break stories to thin vertical slices
- `prd-development` — structured PRD: problem → personas → solution → metrics → stories
- `press-release` — Amazon Working Backwards: write the PR/FAQ before the spec
- `storyboard` — visual narrative of the user experience
- `eol-message` — end-of-life / deprecation comms
- `lean-ux-canvas` — assumptions → hypotheses → MVP

**Validation & experimentation**
- `pol-probe-advisor` — recommend which prototype/probe type given hypothesis + risk
- `pol-probe` — document a lightweight validation experiment ("proof of life")
- `epic-hypothesis` — frame an epic as a testable hypothesis

**Stakeholders**
- `stakeholder-identification` — broad brainstorm → allies/audiences/influencers → R/P/D → equity lens → narrow
- `stakeholder-mapping` — Power×Interest (engagement) + Impact×Power (whose voice) grids; compare to find gaps
- `stakeholder-engagement-advisor` — per-stakeholder message framing, medium, cadence, next action
- `workshop-facilitation` — run any of the above as a facilitated session

**Finance & growth**
- `business-health-diagnostic` — SaaS health across growth / retention / efficiency / capital from real metrics
- `saas-economics-efficiency-metrics` / `saas-revenue-growth-metrics` / `finance-metrics-quickref` — CAC, LTV, NRR, Rule of 40, burn multiple, magic number, etc.
- `finance-based-pricing-advisor` — pricing model from unit economics
- `feature-investment-advisor` — build / don't-build via revenue impact, cost, ROI, strategic value
- `organic-growth-advisor` — McKinsey Growth Pyramid triage (segments / geos / channels / products)
- `acquisition-channel-advisor` — pick acquisition channels for stage
- `tam-sam-som-calculator` — market sizing (top-down + bottom-up)
- `company-research` — structured company/market research

**AI product work**
- `ai-shaped-readiness-advisor` — AI-first (automate tasks) vs AI-shaped (redesign work); which competency first
- `context-engineering-advisor` — context stuffing vs context engineering; memory architecture
- `agent-orchestration-advisor` — multi-agent workflow design (4 dimensions)
- `product-sense-interview-answer` — structure a product-sense interview answer

**Career & leadership**
- `altitude-horizon-framework` — Altitude (scope) × Horizon (time) model for PM→Director thinking
- `director-readiness-advisor` — PM→Director transition (preparing / interviewing / landed / recalibrating)
- `vp-cpo-readiness-advisor` — Director→VP/CPO, incl. CEO-interview framework for evaluating a role
- `executive-onboarding-playbook` — 30-60-90 day VP/CPO diagnostic

**Authoring**
- `pm-skill-creator` / `skill-authoring-workflow` — create new PM skills in this format

## How to apply

1. Identify the user's actual goal and match it to ONE framework above (or a
   short chain, e.g. positioning → problem-framing → OST for a strategy ask).
2. Fetch that framework's full procedure when you need the detailed steps:
   `https://raw.githubusercontent.com/deanpeters/Product-Manager-Skills/main/skills/<name>/SKILL.md`
3. For `*-advisor` skills, ask the context questions FIRST, then recommend.
4. Fill the template with the user's real context; never hand back the blank.

## Gotchas

- Don't default to RICE/PRD for everything — let `prioritization-advisor` /
  the index choose the fitting tool.
- These are pedagogic: state the *why* and the failure mode, not just the output.
- License is CC BY-NC-SA 4.0 — non-commercial, attribute Dean Peters, share-alike.
  Don't repackage commercially.
- Full bodies (key concepts, step procedures, examples) live in each skill's
  SKILL.md at the source path above; this file is the router/index, not a copy.
