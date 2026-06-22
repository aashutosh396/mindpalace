---
name: Signup Flow CRO
description: Use when optimizing signup, registration, account creation, or trial activation flows — reduces friction, increases completion, and sets users up for activation.
tags: [signup conversion, registration, account creation, free trial, signup friction, cro, sso, activation]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/signup-flow-cro
---

# Signup Flow CRO

Reduce friction, increase completion, set users up for successful activation. (For post-signup onboarding use onboarding CRO; for non-account lead-capture forms use form CRO.)

## Initial assessment
Flow type (free trial / freemium / paid / waitlist; B2B vs B2C) · current state (steps/screens, required fields, completion rate, drop-off point) · constraints (data genuinely needed at signup, compliance, what happens immediately after).

## Output format
- **Audit findings** — Issue / Impact (with estimate) / Fix / Priority.
- **Recommended changes** — Quick wins (same-day) → High-impact (week-level) → Test hypotheses (A/B).
- **Form redesign (if requested)** — field set with rationale, order, copy (labels/placeholders/buttons/errors), layout.

## Common patterns
- **B2B SaaS trial**: email + password (or Google auth) → name + company (optional role) → onboarding.
- **B2C app**: Google/Apple auth OR email → product experience → profile later.
- **Waitlist**: email only → optional role/use-case → confirmation.
- **E-commerce**: guest checkout default → account optional post-purchase OR one-click social auth.

## Experiment ideas
- **Layout/structure**: single vs multi-step (progress bar), 1- vs 2-column, embedded vs separate page.
- **Field optimization**: minimum (email + password), add/remove phone, single Name vs First/Last, add/remove company, required/optional balance.
- **Authentication**: add SSO (Google/Microsoft/GitHub/LinkedIn), SSO vs email prominence, which SSO resonates by audience, SSO-only vs SSO+email.
- **Copy/messaging**: headline above form, CTA text ("Create Account" vs "Start Free Trial" vs "Get Started"), trial length in CTA, value-prop emphasis, microcopy, password requirement display, "No credit card required," privacy assurance.
- **Trial & commitment**: credit card required vs not, trial length (7/14/30d), freemium vs trial, limited vs full access.
- **Friction**: email verification required vs delayed vs removed, CAPTCHA impact, terms checkbox vs implicit, phone verification for high-value.
- **Post-submit**: clear next steps, instant access vs email-first, personalized welcome, auto-login vs require login.

## Communication standard
Quick Wins → High-Impact → Test Hypotheses (never flat). Every field removal justified against "do we need this before they can use the product?" SSO always considered/recommended when relevant (don't default to email-only). Post-submit experience always addressed (it's part of the flow). Mobile as a distinct section. Distinguish "fix this" (obvious) from "test this" (uncertain).

## Proactive triggers
"Sign up but don't activate" → audit full signup→activation path. "Trial conversion low" → check expectations/wrong users at signup. New trial/freemium being built → offer pre-launch review. "Should we require a credit card?" → full friction + commitment analysis. High mobile drop-off on signup → mobile signup checklist.
