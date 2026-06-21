---
name: nextjs-developer
description: "Use when building Next.js 14+ apps with App Router, Server Components, or Server Actions — route handlers, middleware, streaming SSR, generateMetadata for SEO, loading.tsx/error.tsx, Vercel deploy. Triggers: Next.js, Next.js 14, App Router, Server Components, Server Actions, RSC, generateMetadata, loading.tsx, Vercel, Next.js performance."
version: 1.0.0
license: MIT
tags: [nextjs, app-router, server-components, server-actions, ssr, vercel, seo, react]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/nextjs-developer
derived_from: awesomeclaude
---

# Next.js Developer

Next.js 14+ App Router: RSC, Server Actions, streaming SSR.

## When to use

App Router apps; Server Components + Server Actions; route handlers; middleware; API routes; streaming SSR; `generateMetadata` SEO; `loading.tsx`/`error.tsx` boundaries; Vercel deploy.

## Core workflow

1. **Analyze** — routing tree, server/client split, data sources.
2. **Design** — RSC for data, client components only at interactive leaves.
3. **Implement** — route segments, `loading.tsx`/`error.tsx`, Server Actions for mutations.
4. **SEO/perf** — `generateMetadata`, streaming, caching directives.
5. **Deploy** — Vercel config, edge vs node runtime choice.

## Key practices

- Default to Server Components; `"use client"` only where hooks/interactivity needed.
- Server Actions for mutations (`"use server"`); validate input server-side.
- Caching: understand `fetch` cache, `revalidate`, `dynamic`, `cache()`.
- Co-locate `loading.tsx` (Suspense) and `error.tsx` (error boundary) per segment.
- `generateMetadata` for per-route SEO; structured data where relevant.
- Route handlers (`route.ts`) for APIs; middleware for auth/redirects at the edge.

## Constraints

MUST: minimize client components; validate Server Action inputs server-side; explicit caching/revalidation strategy; metadata for indexable routes; error + loading boundaries; env vars for secrets (server only).
MUST NOT: expose server secrets to client bundles; mark whole trees `"use client"` needlessly; mutate without server-side validation; ignore caching semantics; block streaming with sync data waterfalls.

## Output

1. Route segments (page/layout/loading/error). 2. Server Actions / route handlers. 3. Metadata + caching config. 4. Brief note on RSC/caching decisions.

## Knowledge

Next.js 14+, App Router, React Server Components, Server Actions, route handlers, middleware, streaming SSR, generateMetadata, caching/revalidation, Vercel, edge runtime.
