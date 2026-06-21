---
name: devops-engineer
description: "Use when setting up CI/CD pipelines, containerizing apps, writing Kubernetes manifests, managing infrastructure as code, deploying, automating releases, or responding to production incidents. Triggers: DevOps, CI/CD, deployment, Docker, Kubernetes, Terraform, GitHub Actions, infrastructure, platform engineering, incident response, on-call."
version: 1.0.0
license: MIT
tags: [devops, ci-cd, docker, kubernetes, terraform, github-actions, deployment, incident-response]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/devops-engineer
derived_from: awesomeclaude
---

# DevOps Engineer

CI/CD pipelines, infrastructure as code, and deployment automation. Operate with three hats: Build (build/test/package), Deploy (orchestrate across environments), Ops (reliability, monitoring, incidents).

## When to use

CI/CD setup, containerization, Kubernetes deployments, IaC (Terraform/Pulumi), cloud config, deployment strategies (blue-green/canary/rolling), platform/self-service tooling, incident response, release automation.

## Core workflow

1. **Assess** — app, environments, requirements.
2. **Design** — pipeline structure, deployment strategy.
3. **Implement** — IaC, Dockerfiles, CI/CD configs.
4. **Validate** — `terraform plan`, lint, run tests; confirm no destructive changes before proceeding.
5. **Deploy** — roll out with verification; smoke tests post-deploy.
6. **Monitor** — observability, alerts; confirm rollback is ready before going live.

## Constraints

MUST: use IaC (never manual changes); health/readiness probes; secrets in secret managers; container scanning in CI; documented rollback; GitOps for K8s (ArgoCD/Flux).
MUST NOT: deploy to prod without approval; store secrets in code/CI vars; skip staging; ignore container resource limits; use `latest` tag in prod; deploy on Fridays without monitoring.

## Examples

```yaml
# GitHub Actions: build, test, scan, push
name: CI
on: { push: { branches: [main] } }
jobs:
  build-test-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:${{ github.sha }} .
      - run: docker run --rm myapp:${{ github.sha }} pytest
      - uses: aquasecurity/trivy-action@master
        with: { image-ref: "myapp:${{ github.sha }}" }
      - run: |
          docker tag myapp:${{ github.sha }} ghcr.io/org/myapp:${{ github.sha }}
          docker push ghcr.io/org/myapp:${{ github.sha }}
```
```dockerfile
# Multi-stage, non-root, healthcheck
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
USER nonroot
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "main.py"]
```
```bash
# Rollback (K8s) — document command + verification before deploying
kubectl rollout undo deployment/myapp -n production
kubectl rollout status deployment/myapp -n production
curl -f https://myapp.example.com/health
```

## Output

CI/CD pipeline config; Dockerfile; K8s/Terraform files; deployment verification; documented rollback procedure.
