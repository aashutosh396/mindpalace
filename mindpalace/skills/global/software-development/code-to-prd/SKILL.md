---
name: Code to PRD
description: Use when you need to reverse-engineer an existing codebase into a Product Requirements Document — analyzes routes, components, models, and APIs into business-readable specs detailed enough to reconstruct every page and endpoint.
tags: [prd, reverse-engineer, documentation, codebase-analysis, requirements, api-inventory, product-spec, functional-inventory]
source: alirezarezvani/claude-skills
derived_from: product-team/code-to-prd
---

# Code → PRD

Reverse-engineer any frontend, backend, or fullstack codebase into a complete PRD. Dual audience: PMs need *what* the system does; engineers/AI agents need enough detail to **fully reconstruct** every page/endpoint. Describe in business language, omit zero business detail.

Supported: React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit, Remix, Astro (frontend); NestJS, Express, Fastify, Django, DRF, FastAPI, Flask (backend). For backend-only, "page" maps to API resource groups / admin views.

## Phase 1 — Global Scan

1. **Identify structure** — find pages/routes, components, route config, API/service layer, state mgmt, i18n (field display names often live here). For backend: modules, controllers/views, services, DTOs/serializers, entities/models, guards/middleware.
2. **Identify framework** from `package.json`, `manage.py`, `requirements.txt`/`pyproject.toml`.
3. **Build route/page inventory** — table of route path, page title, module/menu level, component file. For file-system routing, infer from directories. Backend: endpoint path, HTTP method, controller/view, module, auth required. (NestJS: `@Controller`+`@Get/@Post`. Django: `urls.py` urlpatterns + viewset router.)
4. **Map global context** — global state, shared components, enums/constants, API base config, DB models, middleware, DTOs/serializers.

## Phase 2 — Page-by-Page Deep Analysis

Each page → its own Markdown file. For each, answer:
- **A. Overview** — what it does (1 sentence), where it fits, what brings a user here.
- **B. Layout & regions** — search area, table, detail panel, action bar, tabs; spatial arrangement.
- **C. Field inventory (be exhaustive)** — forms: every field (name, type, required, default, validation, business description). Lists: filter fields, table columns, row actions. Field-name extraction priority: hardcoded text → i18n values → `placeholder`/`label`/`title` props → variable names (last resort).
- **D. Interaction logic** — write as "action → response": trigger, response, validation, API call, success, failure. Cover load/init, search/filter/reset, CRUD, pagination/sorting/selection/bulk, form submit, status transitions, import/export, field interdependencies, permission visibility, polling/auto-refresh.
- **E. API dependencies** — if real HTTP calls: name, method, path, trigger, params. If mock/hardcoded (signals: `setTimeout`, `Promise.resolve()`, `*.mock.*`, `__mocks__`): reverse-engineer the *required* API spec (method, path, inputs, outputs, logic).
- **F. Page relationships** — inbound (which pages link here + params), outbound, data coupling (cross-page refresh triggers).

## Phase 3 — Generate Docs

Output to `prd/`:
```
prd/
├── README.md            # system overview, module table, page inventory, permission model, common patterns
├── pages/01-*.md        # one file per page (self-contained)
└── appendix/
    ├── enum-dictionary.md   # every enum value + meaning
    ├── page-relationships.md
    └── api-inventory.md
```
Per-page template: Route/Module/Generated header → Overview → Layout → Fields (per region tables) → Interactions (per scenario) → API Dependencies → Page Relationships → Business Rules.

## Key Principles

1. **Business language first** — "search button shows a spinner to prevent duplicate submits", not "calls useState". Include technical detail only when it affects product behavior (API paths, validation, permission conditions).
2. **Don't miss hidden logic** — field interdependencies, conditional button visibility, data formatting, default sort/page size, debounce, polling intervals.
3. **Exhaustively list enums** — every status code, type code, role with its meaning.
4. **Mark uncertainty** — tag `[TBC]` and explain; never fabricate business meaning.
5. **Self-contained page files** — reading one file gives complete understanding.

## Pacing

>15 pages: batch 3-5 per module, do overview + inventory first, output each batch for review. ≤15 pages: one pass.

## Common Pitfalls

Component names as page names; skipping modals/drawers (they hold critical logic); missing i18n field names; ignoring dynamic route params; forgetting permission controls; assuming all APIs are real; skipping Django admin customization; missing NestJS guards/pipes; ignoring DB constraints (unique/max_length/choices = validation rules); overlooking middleware.
