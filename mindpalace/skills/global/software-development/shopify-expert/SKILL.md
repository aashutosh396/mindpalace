---
name: shopify-expert
description: "Use when building/customizing Shopify — Liquid themes (.liquid, sections, theme.json), custom apps (shopify.app.toml, OAuth, webhooks), Storefront API / Hydrogen headless, checkout extensions, Shopify Functions, App Bridge, Polaris. Triggers: Shopify, Liquid, Storefront API, Shopify Plus, Hydrogen, Shopify app, checkout extensions, Shopify Functions, App Bridge, theme development, e-commerce, Polaris."
version: 1.0.0
license: MIT
tags: [shopify, liquid, storefront-api, hydrogen, shopify-app, polaris, ecommerce, checkout-extensions]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/shopify-expert
derived_from: awesomeclaude
platforms: [shopify]
---

# Shopify Expert

Shopify themes, custom apps, and headless storefronts.

## When to use

Liquid theme dev/customization; Hydrogen or custom React storefronts (Storefront API); custom Shopify apps; checkout UI extensions + Shopify Functions; performance; third-party integrations; Shopify Plus features.

## Core workflow

1. **Identify surface** — theme (Online Store 2.0), app (embedded), or headless (Storefront API).
2. **Themes** — sections + blocks, `theme.json`/JSON templates, Liquid + metafields.
3. **Apps** — `shopify.app.toml`, OAuth install flow, webhooks (HMAC-verified), App Bridge + Polaris UI.
4. **Headless** — Storefront API (GraphQL) or Hydrogen + Oxygen.
5. **Validate** — Shopify CLI dev/preview; Theme Check; test webhooks + checkout.

## Key practices

- Online Store 2.0: JSON templates, sections everywhere, app blocks; merchant-editable via schema.
- Apps: verify webhook HMAC; respect API rate limits (REST bucket / GraphQL cost); store offline tokens securely.
- Storefront API for customer-facing reads; Admin API for backoffice.
- Checkout UI extensions + Shopify Functions for Plus checkout logic.
- App Bridge for embedded admin; Polaris for consistent UI.

## Constraints

MUST: verify webhook HMAC signatures; respect API rate limits (GraphQL cost / REST leaky bucket); use metafields for custom data; Theme Check clean; least-privilege OAuth scopes; secure token storage.
MUST NOT: hardcode store domains/tokens; ignore rate-limit / cost headers; bypass checkout extension model on Plus; expose Admin API to the storefront; skip webhook verification.

## Output

1. Theme sections/templates or app scaffold (`shopify.app.toml`). 2. Liquid/Storefront/Admin API code. 3. Webhook handlers (HMAC-verified). 4. Brief note on scopes + rate-limit handling.

## Knowledge

Shopify, Liquid, Online Store 2.0, sections/blocks, metafields, Storefront API, Admin API (REST + GraphQL), Hydrogen/Oxygen, checkout UI extensions, Shopify Functions, App Bridge, Polaris, Shopify CLI, webhooks/HMAC.
