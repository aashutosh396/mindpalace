---
name: Analytics Tracking Implementation (GA4 + GTM)
description: Use when setting up, auditing, or debugging analytics tracking — GA4, Google Tag Manager, event taxonomy, conversion tracking, UTM strategy, and consent mode. Produces tracking plans and gap analyses.
tags: [ga4, google tag manager, gtm, event tracking, conversion tracking, tracking plan, utm, consent mode, analytics audit]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/analytics-tracking
---

# Analytics Tracking Implementation

Capture every meaningful customer-journey action accurately and consistently. Bad tracking is worse than no tracking — duplicate events and broken conversions drive bad decisions.

## Gather context
Current state (GA4/GTM set up? tech stack, CMP, events tracked) · business (primary conversions, micro-conversions, paid campaigns) · goals (build/audit/debug, cross-domain, server-side).

## Modes
1. **Set up from scratch** — tracking plan, GA4 + GTM, taxonomy, key events.
2. **Audit existing** — gap analysis, data-quality scorecard, cleanup.
3. **Debug** — missing events, mismatched conversions, GTM-fires-but-GA4-doesn't.

## Event taxonomy (get right before touching GA4/GTM)
**Format**: `object_action` snake_case, verb at end. ✅ `form_submit`, `plan_selected`, `checkout_completed`. ❌ `submitForm`, `FormSubmitted`, `form-submit`. Rules: noun_verb, lowercase+underscores, specific but not a sentence, consistent tense (`_started`/`_completed`/`_failed`).

**Standard params**: page_location, page_title, user_id (link to CRM), plan_name, value + currency, content_group, method.

Core SaaS funnel events: signup_started/completed, trial_started, onboarding_step_completed, feature_activated, plan_selected, checkout_started/completed, subscription_cancelled. Micro: pricing_viewed, demo_requested, form_submitted, content_downloaded, video_started/completed, help_article_viewed.

## GA4 setup
Create property → add web data stream → Enhanced Measurement (disable video/file-download if tracking manually to avoid dupes) → configure all funnel subdomains. Custom events via GTM dataLayer (preferred) over gtag. **Key events** (Admin → Key events, renamed from Conversions Mar 2024): mark signup_completed, checkout_completed, demo_requested, trial_started. Max 30, retroactive 6 months, don't mark micro-conversions unless optimizing ads for them.

## GTM
Container: Tags (GA4 Config on all pages + one GA4 Event tag per event + Google Ads + Meta Pixel) / Triggers (All Pages, DOM Ready, Data Layer Event, Custom Element Click) / Variables (dlv per key, GA4 ID constant, JS variables).
- **Pattern 1 (most reliable)**: app pushes to dataLayer → GTM → GA4.
- **Pattern 2**: CSS-selector click trigger for UI elements without app hooks.

## Conversion tracking
- **Google Ads**: import GA4 conversions (single source of truth); attribution data-driven (>50 conv/mo) else last-click; window 30d lead-gen, 90d high-consideration.
- **Meta**: pixel via GTM + standard events; add Conversions API (recovers ~30% lost to ad blockers/iOS).

## Cross-platform
**UTM conventions**: source (lowercase platform), medium (cpc/email/social), campaign (id/name), content (creative variant), term (keyword). Never tag organic/direct. Attribution windows: GA4 30-90d, Google Ads 30/90d, Meta 7-day click only, LinkedIn 30d. Cross-domain: list both domains in GA4 unwanted-referrals + GTM cross-domain measurement; verify session doesn't restart in DebugView.

## Data quality
- **Dedup**: GTM tag + hardcoded gtag both firing, Enhanced Measurement + custom tag, SPA pageview double-fire. Audit GTM Preview + Network tab.
- **Bot/internal filtering**: GA4 auto-filters bots; add office/dev IPs to Internal Traffic filter.
- **Consent (GDPR)**: implement Advanced Consent Mode via CMP → models data for decliners (vs zero data). Expected consent: 60-75% EU, 85-95% US.

## Proactive flags
Events on every page load → misconfigured trigger. No user_id → can't link to CRM. GA4≠Ads conversions → window mismatch or pixel dup. No consent mode in EU → legal exposure. Pages as "/(not set)" → SPA routing unhandled. Paid traffic showing "direct" → UTMs missing/stripped.
