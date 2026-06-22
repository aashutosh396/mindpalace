---
name: Database Schema Designer
description: Use when creating ERD diagrams, normalizing schemas, designing table relationships, or planning schema migrations — turns requirements into tables, migrations, types, RLS policies, and indexes.
tags: [schema, erd, normalization, rls, multi-tenancy, soft-delete, audit-trail, mermaid, seed-data, indexes]
source: alirezarezvani/claude-skills
derived_from: database-schema-designer
---

# Database Schema Designer

Design relational schemas from requirements and generate migrations (Drizzle/Prisma/TypeORM/Alembic), TS/Python types, seed data, RLS policies, indexes, and Mermaid ERDs. Handles multi-tenancy, soft deletes, audit trails, versioning, polymorphic associations.

## Design process
**1. Requirements → entities.** Extract nouns as tables (incl. junction tables for many-to-many).
**2. Identify relationships.** Map 1-to-many and many-to-many (via junctions).
**3. Add cross-cutting concerns:**
- Multi-tenancy: `organization_id` on all tenant-scoped tables
- Soft deletes: `deleted_at TIMESTAMPTZ` instead of hard deletes
- Audit trail: `created_by`, `updated_by`, `created_at`, `updated_at`
- Versioning: `version INTEGER` for optimistic locking

## Row-Level Security (RLS)
Enable RLS per table; create an app role; write policies that scope rows by org membership via `current_setting('app.current_user_id')`. Add a soft-delete policy (`USING (deleted_at IS NULL)`) and a delete policy (creator OR org admin). Set user context at the start of each request via `set_config`. Always test RLS with a non-superuser role.

## Seed data
Use a faker-based seed script: create org → users (hashed passwords) → projects → tasks in loops. Keep it deterministic and minimal.

## ERD generation (Mermaid)
Emit `erDiagram` with relationship cardinality lines and entity field blocks (PK/FK marked). Generate from Prisma via `prisma-erd-generator` or `dbml` → mermaid.

## Common pitfalls
- Soft delete without index → `WHERE deleted_at IS NULL` full scan
- Missing composite indexes for multi-column WHERE
- Mutable surrogate keys (never use email/slug as PK — use UUID/CUID)
- Non-nullable column added without default/migration plan
- No optimistic locking → concurrent overwrites (add `version`)
- RLS not tested with a non-superuser role

## Best practices
1. Timestamps on every table. 2. Soft deletes for auditable data. 3. Audit log (before/after JSON) for regulated domains. 4. UUIDs/CUIDs as PKs. 5. Index every FK column. 6. Partial indexes for active-only queries. 7. RLS over app-level filtering — the DB enforces tenancy.
