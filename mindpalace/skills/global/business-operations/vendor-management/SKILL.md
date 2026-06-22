---
name: Vendor Management
description: Use when reviewing, scoring, or auditing third-party SaaS/vendor relationships — vendor scorecards with industry tuning, SLA-compliance tracking with credit-claim flags, third-party risk classification, and KEEP/REVIEW/REPLACE recommendations.
tags: [vendor-management, vendor-scorecard, sla-compliance, third-party-risk, tprm, saas-management, renewal-review, vendor-health]
source: alirezarezvani/claude-skills
derived_from: business-operations/vendor-management
---

# Vendor Management

BizOps / IT / VMO operator doing **ongoing vendor performance review** — not selection or contract drafting. Score vendors, track SLA compliance, classify third-party risk, recommend KEEP/REVIEW/REPLACE. Enables quarterly/rolling reviews so the renewal decision is half-made before the contract comes due.

## When NOT to use

New contract terms → legal · outbound proposal/RFP → sales · spend categorization / duplicate-SaaS → procurement-optimizer · internal system SLOs → reliability engineering.

## Workflow

1. **Intake catalog** — per vendor: name, category, annual_spend, contract_end_date, `criticality` (tier-1 business-stops / tier-2 workaround-exists / tier-3 nice-to-have), uptime_pct, support_response_hours_p90, incident_count_12m, security_certs (SOC2/SOC2-Type-II/ISO27001/HIPAA/PCI-DSS/FedRAMP/GDPR-DPA/CCPA), renewal_terms.
2. **Score each 0-100** across 5 dimensions weighted by industry profile (SaaS/Fintech/Healthcare/Enterprise): Reliability (uptime+incidents 25-30%) · Support (P90 response 15-20%) · Security (certs 25-35%) · Commercial (renewal flexibility 10-15%) · Strategic fit (criticality vs spend 15%). Verdict: KEEP (≥75, routine renewal) · REVIEW (50-74, schedule QBR before renewing) · REPLACE (<50, start alternatives search, don't auto-renew).
3. **Measure SLA compliance** — per record: compliance % vs target (month, quarter), trend (improving/stable/degrading), **credit-claim eligibility flag** (breach_count_12m ≥ 2 OR actual_last_quarter < target by >0.5pp).
4. **Classify third-party risk** — Critical/High/Medium/Low across 4 vectors: data sensitivity (PII/PHI/cardholder/source), financial exposure (spend × tier), operational dependency (tier-1 + no break-glass = Critical), regulatory exposure (profile-weighted, e.g. healthcare HIPAA-without-BAA = Critical). Output: risk matrix + per-vendor mitigations.
5. **Synthesize** — top 3 KEEP wins, top 3 REVIEW conversations, top 3 REPLACE candidates, all claimable SLA credits (with $ estimate), all Critical-risk vendors with no mitigation.

## Key Rule

Output artifacts are inputs to a human decision, not the decision. The point of deterministic tools: two operators score the same catalog the same way.

## Anti-Patterns

Treat all vendors at the same tier · annual review is enough (tier-1 quarterly, tier-2 semi-annual, tier-3 at renewal) · trust the security questionnaire without the SOC2 report · no break-glass for a tier-1 vendor · forget offboarding (data deletion + access revocation — SolarWinds/Okta) · score by gut feel.

## Forcing Questions (one at a time, recommended + canon)

1. **Tier-1 threshold — by spend or operational dependency?** → operational dependency (Gartner TPRM; Target/HVAC breach — spend-only tiering misses critical low-spend vendors).
2. **For tier-1, in-hand SOC 2 Type II (<12mo old) or just the questionnaire?** → insist on the report (NIST SP 800-161; Shared Assessments SIG).
3. **72-hour break-glass if a tier-1 disappears tomorrow?** → documented + annually tested (NotPetya/M.E.Doc; log4j).
4. **When was the SLA last actually invoked (credit claimed)?** → if never, audit whether terms are weak or breaches unreported (Atlassian SLA; ITIL v4).
5. **Is the offboarding checklist current — data deletion, access revocation, key rotation?** → rehearse on one vendor per quarter (SolarWinds; Okta 2022).
6. **Regulatory blast-radius — HIPAA/GDPR/SOX/PCI?** → surface explicitly; weights security scoring (ISO/IEC 27036).
