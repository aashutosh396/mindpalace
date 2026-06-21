---
name: fastapi-expert
description: "Use when building high-performance async Python APIs with FastAPI and Pydantic V2. Invoke for REST endpoints, Pydantic models, async SQLAlchemy, JWT auth, WebSocket endpoints, OpenAPI docs. Triggers: FastAPI, Pydantic, async Python, Python API, REST API Python, SQLAlchemy async, JWT authentication, OpenAPI, Swagger Python."
version: 1.0.0
license: MIT
tags: [fastapi, pydantic, async, python, sqlalchemy, jwt, websocket, openapi]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/fastapi-expert
derived_from: awesomeclaude
---

# FastAPI Expert

Async Python APIs with FastAPI + Pydantic V2, production-grade.

## When to use

REST APIs with FastAPI; Pydantic V2 validation schemas; async DB (SQLAlchemy); JWT auth; WebSocket endpoints; OpenAPI docs; performance tuning.

## Core workflow

1. **Analyze** — endpoints, data models, auth needs.
2. **Design schemas** — Pydantic V2 models.
3. **Implement** — async endpoints with dependency injection.
4. **Secure** — auth, authorization, rate limiting.
5. **Test** — async tests (pytest + httpx); verify `/docs`. Checkpoint each step: schemas validate, endpoints return correct codes.

## Key pattern

```python
DbDep = Annotated[AsyncSession, Depends(get_db)]

@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, db: DbDep) -> UserResponse:
    if await crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return await crud.create_user(db, payload)

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()
```

## Constraints

MUST: Pydantic V2 models for I/O validation; async endpoints + async SQLAlchemy; dependency injection (`Depends`); `response_model` on endpoints; explicit HTTP status codes; hash passwords; async tests.
MUST NOT: blocking I/O in async routes; raw SQL without params; leak ORM models in responses (use response schemas); store secrets in code; skip input validation.

## Output

1. Pydantic schemas. 2. Async routers + CRUD layer. 3. Auth/security wiring. 4. pytest+httpx tests. 5. Brief note on async/validation decisions.

## Knowledge

FastAPI, Pydantic V2, async/await, SQLAlchemy (async), Alembic, JWT (python-jose/passlib), WebSockets, dependency injection, OpenAPI/Swagger, pytest, httpx.
