---
name: Form CRO
description: Use when optimizing a non-signup form — lead capture, contact, demo request, application, survey, or checkout — maximizes completion rate while capturing the data that matters.
tags: [form optimization, lead form, contact form, form conversion, form fields, form friction, cro, demo request]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/form-cro
---

# Form CRO

Maximize form completion while capturing the data that matters. (For account-creation forms use signup-flow CRO; for forms inside modals use popup CRO.)

## Initial assessment
Form type (lead capture / contact / demo / application / survey / checkout / quote) · current state (field count, completion rate, mobile/desktop split, abandonment point) · business context (what happens with submissions, which fields are actually used, compliance requirements).

## Core principles (thresholds that drive every audit)
- **Field count** — every field costs conversions. Lead-gen ceiling: 3-5 fields; 7+ required = high-priority finding unless qualification value is proven.
- **Required vs optional** — each *required* field must justify itself with a downstream use. "Nice for sales" isn't justification — make it optional or cut it.
- **High-friction fields** — phone, company size, address are the biggest abandonment drivers top-of-funnel; demand justification or defer to step 2 / progressive profiling.
- **Error recovery** — inline validation on blur (not submit), specific copy ("Enter a work email," not "Invalid input"), never clear filled fields on error.
- **CTA** — value-specific ("Get my report") beats generic ("Submit").

## Output: Form Audit (Issue / Impact / Fix / Priority)
Each issue: what's wrong · estimated effect on conversions · specific fix · High/Medium/Low. Plus: recommended field set (justified required + optional), field order, copy (labels/placeholders/button/errors), layout, and A/B test hypotheses.

## Experiment ideas
- **Structure/flow**: single vs multi-step (progress bar), 1- vs 2-column, embedded vs separate page, above-fold vs after-content.
- **Field optimization**: minimum viable fields, add/remove phone, add/remove company, required/optional balance, field enrichment auto-fill, hide fields for known visitors.
- **Smart forms**: real-time validation, progressive profiling, conditional fields, auto-suggest company names.
- **Copy/design**: label clarity, placeholder/help-text, error tone, button text/color/placement, trust elements (privacy, badges, testimonial, response time).
- **By type**: demo (phone requirement test, "preferred contact," "biggest challenge?", calendar embed) · lead capture (email-only vs +name, gated vs ungated) · contact (department routing, message-field requirement, alt contact methods).
- **Mobile/UX**: larger touch targets, correct keyboard per field, sticky submit, auto-focus first field.

## Communication standard
Every field recommendation justified (never just "remove fields"). Issue/Impact/Fix/Priority structure. Multi-step vs single-step always includes the qualifying criteria. Mobile addressed separately from desktop. Min 3 submit-button copy options with reasoning. Error rewrites when error handling is flagged.

## Proactive triggers
"Lead form isn't converting" → field audit + core principles. Demo/contact page being built → offer review. "Leads but bad quality" → wrong fields / missing qualification. Mobile gap detected → mobile checklist. 7+ fields → flag field-cost framework + multi-step.
