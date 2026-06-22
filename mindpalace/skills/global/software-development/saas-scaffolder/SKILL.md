---
name: SaaS Scaffolder
description: Use when starting a new subscription web app and you need production-ready boilerplate — scaffolds Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + Drizzle + Stripe with auth, DB schema, billing, and dashboard wired up.
tags: [saas, boilerplate, nextjs, stripe, drizzle, nextauth, scaffold, billing, starter-template, app-router]
source: alirezarezvani/claude-skills
derived_from: product-team/saas-scaffolder
---

# SaaS Scaffolder

Generate production-ready SaaS boilerplate: auth, DB schema, billing, API routes, working dashboard. Default stack: Next.js 14+ App Router, TypeScript, Tailwind, shadcn/ui, Drizzle ORM, Stripe. Swappable: auth (nextauth/clerk/supabase), DB (neondb/supabase/planetscale), payments (stripe/lemonsqueezy/none).

## Input

```
Product, Description, Auth, Database, Payments, Features[]
```

## File Tree (target)

`app/` with route groups `(auth)/`, `(dashboard)/`, `(marketing)/`, plus `api/auth/[...nextauth]`, `api/webhooks/stripe`, `api/billing/checkout`, `api/billing/portal`. `components/` (ui, auth, dashboard, marketing, billing), `lib/` (auth, db, stripe, validations, utils), `db/` (schema + migrations), `hooks/`, `types/`, `middleware.ts`, `.env.example`, `drizzle.config.ts`.

## Key Patterns

- **NextAuth** — `DrizzleAdapter(db)`, OAuth provider, session callback that injects `user.id` + `subscriptionStatus`, `pages: { signIn: "/login" }`.
- **Drizzle schema** — `users` table with `stripeCustomerId/SubscriptionId/PriceId/CurrentPeriodEnd`; `accounts` table with cascade FK to users.
- **Stripe checkout route** — auth-guard → look up user → create-or-reuse `stripeCustomerId` → `checkout.sessions.create` (mode subscription, trial 14d) → return URL.
- **Middleware** — `withAuth` matcher on `/dashboard`, `/settings`, `/billing`; redirect to `/login` when no token.
- **.env.example** — every var: `DATABASE_URL` (with `?sslmode=require`), `NEXTAUTH_SECRET/URL`, OAuth client id/secret, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, publishable key, price ids.

## Scaffold Checklist (validate at end of each phase)

**P1 Foundation** — Next.js+TS+App Router, Tailwind theme tokens, shadcn/ui, ESLint+Prettier, `.env.example`. ✅ `npm run build` clean.

**P2 Database** — Drizzle configured, schema (users/accounts/sessions/verification_tokens), initial migration, `lib/db.ts` singleton, connection tested. ✅ `db.select().from(users)` returns `[]` without throwing. 🔧 ensure `?sslmode=require`; `drizzle-kit push` (dev) / `migrate` (prod).

**P3 Authentication** — provider installed, OAuth configured, auth route, session callback adds id+subscriptionStatus, middleware protects dashboard, login/register pages with error states. ✅ OAuth sign-in → session has id+status; `/dashboard` w/o session redirects. 🔧 sign-out loops in prod = `NEXTAUTH_SECRET` missing/inconsistent; extend session types via `declare module "next-auth"`.

**P4 Payments** — Stripe client typed, checkout route, customer-portal route, webhook with signature verification, webhook updates subscription status **idempotently**. ✅ test checkout `4242 4242 4242 4242` writes `stripeSubscriptionId`; replay `checkout.session.completed` → no duplicate writes. 🔧 use `stripe listen --forward-to localhost:3000/api/webhooks/stripe`; never hardcode webhook secret.

**P5 UI** — landing (hero/features/pricing), dashboard (sidebar + responsive header), billing page (current plan + upgrade), settings (profile form + success states). ✅ final `npm run build`; walk all routes, no broken layouts/hydration errors.

## Companion Reference Files (generate alongside)

- `CUSTOMIZATION.md` — auth/db/ORM/payment/UI/billing-model alternatives.
- `PITFALLS.md` — missing `NEXTAUTH_SECRET`, webhook secret mismatch, Edge runtime vs Drizzle, unextended session types, dev-vs-prod migration.
- `BEST_PRACTICES.md` — Stripe singleton, server actions for mutations, idempotent webhooks, Suspense boundaries, server-side feature gating via `stripeCurrentPeriodEnd`, rate limiting auth routes (Upstash Redis + `@upstash/ratelimit`).
