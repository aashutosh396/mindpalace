---
name: Terraform Patterns
description: Use when designing Terraform modules, setting up state backends, reviewing or hardening .tf code, planning multi-region/multi-cloud, or wiring Terraform CI/CD — opinionated IaC decisions, not a tutorial.
tags: [terraform, iac, opentofu, terragrunt, state-management, modules, infracost, multi-region, hcl, provider-aliases]
source: alirezarezvani/claude-skills
derived_from: engineering/terraform-patterns
---

# Terraform Patterns

Concrete decisions for infrastructure code that doesn't break at 3 AM: module design, state management, provider patterns, security hardening, CI/CD.

## Review checklist
**Module:** variables have descriptions + type constraints; outputs expose only what consumers need (specific attributes, not whole resources); consistent naming `{provider}_{type}_{purpose}`; locals for computed/DRY values; nothing hardcoded.
**State:** remote backend (S3+DynamoDB / GCS / Azure Blob / TF Cloud); locking enabled; encryption at rest; no secrets in state (or restricted access); directory or workspace isolation per environment.
**Providers:** pessimistic version pin `~> 5.0`; `required_providers` in `terraform {}`; aliases for multi-region/account; no provider config in child modules.
**Security:** no hardcoded secrets/keys; IAM least-privilege (no `Action: "*"`); encryption on storage/DB/secrets; no `0.0.0.0/0` ingress on 22/3389; `sensitive = true` on secret vars; `prevent_destroy` on stateful resources.

## Module layout
`main.tf · variables.tf · outputs.tf · versions.tf · locals.tf · data.tf · README.md`. Composition: root calls child modules; child modules never call other child modules; pass values explicitly (no hidden data-source lookups in children); provider config only in root.

## Project structure decision
Flat module — single app, <20 resources, one team. Nested modules (`environments/{dev,staging,prod}` + `modules/`) — multiple envs, shared patterns. Terragrunt mono-repo — 3+ envs with identical structure, shared backend config, cross-module dependencies (skip it for a single env or small team — it's another binary + learning curve).

## State backend
TF Cloud → native backend (locking, encryption, RBAC built in) · AWS → S3 + DynamoDB · GCP → GCS · Azure → Blob · else → Consul/Postgres. Separate state file per environment (never one shared file).

## Provider patterns
Multi-region via `alias`; multi-account via `assume_role`; multi-cloud only with a concrete business reason (data residency, existing multi-cloud workloads) — "avoiding lock-in" alone is not enough; it doubles operational complexity.

## CI/CD
PR → `init` + `validate` + `plan -out`, post plan as PR comment. Merge to main → `apply` gated by a protected environment. Scheduled drift detection via `plan -detailed-exitcode` (exit 2 = drift → alert). Add Infracost for cost-diff PR comments with budget thresholds.

## OpenTofu
MPL-2.0 open-source fork; state files compatible; drop-in `tofu` binary. Choose it for a fully open-source supply chain or client-side state encryption without TF Cloud.

## Import existing infra
Write an empty resource block → `terraform import <addr> <id>` → `plan` → fill the block until plan shows no changes. Bulk: `plan -generate-config-out`. Always back up state before manipulation (`state pull > backup.tfstate`).

## Proactive triggers
No remote backend · provider without version constraint · hardcoded secrets · IAM `*` actions · SG open to 0.0.0.0/0 on SSH/RDP · no state locking · resources without tags · missing `prevent_destroy` on DB/storage.
