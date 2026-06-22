---
name: Tech Stack Evaluator
description: Use when comparing frameworks/stacks, calculating total cost of ownership, assessing migration paths, or analyzing ecosystem viability — weighted comparison, 5-year TCO, security + ecosystem scoring.
tags: [tech-stack, framework-comparison, tco, migration-analysis, ecosystem-health, build-vs-buy, technology-evaluation, cloud-comparison, decision-matrix]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/tech-stack-evaluator
---

# Tech Stack Evaluator

Data-driven comparison of technologies, frameworks, cloud providers with actionable recommendations.

## Capabilities
- **Technology comparison**: weighted scoring across criteria (e.g. developer productivity 40%, ecosystem 30%, performance 30%).
- **TCO analysis**: 5-year total including hidden costs (team size, hosting, growth rate).
- **Ecosystem health**: GitHub metrics, npm adoption, community strength.
- **Security assessment**: vulnerabilities + compliance readiness (SOC2/GDPR).
- **Migration analysis**: effort, risks, timeline (codebase size, component count, team size).
- **Cloud comparison**: AWS/Azure/GCP for specific workloads.

## Input Formats
Natural-language query, structured YAML (technologies + use_case + weights), or JSON.

## Analysis Depth
Quick (200-300 tokens): weighted scores + recommendation + top 3 factors + confidence. Standard (500-800): comparison matrix + TCO overview + security summary. Full (1200-1500): all metrics + migration + detailed recommendations.

## Confidence Levels
High 80-100% (clear winner, strong data) · Medium 50-79% (trade-offs, moderate uncertainty) · Low <50% (close call, limited data).

## When to Use / NOT Use
Use for: comparing frameworks for new projects, evaluating cloud providers for workloads, planning migrations with risk assessment, build-vs-buy with TCO, OSS library viability. NOT for: trivial decisions between similar tools (use team preference), mandated choices (already decided), emergency production issues (use monitoring).
