---
name: use-graphql-api
description: "Use when querying or mutating a GraphQL endpoint from the command line — discover the schema via introspection, build queries/mutations with variables, execute with `gh api graphql` or curl, parse with jq, and chain calls by piping IDs between them. Triggers: GraphQL, gh api graphql, introspection, query, mutation, GitHub Discussions/Projects v2, Hasura, Apollo, GraphQL endpoint."
version: 1.0.0
license: MIT
tags: [graphql, api, github, query, mutation, introspection, jq, automation, cli]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/use-graphql-api
prerequisites: ["gh CLI (for GitHub) or curl", "jq"]
derived_from: awesomeclaude
---

# Use GraphQL API

Discover, construct, execute, and chain GraphQL operations from the command line.

## When to Use

- Querying or mutating data via a GraphQL endpoint (GitHub, Hasura, Apollo)
- Automating GitHub ops that need GraphQL (Discussions, Projects v2)
- Shell scripts fetching structured data from GraphQL
- Chaining calls where one operation's output feeds the next

## Procedure

### Step 1 — Discover the schema
Introspect available types/queries/mutations. GitHub: `gh api graphql -f query='{ __schema { queryType { fields { name description } } } }'`. Generic: POST a `__schema` introspection query via curl with a Bearer token. 401 → check token (`gh auth status`); "Cannot query field" → introspection may be disabled, use the docs.

### Step 2 — Identify the operation type
query (read), mutation (write/create/update/delete), subscription (stream, rare in CLI). If the action changes state, it is a mutation. Confirm the exact operation name exists (grep the mutationType fields).

### Step 3 — Construct the operation
Rules: always use variables (`$var: Type!`) not inline values; request only needed fields; use `first: N` with `nodes` for connections; add `id` to every object selection (you'll need it for chaining). Watch nullability: most input fields are non-null (`!`). GraphQL has no trailing commas.

### Step 4 — Execute via CLI
GitHub: `gh api graphql -f query='...' -f owner="..." -f repo="..."`. Generic: `curl -s -X POST "$ENDPOINT" -H "Authorization: Bearer $TOKEN" -d "$(jq -n --arg query '...' '{query:$query}')"`. Errors array → read the message (permissions, invalid IDs, rate limits); 403 → token missing scope (`gh auth refresh -s <scope>`).

### Step 5 — Parse the response
Use `--jq` (gh) or pipe to jq. Extract single values (`.data.viewer.login`), iterate lists (`.data...nodes[] | ...`), or assign IDs to shell variables for later steps.

### Step 6 — Chain operations
Extract `id` fields in earlier queries and pass them as `ID!` variables to subsequent mutations (e.g., get repo ID → get category ID → create discussion). Node IDs are opaque strings (e.g., `R_kgDO...`) — never construct them manually. Use `set -e` so a failed step doesn't silently empty a variable; add `sleep 1` if rate-limited.

## Validation

- [ ] Introspection returns schema data
- [ ] Queries syntactically valid (no parser errors)
- [ ] Responses have `data` without `errors`
- [ ] Extracted values match types (IDs non-empty strings)
- [ ] Chained operations complete end-to-end

## Common Pitfalls

- Forgetting `!` on required variable types — check schema nullability.
- Using REST IDs in GraphQL — fetch opaque node IDs via GraphQL.
- Not paginating — use `first`/`after` with `pageInfo { hasNextPage endCursor }`.
- Hardcoding IDs — they differ between environments; query dynamically.
- Ignoring the `errors` array even when `data` is present (partial errors).
- Shell quoting issues with nested JSON — use `--jq` or pipe to jq.

## Related

- headless-web-scraping — fallback when no API exists
- serialize-data-formats — handling the JSON responses
