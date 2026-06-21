---
name: code-documenter
description: "Use when adding docstrings to functions/classes, creating API documentation, building documentation sites, or writing tutorials and user guides. Covers Google/NumPy/Sphinx docstrings, JSDoc, OpenAPI/Swagger specs, doc portals (Docusaurus/MkDocs), and validation. Triggers: documentation, docstrings, OpenAPI, Swagger, JSDoc, comments, API docs, tutorials, user guides, doc site."
version: 1.0.0
license: MIT
tags: [documentation, docstrings, jsdoc, openapi, api-docs, tutorials, doc-sites, coverage]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/code-documenter
derived_from: awesomeclaude
---

# Code Documenter

Inline documentation, API specs, doc sites, and developer guides.

## When to use

Any task involving code documentation, API specs, or developer-facing guides.

## Core workflow

1. **Discover** — ask for format preference and exclusions.
2. **Detect** — identify language and framework.
3. **Analyze** — find undocumented code.
4. **Document** — apply a consistent format.
5. **Validate** — test all examples: Python `python -m doctest file.py` / `pytest --doctest-modules`; TS/JS `tsc --noEmit`; OpenAPI `npx @redocly/cli lint openapi.yaml`. Fix and re-validate on failure.
6. **Report** — coverage summary.

## Quick-reference examples

```python
def fetch_user(user_id: int, active_only: bool = True) -> dict:
    """Fetch a single user record by ID.

    Args:
        user_id: Unique identifier for the user.
        active_only: When True, raise an error for inactive users.
    Returns:
        A dict with user fields (id, name, email, created_at).
    Raises:
        ValueError: If user_id is not a positive integer.
        UserNotFoundError: If no matching user exists.
    """
```
```typescript
/**
 * Fetches a paginated list of products.
 * @param {string} categoryId - The category to filter by.
 * @param {number} [page=1] - Page number (1-indexed).
 * @returns {Promise<ProductPage>} A page of product records.
 * @throws {NotFoundError} If the category does not exist.
 * @example const page = await fetchProducts('electronics', 2, 10);
 */
```

## Constraints

MUST: ask format preference before starting; detect framework for correct API-doc strategy; document all public functions/classes; include parameter types + descriptions; document exceptions/errors; test code examples; generate coverage report.
MUST NOT: assume docstring format; apply wrong API-doc strategy for the framework; write untested/inaccurate docs; skip error documentation; verbosely document obvious getters/setters; create hard-to-maintain docs.

## Output formats

- Code docs: documented files + coverage report
- API docs: OpenAPI specs + portal config
- Doc sites: config + content structure + build instructions
- Guides/tutorials: structured markdown with examples + diagrams
