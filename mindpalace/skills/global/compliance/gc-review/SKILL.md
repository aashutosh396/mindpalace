---
name: General Counsel Review — Legal Forcing Questions
description: Use when reviewing a term sheet before signing, redlining a customer MSA, or checking IP assignment and regulatory exposure on a new product — six GC forcing questions on contracts, IP, data, termination, regulatory surface, and employment/equity.
tags: [legal, contracts, term-sheet, ip-assignment, indemnity, dpa, gdpr, regulatory, equity, general-counsel]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/gc-review
---

# General Counsel Forcing Questions

Six questions before any contract, term sheet, IP move, or regulatory commitment. A single missed clause can cost more than a year of engineering.

> Not legal advice. Surfaces the right questions to ask before engaging qualified counsel for binding decisions.

## When to run
- Before signing any contract >$100K or >1 year; before issuing equity; before a term-sheet response.
- Before entering a regulated market (healthcare, fintech, defense); before an OSS license decision in core IP; before an M&A LOI.

## The six questions
1. **IP Ownership** — work-for-hire vs license vs joint? Written IP assignment for employees/contractors in place? OSS license compatibility checked?
2. **Liability & Indemnity** — what's the liability cap, and what's carved out? Standard cap: 12 months of fees. Carve-outs: IP infringement, data breach, willful misconduct. Mutual indemnity desirable.
3. **Data Processing** — what personal data is involved, and is a DPA in place? GDPR/CCPA scope, subprocessor flow-down, data residency.
4. **Termination & Renewal** — termination right, notice period, auto-renew trap? For convenience vs cause; 30/60/90-day notice.
5. **Regulatory Surface** — does this expose a new regime? Healthcare→HIPAA; fintech→BSA/AML, money-transmitter; medical device→FDA/MDR/ISO 13485; data→GDPR/CCPA/breach laws.
6. **Employment/Equity** — jurisdiction, classification, equity grant, IP assignment? Misclassification risk; standard 4-year vest/1-year cliff; acceleration triggers; 409A current?

## Output format
```markdown
# GC Review: <plan>
## Document — type / counterparty / $ value
## Issues
| # | Issue | Risk | Recommendation |
|---|---|---|---|
| 1 | uncapped IP indemnity | HIGH | cap at fees, mutual |
## Regulatory Trigger — new regime? frameworks
## Outside Counsel Action Items — [ ] item 1 …
## Verdict — 🟢 SIGN AS-IS (rare) | 🟡 NEGOTIATE top-3 | 🔴 DO NOT SIGN
```
