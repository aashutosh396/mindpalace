---
name: Senior DevOps
description: Use when setting up CI/CD pipelines, deploying applications, managing infrastructure-as-code, or implementing deployment automation across AWS/GCP/Azure — pipeline scaffolding, Terraform, blue-green/rolling deploys with rollback.
tags: [devops, ci-cd, terraform, kubernetes, blue-green, rolling-deploy, github-actions, iac, rollback, multi-cloud]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-devops
---

# Senior DevOps

CI/CD, IaC, containerization, deployment automation across AWS/GCP/Azure.

## Three Core Capabilities
- **Pipeline generation**: CI/CD for GitHub Actions or CircleCI with build/test/security-scan/deploy stages. Typical GH Actions: checkout → setup → `npm ci` → lint → test --coverage → docker build-push (on main) → deploy (e.g. `aws ecs update-service --force-new-deployment`).
- **Terraform scaffolding**: generate + validate IaC modules (AWS ECS/GCP GKE/Azure AKS). Enforces consistent module structure; runs `terraform validate` + `plan` before any apply.
- **Deployment manager**: K8s manifests + ordered kubectl runbooks for blue-green / rolling with health-check gates before traffic switch + rollback runbooks. **Writes manifests and prints commands — never applies to cluster itself, so every change gets human review.**

## Deployment Workflow
1. Scaffold/update Terraform → `terraform init`/`validate`/`plan -out=tfplan` → review diff → `apply tfplan` → verify resources healthy.
2. Generate pipeline → build + tag image (`$(git rev-parse --short HEAD)`) → push → deploy with `--health-check-url` gate → verify pods (`kubectl rollout status`) → switch traffic (`kubectl patch service ... slot:blue`).
3. Rollback: `rollback --to-version=X` or `kubectl rollout undo` → verify pods + health endpoint.

## Blue-Green Pattern
Slot label distinguishes blue/green deployments. `readinessProbe` (`/healthz`, initialDelay, period) gates traffic switch — pod must pass before switching. Set resource requests + limits.

## Cloud-Agnostic IaC
**Terraform/OpenTofu (default)**: single HCL across all clouds, remote state backends, plan-before-apply. **Pulumi**: when team prefers TS/Python/Go/C# over HCL. **Cloud-native** (CloudFormation/Bicep/Deployment Manager): only if 100% committed to one cloud AND it offers a feature Terraform can't replicate.

## Multi-Cloud Decision
Default single-cloud (lower ops complexity, deeper managed-service integration, committed-use discounts). Multi-cloud only with concrete driver: compliance/data-residency, acquisition on another cloud, best-of-breed need. Hybrid: regulated workloads on-prem + burst in cloud. Don't add a second cloud for theoretical redundancy.
