---
name: email-html-mjml
description: "Use when creating, generating, designing, or building a responsive HTML email — welcome/promo/transactional/newsletter templates, compiling MJML to HTML, editing existing MJML, or fixing cross-client email rendering (Outlook, Gmail, Apple Mail, mobile)."
version: 1.0.0
license: MIT
tags: [mjml, email, html-email, responsive, newsletter, outlook, gmail, transactional, accessibility, dark-mode]
source: https://github.com/framix-team/skill-email-html-mjml
derived_from: awesomeclaude
prerequisites:
  commands: [npx]
---

# email-html-mjml — responsive cross-client email developer

Generate valid MJML 4.x templates and compile them to production-ready HTML.
Primary goal is compatibility: Outlook (2013–365), Gmail (web/app), Apple Mail,
major mobile clients. Every output must compile with
`--config.validationLevel=strict` and survive Gmail's 102KB clip limit.

Requires Node.js 14+. Install MJML per-project (`npm install -D mjml`) — never global.

## When to use

User asks to create/design/build an email template (welcome, promo blast,
transactional, newsletter, any responsive email), compile MJML→HTML, edit
existing MJML, or troubleshoot email rendering across clients.

## Workflow

1. Gather requirements — infer email type, brand colors, content from context.
   Ask only for genuinely missing + blocking info. No front-loaded questionnaire.
2. Plan layout — decide and announce structure first (single-column, 2-col grid,
   hero + content, etc.).
3. Load component references — read the relevant component file(s) before writing.
4. Generate MJML — complete, valid, starting from `<mjml>` with a full `<mj-head>`.
5. Compile — `npx mjml` with `--config.minify=true`.
6. Deliver both files — `.mjml` source AND compiled `.html`.

## 9 engineering rules

1. Structural integrity — all visual content in `<mj-column>` inside `<mj-section>`.
   Sections cannot be nested.
2. Responsive defaults — assume 600px width. Use `<mj-group>` to stop mobile
   stacking for side-by-side elements (social bars, logo rows).
3. Outlook — use `<mj-font>` for web fonts (avoids Times New Roman fallback) with
   a fallback stack (Arial, sans-serif). For section background images set both
   `background-size` and a fallback `background-color`.
4. Gmail — use `inline="inline"` on `<mj-style>`. Prefer component attributes
   (`color`, `font-size`) over CSS classes for critical styles (classes get stripped).
5. Dark mode — add when requested or when a light background would cause harsh
   forced inversion. See pattern below.
6. Accessibility — every `<mj-image>` needs `alt`; always set `<mj-title>`; WCAG
   2.1 AA 4.5:1 contrast. Heading roles via `mj-html-attributes` (direct
   `role`/`aria-level` on `mj-text` is illegal under strict validation).
7. Styling efficiency — use `<mj-attributes>` with `<mj-all>`, defaults, `<mj-class>`.
8. Hero — use `<mj-hero>` for full-bleed banners (falls back gracefully). Avoid
   `<mj-accordion>` and `<mj-carousel>` (poor client support).
9. Templating — wrap dynamic tags (Handlebars/Liquid) in `<mj-raw>` to protect
   them from the MJML parser.

## Critical gotchas

- Outlook background images: VML only generated for `<mj-section>` and `<mj-hero>`,
  nowhere else. Positioning uses keyword values only (`top`/`center`/`bottom`) —
  pixel values ignored. Always pair `background-repeat="no-repeat"` with explicit
  `background-size`.
- Gmail 102KB clip: always compile with `--config.minify=true`.
- iOS/Android stacking: minify removes whitespace between inline-block columns;
  whitespace between tags causes stacking even inside `<mj-group>`.
- Vertical-align bug: if any column in a section sets `vertical-align`, ALL columns
  in that section must explicitly set it.
- JavaScript is fully blocked in all email clients — no `onclick`, no interactivity.
  "Interactive" elements (copy buttons, toggles) are decorative only.

## Dark mode pattern

```xml
<mj-head>
  <mj-raw>
    <meta name="color-scheme" content="light dark">
    <meta name="supported-color-schemes" content="light dark">
  </mj-raw>
  <mj-style inline="inline">.dark-logo { display: none !important; }</mj-style>
  <mj-style>
    @media (prefers-color-scheme: dark) {
      .light-logo { display: none !important; }
      .dark-logo  { display: block !important; }
    }
  </mj-style>
</mj-head>
```

Safe neutrals: `#121212` (not `#000000`), `#F1F1F1` (not `#FFFFFF`).

## Accessibility checklist

- `<mj-title>` set; `lang` on root `<mjml>`; `alt` on every image + social element.
- Heading role via `mj-html-attributes` (NOT direct attribute on `mj-text`):
  ```xml
  <mj-html-attributes>
    <mj-selector path=".email-heading div">
      <mj-html-attribute name="role">heading</mj-html-attribute>
      <mj-html-attribute name="aria-level">1</mj-html-attribute>
    </mj-selector>
  </mj-html-attributes>
  <!-- component: <mj-text css-class="email-heading">Heading</mj-text> -->
  ```
- 4.5:1 contrast on all text/background pairs. No text baked into images.

## Compilation

```bash
npx mjml template.mjml -o dist/template.html --config.minify=true --config.validationLevel=strict
```

Hard rules: never `npm install -g mjml`; always `npx` or `./node_modules/.bin/mjml`;
if mjml not in `package.json`, suggest `npm install -D mjml`.

## Component references

Read the matching reference file from the source repo before writing MJML using
those components (under `email-html-mjml/` in the source repo):

- `components/head.md` — mj-attributes, mj-font, mj-style, mj-preview, mj-breakpoint, mj-html-attributes
- `components/layout.md` — mj-body, mj-section, mj-column, mj-group, mj-wrapper
- `components/content.md` — mj-text, mj-image, mj-button, mj-divider, mj-spacer, mj-table
- `components/interactive.md` — mj-accordion, mj-carousel, mj-social, mj-navbar
- `components/advanced.md` — mj-hero, mj-raw, mj-include
- `mjml-reference.md` — hierarchy, ending tags, validation, width math, Gmail clip
- `compilation.md` — full compile workflow

## Output

Always deliver both: `<name>.mjml` (editable source) AND `<name>.html` (production).
Name files after email type: `welcome.mjml`, `promo-sale.mjml`, `order-confirmation.mjml`.
