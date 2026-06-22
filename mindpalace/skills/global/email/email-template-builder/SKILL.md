---
name: Transactional Email Template Builder
description: Use when adding transactional email to a product, migrating email providers, refactoring legacy templates, or adding i18n — React Email templates, Resend/Postmark/SendGrid/SES, dark mode, spam optimization, tracking.
tags: [transactional-email, react-email, resend, postmark, sendgrid, ses, email-templates, i18n, spam-optimization, deliverability]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/email-template-builder
---

# Transactional Email Template Builder

Complete transactional email systems: React Email templates, multi-provider sending, preview server, i18n, dark mode, spam optimization, analytics. Output for Resend/Postmark/SendGrid/AWS SES.

## Project Structure
`emails/components/{layout,partials}` · `templates/` (welcome, verify-email, password-reset, invoice, notification, weekly-digest) · `lib/send.ts` + `lib/providers/` + `lib/tracking.ts` · `i18n/{en,de}.ts` · `preview/server.ts`.

## Base Layout
`@react-email/components` Html/Head/Body/Container. Embed dark-mode `@media (prefers-color-scheme: dark)` overrides with `!important` (overrides inline styles). Brand header (logo `<Img>`), content section, footer (address + `{{unsubscribe_url}}` + privacy). Custom `<Font>` with fallback.

## Templates
Welcome: heading + body + CTA `<Button href={confirmUrl}>` + "button not working?" plain link + benefits list. Invoice: meta box (date/due/amount), line-items table (`<Row>`/`<Column>`, even/odd row tints), total, download PDF button; use `Intl.NumberFormat` for currency, amounts in cents (`/100`).

## Unified Send
Typed `EmailPayload` discriminated union → `render(component(props))` → `addTrackingParams` → provider `send` with `from`, `to`, `subject`, `html`, tags. Swap providers behind one interface.

## i18n
Per-locale typed translation objects with functions (`preview: (name) => ...`); pick `locale === "de" ? de : en` in template.

## UTM Tracking
`addTrackingParams(html, {campaign})` rewrites all `href` with utm_source/medium/campaign params (handles existing `?` vs new).

## Spam Score Checklist
SPF + DKIM + DMARC on sender domain · from address on own domain · subject <50 chars, no ALL CAPS / "FREE!!!" · 60%+ text-to-image ratio · plain-text version included · unsubscribe link (CAN-SPAM/GDPR) · no URL shorteners · no red-flag words ("guarantee", "no risk", "limited time") · single CTA · alt text on images · valid HTML · test Mail-Tester.com (target 9+/10).

## Pitfalls
Inline styles required (clients strip `<head>`) · max 600px width (Gmail mobile) · no flexbox/grid (use Row/Column) · dark mode needs `!important` · always populate plain-text field · separate sending domains/IPs for transactional vs marketing (protect deliverability).
