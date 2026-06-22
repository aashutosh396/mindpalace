---
name: i18n / Localization Expert
description: Use when setting up, auditing, or enforcing internationalization in a UI codebase (React/TS, i18next/next-intl/vue-i18n, JSON locales) — installs/configures the framework, replaces hardcoded strings, ensures locale parity, maps error codes to localized messages, validates pluralization/formatting.
tags: [i18n, l10n, localization, internationalization, react-i18next, next-intl, vue-i18n, locale, translation, parity]
source: daymade/claude-code-skills
derived_from: i18n-expert
---

Deliver a complete i18n setup + audit: configure the framework, replace user-facing strings with keys, ensure locale parity, validate pluralization/formatting (default locales en-US + zh-CN).

## Scope inputs (ask if unclear)
Framework + routing style; existing i18n state (none/partial/legacy); target locales; translation quality needs (AI/professional/manual); locale formats (JSON/YAML/PO/XLIFF); formality/cultural requirements.

## Workflow (Audit → Fix → Validate)
1. **Confirm scope/locales** — identify framework + locale file locations; default en-US + zh-CN.
2. **Setup baseline (if missing)** — pick library (React → react-i18next; Next.js → next-intl; Vue → vue-i18n); install + create config; wire provider at app root + load resources; add language switcher + persistence (route/param/localStorage); establish locale layout + key namespaces; define locale-segment strategy early if routing is locale-aware (subpath/subdomain/query); translate metadata if user-facing.
3. **Audit key usage + parity** — `python scripts/i18n_audit.py --src <root> --locale en-US.json --locale zh-CN.json`. Missing keys/parity gaps = blockers. Manually verify dynamic keys `t(var)`.
4. **Find raw user-facing strings** — `rg` for JSX text and `aria-label=/title=/placeholder=` attributes; localize accessibility labels.
5. **Replace strings with keys** — `t('namespace.key')`; plurals `t('key', {count})` + `_one/_other`; Intl/app formatters for date/number/time.
6. **Localize error handling (critical)** — map error codes → localized keys, show localized UI only, log raw details only, localized fallback for unknown codes.
7. **Update locale files** — add missing keys in both locales, keep placeholders consistent, avoid renames, generate translations preserving placeholders + plural rules.
8. **Validate** — re-run audit until missing/parity is zero; validate JSON (`python -m json.tool`); update tests asserting visible text.

## Guardrails
Never expose raw `error.message` to UI. Don't add extra locales unless requested. Prefer structured namespaces (`errors.*`, `buttons.*`, `workspace.*`). Keep translations concise/consistent. Keep technical/brand terms untranslated (product name, API, MCP, Bash). Preserve `{name}`/`{{name}}` placeholders exactly; validate plurals by locale rules. Non-web surfaces (Electron dialogs, CLI prompts, native menus) need localization too.

## Performance
Lazy-load locale bundles; split large locale files by namespace.

## Validation checklist
No missing keys, no raw UI strings; locale switching works + persists; plurals/formatting verified in both locales; fallback locale configured.
