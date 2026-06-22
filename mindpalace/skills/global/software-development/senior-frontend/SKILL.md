---
name: Senior Frontend (React/Next.js)
description: Use when building React/Next.js components, optimizing performance, analyzing bundle size, scaffolding frontend projects, or reviewing frontend code quality — with eval-gated profile decisions.
tags: [react, nextjs, typescript, tailwind, frontend, performance, bundle-size, accessibility, core-web-vitals, server-components]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-frontend
---

# Senior Frontend (React/Next.js)

Frontend patterns, performance, and decision discipline for React/Next.js.

## Surface 4 Assumptions Before Recommending
1. **Primary device + network** — mobile-4G / desktop-fiber / low-end-Android / corporate.
2. **LCP target in ms** — a number, not "fast."
3. **SEO-dependent vs auth-walled** — drives SSR/SSG/RSC vs SPA.
4. **WCAG target + named a11y owner.**

Every recommendation must include: Core Web Vitals targets (LCP, INP, CLS) at p75 on primary device; per-route JS bundle budget (KB-gzip); Lighthouse a11y + perf floor. Missing any → incomplete.

## Profiles
| Profile | When | LCP (mobile-4G p75) | Bundle |
|---|---|---|---|
| next-app-router | SaaS, SEO + dynamic, RSC-first | 2000ms | 150 KB/route |
| remix-or-sveltekit | mobile-4G primary, low-JS, progressive enhancement | 1500ms | 80 KB/route |
| vite-spa | auth-walled, desktop/corporate | 2500ms | 200 KB init + 80/route |
| astro-or-static | marketing/docs/blog, SEO-critical | 1200ms | 30 KB JS/page |

## React Patterns
- **Compound components**: share state via Context, `Tabs.List`/`Tabs.Panel`.
- **Custom hooks**: extract reusable logic (`useDebounce`, `useLocalStorage`).
- **Render props**: share rendering logic (`DataFetcher` with `render`).

## Next.js Optimization
- Server Components by default; add `'use client'` only for event handlers, state, effects, browser APIs.
- `next/image`: `priority` above-fold; `fill` + `sizes` responsive.
- Parallel fetch via `Promise.all`; stream with `<Suspense>`.
- Config: `images.formats: ['image/avif','image/webp']`, `experimental.optimizePackageImports`.

## Bundle Health
Replace heavy deps: moment(290KB)→date-fns/dayjs · lodash(71KB)→lodash-es tree-shaking · axios(14KB)→fetch/ky · jquery→DOM · @mui→shadcn/Radix. Grade A 90+, C 70-79 (replace heavy deps), F <60.

## Accessibility Checklist
Semantic HTML (`<button>`,`<nav>`,`<main>`) · keyboard-focusable interactives · ARIA labels on icons · 4.5:1 contrast · visible focus (`focus-visible:ring`) · skip link. Test with Testing Library: assert roles, `aria-labelledby` on dialogs.

## TypeScript
Props with `children: React.ReactNode`; generic components `ListProps<T>` with typed `renderItem`. Conditional classes via `cn()`.
