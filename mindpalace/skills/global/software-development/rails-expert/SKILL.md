---
name: rails-expert
description: "Use when building Rails 7+ web apps with Hotwire, real-time features, or background jobs. Optimizes Active Record (includes/eager_load), Turbo Frames/Streams, Action Cable, Sidekiq workers, RSpec suites. Triggers: Rails, Ruby on Rails, Hotwire, Turbo Frames, Turbo Streams, Action Cable, Active Record, Sidekiq, RSpec Rails."
version: 1.0.0
license: MIT
tags: [rails, ruby, hotwire, turbo, action-cable, active-record, sidekiq, rspec]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/rails-expert
derived_from: awesomeclaude
---

# Rails Expert

Rails 7+: Hotwire, real-time, background jobs.

## When to use

Rails 7+ apps; Active Record optimization; Turbo Frames/Streams partial updates; Action Cable WebSockets; Sidekiq background jobs; RSpec test suites.

## Core workflow

1. **Analyze** — models, associations, routes.
2. **Design** — models with associations, indexes, scopes.
3. **Implement** — controllers + Hotwire (Turbo Frames/Streams) for partial updates.
4. **Async/real-time** — Sidekiq jobs; Action Cable channels.
5. **Test** — RSpec (models, requests, system specs).

## Key practices

- Active Record: `includes`/`eager_load`/`preload` to kill N+1; add DB indexes on FKs.
- Turbo Frames for scoped updates; Turbo Streams for broadcast inserts/replaces.
- Service objects / POROs for business logic; skinny controllers.
- Sidekiq for slow/external work; idempotent jobs.
- Strong parameters; validations + DB constraints together.

## Constraints

MUST: eager-load associations (no N+1); DB indexes on foreign keys; strong params; idempotent Sidekiq jobs; RSpec coverage for models + requests; CSRF protection on.
MUST NOT: business logic in views; N+1 queries; skip migrations; trust mass-assignment without strong params; block the request on slow external calls (use jobs); secrets in source (use credentials/env).

## Output

1. Models + migrations with indexes. 2. Controllers + Hotwire views. 3. Sidekiq jobs / Action Cable channels. 4. RSpec specs. 5. Brief note on query/realtime decisions.

## Knowledge

Rails 7+, Active Record, Hotwire (Turbo/Stimulus), Turbo Frames/Streams, Action Cable, Sidekiq, RSpec, FactoryBot, strong parameters, scopes, service objects.
