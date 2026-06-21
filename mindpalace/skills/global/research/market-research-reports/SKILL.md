---
name: market-research-reports
description: "Use when producing a comprehensive market or industry research report in consulting-firm style. Triggers: 'market research report', 'industry analysis', 'competitive landscape', 'market sizing', 'TAM SAM SOM', 'Porter's Five Forces', 'PESTLE', 'SWOT', 'BCG matrix', 'go-to-market analysis', 'market entry', 'due diligence report', 'investment thesis', 'sector report'. Produces a long-form, framework-driven, visually structured strategic document."
version: 1.0.0
license: MIT
tags: [market-research, competitive-analysis, tam-sam-som, porters-five-forces, pestle, swot, bcg-matrix, strategy, go-to-market]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/market-research-reports
derived_from: awesomeclaude
---

# Market Research Reports

## What it does
Generates a professional-grade market/industry research report modeled on deliverables from McKinsey, BCG, Bain, Gartner, and Forrester: deep, data-driven, framework-led, and visually structured, ending in actionable recommendations and an implementation roadmap. Built for long-form output (the upstream targets 50+ pages); scale the depth to the ask — a one-pager and a full report use the same structure.

## When to use
- Market analysis for an investment, entry, or strategic decision
- Competitive landscape and market dynamics analysis
- Market sizing (TAM/SAM/SOM)
- M&A due diligence material
- Go-to-market strategy or new-product business case
- Industry thought-leadership content
- Regulatory/policy impact analysis on a market

## Strategic frameworks (the analytical backbone)
- **TAM / SAM / SOM** — Total / Serviceable Addressable / Serviceable Obtainable Market; size the opportunity in concentric layers with explicit assumptions.
- **Porter's Five Forces** — competitive rivalry, threat of new entrants, supplier power, buyer power, threat of substitutes; rate each High/Medium/Low with justification.
- **PESTLE** — Political, Economic, Social, Technological, Legal, Environmental macro factors.
- **SWOT** — Strengths, Weaknesses, Opportunities, Threats.
- **BCG Growth-Share Matrix** — stars / cash cows / question marks / dogs for portfolio or segment positioning.
- **Competitive positioning matrix** — map players on two decision-relevant axes.

## Recommended structure
**Front matter:** cover, table of contents, executive summary (market snapshot box, 3-5 bullet investment thesis, key findings, top 3-5 recommendations).

**Core analysis:**
1. **Market Overview & Definition** — scope, segmentation, key terms
2. **Market Size & Growth** — current size, historical and forecast CAGR, TAM/SAM/SOM, regional/segment breakdown
3. **Market Dynamics** — drivers, restraints, trends, PESTLE
4. **Competitive Landscape** — Five Forces, key players, market share, positioning matrix, strategic groups
5. **Customer / Demand Analysis** — segments, needs, buying behavior
6. **Risk Analysis** — risk heatmap, mitigation
7. **Strategic Recommendations** — opportunity/prioritization matrix, actions
8. **Implementation Roadmap** — phased timeline with milestones

**Back matter:** methodology, sources, appendix.

## Visuals
Anchor the report with a handful of priority diagrams generated up front, then add more as sections demand: growth trajectory chart, TAM/SAM/SOM concentric circles, Porter's Five Forces, competitive positioning matrix, risk heatmap, plus an executive-summary infographic. Use whatever diagramming tool is available (mermaid, matplotlib, draw.io, or an image generator); the upstream pairs with scientific-schematics / generate-image skills when present.

## Best practices
- **Lead with the thesis.** The executive summary must stand alone.
- **Every number has a source and an assumption.** Market sizes are estimates — show the math (e.g., TAM = users x ARPU).
- **Frameworks serve the argument**, not the other way around — don't include a SWOT just to have one.
- **End on action.** Recommendations must be specific, prioritized, and sequenced.
- Cite sources; flag confidence levels where data is thin.
