---
name: wordpress-pro
description: "Use when building WordPress themes/plugins, Gutenberg blocks + patterns, WooCommerce stores, WP REST API endpoints, security hardening (nonces, sanitization, escaping, capability checks), and performance tuning. Triggers: WordPress, WooCommerce, Gutenberg, WordPress theme, WordPress plugin, custom blocks, ACF, WordPress REST API, hooks, filters, WordPress performance, WordPress security."
version: 1.0.0
license: MIT
tags: [wordpress, woocommerce, gutenberg, plugins, themes, rest-api, acf, security]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/wordpress-pro
derived_from: awesomeclaude
platforms: [wordpress, woocommerce]
---

# WordPress Pro

Custom themes, plugins, Gutenberg blocks, WooCommerce.

## When to use

Custom themes/plugins; Gutenberg blocks + block patterns; WooCommerce extension/config; WP REST API endpoints; security hardening; performance via caching + query tuning; ACF; hooks/filters.

## Core workflow

1. **Analyze** — theme vs plugin scope; existing hooks; data model.
2. **Design** — extend via hooks/filters (never edit core); custom post types/taxonomies as needed.
3. **Implement** — themes (template hierarchy) or plugins (activation hooks); register Gutenberg blocks.
4. **Secure** — nonces, sanitize input, escape output, capability checks, prepared queries.
5. **Optimize** — object/page caching, efficient `WP_Query`, avoid expensive queries on every load.

## Key practices

- Extend via `add_action`/`add_filter`; never modify WordPress/WooCommerce core.
- Sanitize on input (`sanitize_text_field`, etc.), escape on output (`esc_html`, `esc_attr`, `esc_url`).
- Verify nonces on form/AJAX actions; `current_user_can()` capability checks.
- `$wpdb->prepare()` for any custom SQL.
- Gutenberg: `register_block_type` + `block.json`; server-rendered or React-edit blocks.
- WooCommerce: hooks/template overrides via theme, not core edits.

## Constraints

MUST: sanitize input + escape output; nonce verification + capability checks on actions; `$wpdb->prepare()` for SQL; extend via hooks/filters; enqueue scripts/styles properly; object/page caching for heavy queries.
MUST NOT: edit core files; trust/echo raw user input; skip nonces or capability checks; raw unprepared SQL; load assets on every page unconditionally; run unbounded `WP_Query` (`posts_per_page=-1`) on hot paths.

## Output

1. Theme template / plugin file with proper hooks. 2. Gutenberg block (`block.json` + render). 3. Sanitized/escaped + nonce-protected handlers. 4. Brief note on security + perf decisions.

## Knowledge

WordPress, WooCommerce, Gutenberg (block.json), block patterns, custom post types/taxonomies, hooks/filters, WP REST API, ACF, nonces, sanitization/escaping, capabilities, $wpdb->prepare, transients/object cache, WP_Query.
