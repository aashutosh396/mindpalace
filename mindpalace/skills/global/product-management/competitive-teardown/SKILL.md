---
name: Competitive Teardown
description: Use when conducting competitor analysis, building sales battle cards, preparing a strategy/roadmap session, or responding to a competitor's new feature/pricing — synthesizes pricing, reviews, job postings, SEO, and social into a scored 12-dimension teardown.
tags: [competitive-analysis, competitor, teardown, battle-card, swot, feature-matrix, positioning-map, market-analysis, ux-audit]
source: alirezarezvani/claude-skills
derived_from: product-team/competitive-teardown
---

# Competitive Teardown

Synthesize competitor signals (pricing pages, app-store reviews, job postings, SEO, social) into structured competitive intelligence.

## When to Use

Before a strategy/roadmap session; when a competitor launches a major feature or pricing change; quarterly review; before a sales pitch needing battle-card data; when entering a new segment.

## Workflow

1. **Define competitors** — 2-4, confirm the primary focus.
2. **Collect data** — ≥3 sources per competitor. *Checkpoint:* have pricing, ≥20 reviews, job-posting counts for each.
3. **Score using rubric** — 12-dimension scorecard for each competitor + your own product. *Checkpoint:* every dimension has a score + ≥1 evidence note.
4. **Generate outputs** — Feature Matrix, Pricing Analysis, SWOT, Positioning Map, UX Audit.
5. **Build action plan** — quick wins / medium-term / strategic.
6. **Package for stakeholders** — 7-slide presentation.

## Data Sources (what to capture)

- **Website** — pricing tiers + price points, features per tier, primary CTA/messaging, case studies/logos (ICP signal), integrations, trust signals.
- **App-store reviews** — categorize: praise (defend/strengthen), feature requests (opportunity gaps), bugs (quality), UX complaints (friction to beat). (iTunes Search API → trackId → customer-reviews RSS.)
- **Job postings** — eng volume (scaling vs consolidating), tech mentions (stack), sales/CS ratio (PLG vs sales-led), data/ML roles (AI features), compliance roles (regulatory expansion).
- **SEO** — top 20 organic keywords + intent, Domain Authority/backlinks, blog cadence/topics, which pages rank.
- **Social** — recurring praise/complaints/requests via X/Reddit/LinkedIn.

## Scoring Rubric (12 dimensions, 1-5)

Features · Pricing · UX · Performance · Docs · Support · Integrations · Security · Scalability · Brand · Community · Innovation. (1 = weak, 3 = average, 5 = best-in-class.) Anchor every score to an evidence note (e.g. "UX 2 — reviews cite confusing navigation 38×; onboarding 7 steps before TTFV").

## Output Templates

- **Feature Matrix** — rows = core features/tiers/platform caps; columns = you + ≤3 competitors; score 1-5, sum out of 60.
- **Pricing Analysis** — model type, entry/mid/enterprise price, trial length; summarize price leader / value leader / premium / your position + 2-3 pricing opportunities.
- **SWOT** — 3-5 bullets per quadrant, each anchored to a data signal.
- **Positioning Map** — 2×2 axes, place each competitor + you, bubble size = share/funding.
- **UX Audit** — onboarding (TTFV, steps, CC-required, wizard), key-workflow steps + friction, mobile parity, navigation (search/shortcuts/help).
- **Action Items** — quick wins (0-4wk, low effort) / medium-term (1-3mo) / strategic (3-12mo).

## Stakeholder Presentation (7 slides)

1. Executive Summary (threat level LOW/MED/HIGH/CRITICAL + top strength/opportunity/action) · 2. Market Position (2×2) · 3. Feature Scorecard (radar/table totals) · 4. Pricing Analysis · 5. UX Highlights (their wins vs your wins) · 6. Voice of Customer (top 3 review complaints) · 7. Action Plan (+ raw-data appendix).
