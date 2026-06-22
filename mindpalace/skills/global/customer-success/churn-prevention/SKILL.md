---
name: Churn Prevention
description: Use when designing or optimizing a cancel flow, save offers, exit surveys, dunning/failed-payment recovery, or win-back — reduces voluntary and involuntary SaaS churn.
tags: [churn, cancel-flow, save-offers, dunning, exit-survey, payment-recovery, win-back, involuntary-churn, failed-payments, retention]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/churn-prevention
---

Reduce voluntary churn (decided to leave) and involuntary churn (payment failed). A 20% save rate on voluntary + 30% recovery on involuntary recovers 5-8% of lost MRR monthly. (For health scoring/expansion use customer-success-manager.)

## Modes
Build cancel flow (none exists) · optimize existing (low save rates) · set up dunning (failed-payment priority).

## Cancel flow (not a dark pattern — a structured conversation)
`[Trigger] → [Exit Survey] → [Dynamic Save Offer] → [Confirmation] → [Post-Cancel]`
1. **Trigger** — show cancel clearly; start the flow at click, not a dead-end form.
2. **Exit survey** — ONE required multiple-choice question (6-8 reasons); collected before offer.
3. **Dynamic save offer** — match offer to reason; one per attempt; if declined, let them cancel.
4. **Confirmation** — clear summary (access/data/billing), explicit button, no pre-checked boxes.
5. **Post-cancel** — immediate confirmation email (date, retention policy, reactivation link) + 7-day re-engagement (single CTA) + 30-day win-back if warranted.

## Exit reason → save offer mapping (one offer per reason)
Too expensive → discount/downgrade · not using → usage tips + pause · missing feature → roadmap + workaround · switching → competitive comparison · project ended → pause · too complicated → onboarding help + human support · just testing → no offer, let go.

## Save offer rules
Discount (price objection only) · Pause (seasonal/not-using) · Downgrade (too expensive + light usage) · Extended trial (hasn't explored value) · Feature unlock (missing feature on higher plan) · Human support (frustrated, not price). Quantify value ("Save $X"), no fake countdowns, clear CTA vs "continue cancelling."

## Dunning (involuntary — 20-40% of total churn, mostly recoverable)
- **Smart retry:** retry 3 days after failure (most recoveries), then +5, then +7, final +3 then cancel.
- **Card updater:** enable Stripe/Braintree Account Updater.
- **Email sequence:** Day 0 "Payment failed" (neutral) · Day 3 "Action needed" · Day 7 "Account at risk" · Day 12 "Final notice" + support · Day 15 "Paused/cancelled" → reactivate. Specific subjects, no guilt, link directly to payment-update page (not dashboard).

## Metrics & benchmarks
Save rate 10-15% good / 20%+ excellent · voluntary churn <2%/mo · involuntary <1%/mo · recovery rate 25-35% · win-back 5-10% · exit-survey completion >80%.
Red flags: save <5% (offers not matching reasons) · survey completion <70% (too long/optional) · recovery <20% (retry/emails weak) · churn >5%/mo (flag for product/ICP review — prevention alone won't fix).

## Proactive flags
Instant cancellation (revenue leaking) · single generic save offer · no dunning sequence · optional exit survey · no post-cancel reactivation email.
