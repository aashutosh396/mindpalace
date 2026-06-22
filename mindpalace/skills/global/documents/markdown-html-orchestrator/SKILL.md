---
name: Markdown → HTML Orchestrator
description: Use when converting a markdown file (≥100 lines) into single-file interactive HTML — classifies it as document / code-review / slide-deck and routes to the right converter after a one-time design-system onboarding. Refuses below 100 lines or without onboarding.
tags: [markdown, html, converter, orchestrator, documentation, code-review, slides, doctype-classifier, single-file]
source: alirezarezvani/claude-skills
derived_from: markdown-html/skills/markdown-html-orchestrator
---

# Markdown → HTML — Domain Orchestrator

Premise (Shihipar, *Claude Code HTML output*, 2026): **markdown collapses past ~100 lines** for agent-generated artifacts — long specs, reviews, and decks lose density, hierarchy, and lightweight interaction; HTML restores all three as a single shareable file. This orchestrator classifies the input, routes to one of three converters, and returns a digest.

## Pre-flight gates (hard refusals)

1. **< 100 lines** — markdown still wins; refuse and tell the user to keep it as markdown.
2. **Design-system not onboarded** — refuse until the one-time brand wizard has run (the `design-system` skill); converters render unbranded without it.
3. **Unwritable output dir** — refuse.

## Routing (deterministic two-signal scoring)

Filename hint = 2 points; each content signal = 1 point. Silent-route when winner ≥3 AND (runner-up = 0 OR winner ≥ 2× runner-up); otherwise ask ONE question with a recommended answer.

| Lane | Filename hints | Content signals | Converter |
|---|---|---|---|
| DOCUMENT | `report.md`, `spec.md`, `rfc-*.md`, `*-analysis.md`, `*-explainer.md` | `## Table of Contents` (2), `#`/`##`, tables, `> [!NOTE]/[!TIP]` callouts | `md-document` |
| REVIEW | `review.md`, `*-pr-*.md`, `*.diff.md` | ` ```diff ` (2), `--- `/`+++ ` (2), `@@` (2), `> [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]` (2), `LGTM`/`nit:` | `md-review` |
| SLIDES | `deck.md`, `slides.md`, `*-talk.md`, `presentation*.md` | `^---$` ≥3 (2+), `<!-- notes:` (2), H1 count ≥5 with median gap ≤12 lines (2) | `md-slides` |

## Workflow

1. **Confirm onboarding** — if never run, surface the design-system wizard (10 questions, 1-2 min: brand primary/accent + heading/body Google Fonts + design style editorial/technical/minimal/playful + output dir + syntax theme + TOC behavior + optional logo/company; stored at `~/.config/markdown-html/design-system.json`).
2. **Classify** the input markdown.
3. **Route or ask** — if silent-route, forward markdown + design-system config to the named converter; if not, ask one question.
4. **Resolve output path** — kebab slug + collision suffix (`-2`, `-3`, …; `timestamp` opt-in).
5. **Hand off** — the converter writes a single self-contained HTML file. Return a ≤100-word digest: input lines, output path, design style applied, top 3 features used, one forcing question. Never render HTML by hand.

## Forcing questions (one at a time, recommended answer)

1. What decision does this HTML drive — skim, decide, or present? (Name it first; density follows.)
2. Is the input ≥100 lines? (If not, keep as markdown.)
3. Is the design-system onboarded? (Globally, by default.)
4. Where does output save, and will it overwrite? (Configured dir + collision suffix — never silently overwrite.)
5. Doctype confidence — silent-route or ask? (Silent only when verdict is one of document/review/slides AND silent_route_allowed.)

Never run a converter before the lane is locked.

## Hard rules / non-goals

Single-file HTML only — externals limited to Google Fonts CSS + Prism.js CDN; no JS framework runtime (vanilla JS + IntersectionObserver only); no multi-file output, no build step, no live-reload. Never silently chain converters ("convert AND make slides" = two ops — finish one, ask before chaining). Customization must change behavior, not decorate. Not a landing-page generator, not a prompt-tuning playground, not a static-site generator, not a PDF generator (slides use `@media print`).
