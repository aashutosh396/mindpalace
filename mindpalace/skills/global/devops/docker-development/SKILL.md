---
name: Docker Development
description: Use when optimizing a Dockerfile, writing docker-compose, building multi-stage images, or auditing container security — concrete decisions for smaller images, faster builds, and reduced attack surface.
tags: [docker, dockerfile, docker-compose, multi-stage-build, container-security, image-size, layer-caching, distroless, buildkit]
source: alirezarezvani/claude-skills
derived_from: engineering/docker-development
---

# Docker Development

Concrete decisions for production-grade containers: optimization, multi-stage builds, compose orchestration, security hardening.

## Dockerfile optimization
**Base image:** specific tags (never `:latest` in prod); slim/alpine variants; pin digest in CI; match base to runtime (don't use `python:3.12` for a compiled binary).
**Layers:** combine related `RUN` with `&& \`; order least-changing first (deps before source); clean package-manager cache in the same `RUN`; use `.dockerignore`; separate build deps from runtime deps.
**Build cache:** COPY dependency files (package.json/requirements.txt/go.mod) before source; install deps in a layer separate from code copy; BuildKit cache mounts `--mount=type=cache`; avoid `COPY . .` before dependency install.
**Multi-stage:** stage 1 build (full SDK + dev deps), stage 2 runtime (minimal base, prod artifacts only); `COPY --from=builder` only what's needed; final image has NO build tools, source, or dev deps.

## Base image decision
Compiled binary (Go/Rust/C) → distroless/static or scratch · need shell for debug → alpine · need glibc → slim · need many OS packages → debian-slim · few → alpine + apk.

## docker-compose best practices
**Services:** `depends_on` with `condition: service_healthy`; healthcheck on every service; resource limits (`mem_limit`, `cpus`); named volumes; pinned versions.
**Networking:** explicit networks; separate frontend/backend; `internal: true` for backend-only; expose only what needs external access.
**Environment:** `env_file` for secrets (never inline); `.env` in `.gitignore`; `${VAR:-default}` substitution; document required vars.
**Dev vs prod:** profiles or override files; dev = bind mounts + debug ports; prod = named volumes + `restart: unless-stopped` + no debug ports.

## Security audit
Critical: running as root (add `USER nonroot`); secrets in ENV/ARG (use BuildKit `--mount=type=secret`); privileged; sensitive host mounts (`/etc`, docker.sock). High: `:latest`; all capabilities retained (`cap_drop: [ALL]`); host network mode. Medium: no healthcheck; writable root FS (`read_only: true`); no resource limits.

## Proactive triggers
`:latest` tag · no `.dockerignore` (add `.git`, `node_modules`, `__pycache__`, `.env`) · `COPY . .` before deps install · running as root · secrets baked into layers · image >1GB (multi-stage required) · no healthcheck · `apt-get` without `rm -rf /var/lib/apt/lists/*` in the same RUN.
