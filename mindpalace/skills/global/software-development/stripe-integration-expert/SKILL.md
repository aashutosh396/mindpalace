---
name: Stripe Integration Expert
description: Use when integrating Stripe for the first time, debugging webhook reliability, migrating payment providers, or adding usage-based billing — subscriptions, proration, idempotent webhooks, customer portal, Next.js/Express/Django.
tags: [stripe, billing, subscriptions, webhooks, proration, usage-based-billing, checkout, customer-portal, payments, idempotency]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/stripe-integration-expert
---

# Stripe Integration Expert

Production Stripe: subscriptions (trials, proration), one-time + usage-based billing, idempotent webhooks, customer portal, invoicing. Next.js/Express/Django.

## Subscription State Machine
`FREE_TRIAL →paid→ ACTIVE →cancel→ CANCEL_PENDING →period_end→ CANCELED`. Downgrade → DOWNGRADING → ACTIVE(lower) at period end. Trial-end-no-payment → PAST_DUE → (3 failures) CANCELED. DB statuses: `trialing|active|past_due|canceled|cancel_pending|paused|unpaid`.

## Client Setup
`new Stripe(SECRET_KEY, { apiVersion, typescript: true })`. Store price IDs per plan in env, never hardcode.

## Checkout (Next.js App Router)
Get-or-create Stripe customer (store `stripeCustomerId` in DB, set `metadata.userId`). `checkout.sessions.create`: mode subscription, `subscription_data.trial_period_days` only if `!hasHadTrial`, `allow_promotion_codes`, success/cancel URLs, **always pass `metadata.userId`** (can't link subscription to user without it).

## Upgrade/Downgrade
- Upgrade (immediate): `proration_behavior: "always_invoice"`, `billing_cycle_anchor: "unchanged"`.
- Downgrade (period end): `proration_behavior: "none"`.
- Preview proration with `invoices.retrieveUpcoming` before confirming — show user the amount.

## Idempotent Webhooks (critical)
1. `constructEvent(body, signature, WEBHOOK_SECRET)` — verify signature, 400 on fail.
2. Check processed-events table → skip if seen.
3. Switch on type: `checkout.session.completed`, `customer.subscription.created/updated/deleted`, `invoice.payment_succeeded/failed`.
4. Mark processed on success. **Return 500 on error so Stripe retries — don't mark processed.**
- `payment_failed`: set `past_due`; dunning email (retry < 3, final at 3).
- Webhook order not guaranteed → re-fetch from Stripe API, never trust event data alone for DB writes.

## Usage-Based
`subscriptionItems.createUsageRecord(itemId, { quantity, timestamp, action: "increment" })`. Find metered item via `price.recurring.usage_type === "metered"`.

## Customer Portal
`billingPortal.sessions.create({ customer, return_url })`. Must enable features in Stripe Dashboard → Billing → Customer portal.

## Feature Gating
Active if status active/trialing; grace if past_due AND `currentPeriodEnd > now`.

## Test (Stripe CLI)
`stripe listen --forward-to localhost:3000/api/webhooks/stripe`; `stripe trigger <event>`. Cards: 4242…=success, 4000 0025 0000 3155=auth, 4000…9995=decline.

## Pitfalls
Webhook order · double-processing (idempotency table) · trial abuse (store `hasHadTrial`) · proration surprises (preview first) · portal not configured · missing checkout metadata.
