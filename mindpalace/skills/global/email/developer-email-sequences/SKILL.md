---
name: developer-email-sequences
description: Use when creating email sequences for developers — onboarding drips, activation, changelog/product-update emails, re-engagement campaigns, email cadence, or transactional vs marketing email decisions.
version: 1.0.0
license: MIT
tags: [email, developer-marketing, onboarding, drip, changelog, re-engagement, transactional, cadence]
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/developer-email-sequences
derived_from: awesomeclaude
---

# Developer Email Sequences

Developers are ruthless with email: they scan the preview pane (subject + first line are everything), unsubscribe on one irrelevant email, often prefer plain text, click useful code snippets, and trust transactional mail over "newsletters". **Golden rule: every email must provide immediate value or solve a problem.**

## Onboarding sequence

Goal: get to first "Hello World". Timing: Email 1 immediately on signup; 2 at 24h; 3 at 3 days; 4 at 7 days — **stop the moment they activate**.

1. Welcome — confirm signup, one CTA (quickstart link, nothing else). Subject "Your API key is ready".
2. First nudge — address common blockers, ask where they got stuck (checkbox reply). Subject "Quick question about your setup".
3. Value reminder — customer example or code snippet.
4. Last chance — direct ask, "Reply if you need help".

## Activation sequence

Goal: first-time → regular user. Trigger: after first successful call. Timing: immediately, +3d, +7d, +14d. Beats: celebration ("Your first call worked!") → next step ("most devs do X next") → deep feature tutorial → production integration (case study/deploy guide).

## Changelog / product-update emails

Frequency: weekly digest or per-release, never >2x/week. Order **breaking changes first**, then New / Improved / Fixed, with code examples for new features and a link to the full changelog (don't dump it all). No marketing fluff. End with where to get upgrade help.

## Re-engagement sequence

Trigger: inactivity. Timing: day 30, 45, 60, 90 (sunset). Beats: check-in ("Did something break?") → what's new they missed → direct ask (survey/reply) → sunset warning ("Pausing your account in 14 days" — keys stop, data stays safe, log in to keep active). After unsubscribe, don't beg.

## Frequency guidelines

| Type | Max frequency |
|---|---|
| Transactional | as needed |
| Onboarding | 4 over 7 days (stop on activation) |
| Changelog | 1x/week (digest preferred) |
| Re-engagement | 4 over 60 days then stop |
| Marketing/newsletter | 2x/month, must add value |

Unsubscribe test: if a dev would feel *relieved* to unsubscribe, you send too many.

## Transactional vs marketing

Transactional (triggered by user action, expected, higher deliverability, no unsubscribe needed): password resets, receipts, usage alerts, security notices. Marketing (scheduled, opt-in, full CAN-SPAM, unsubscribe required): newsletters, announcements, webinars. Onboarding is a gray area — still give an easy unsubscribe.

## Technical content in emails

Code snippets: keep under 10 lines, syntax-highlight if HTML, test that it works, state language/version, never include realistic-looking secrets. For API updates, show the new endpoint with a short snippet, rate limit, and docs link.

## Metrics

| Metric | Good | Warning → action |
|---|---|---|
| Open rate | >40% | <25% fix subjects |
| Click rate | >10% | <3% fix content/CTA |
| Unsubscribe | <0.2% | >0.5% reduce frequency |
| Reply rate | >1% | celebrate |
| Onboarding activation | >30% | <15% rethink sequence |

A/B test priority: subject lines > send time > length > plain vs HTML > CTA wording.

## Common mistakes

"Just checking in" (no value); empty weekly newsletters (trains devs to ignore); HTML-heavy spammy design; multiple CTAs; fake personalization; celebrating *your* milestones (funding) — focus on what matters to them.

Tools: Customer.io, Postmark (transactional), Buttondown, Resend, Loops.
