---
name: fullstack-guardian
description: "Use when implementing features across frontend and backend, building REST APIs with corresponding UI, connecting components to endpoints, creating end-to-end data flows from database to UI, or implementing CRUD with forms. Addresses Frontend, Backend, and Security in one workflow with layered defenses. Triggers: fullstack, implement feature, build feature, create API, frontend and backend, full stack, new feature, end-to-end, CRUD."
version: 1.0.0
license: MIT
tags: [fullstack, frontend, backend, security, api, crud, end-to-end, web-development]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/fullstack-guardian
derived_from: awesomeclaude
---

# Fullstack Guardian

Security-focused full-stack development across the entire application stack — database to UI — addressing Frontend, Backend, and Security simultaneously.

## When to use

Full-stack feature work, REST APIs with UI, connecting components to endpoints, end-to-end data flows, CRUD with forms, authenticated routes with views.

## Core workflow

1. **Gather requirements** — feature scope and acceptance criteria.
2. **Design solution** — all three perspectives (Frontend/Backend/Security).
3. **Write technical design** — document approach in `specs/{feature}_design.md`.
4. **Security checkpoint** — before writing code, confirm auth, authz, validation, and output encoding are addressed.
5. **Implement** — build incrementally, testing each component.
6. **Hand off** — to QA (Test Master) and deployment (DevOps).

## Constraints

MUST: address Frontend, Backend, Security; validate input on both client AND server; parameterized queries (prevent SQLi); sanitize output (prevent XSS); error handling at every layer; log security-relevant events; write the plan before coding; test each component as built.
MUST NOT: skip security; trust client-side validation alone; expose sensitive data in API responses; hardcode credentials/secrets; build without acceptance criteria; happy-path-only error handling.

## Three-perspective example

```python
# [Backend] Authenticated route, parameterized query, scoped response
@router.get("/users/{user_id}/profile", dependencies=[Depends(require_auth)])
async def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")  # before any DB access
    row = await db.fetchone("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return ProfileResponse(**row)  # explicit schema — no password/token leakage
```
```typescript
// [Frontend] Calls endpoint, handles errors; client guard is never the only guard
async function fetchProfile(userId: number): Promise<Profile> {
  if (!Number.isInteger(userId) || userId <= 0) throw new Error("Invalid user ID");
  const res = await apiFetch(`/users/${userId}/profile`);  // attaches auth header
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
```
[Security] Auth enforced server-side (client header is convenience, not the gate); response schema excludes sensitive fields; 403 before DB access avoids timing leak.

## Output

1. Technical design doc (if non-trivial)
2. Backend code (models, schemas, endpoints)
3. Frontend code (components, hooks, API calls)
4. Brief security notes
