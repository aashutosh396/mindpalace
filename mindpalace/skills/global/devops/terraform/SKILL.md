---
name: terraform
description: "Use when writing, reviewing, or generating Terraform/HCL infrastructure-as-code — .tf files, providers, modules, variables, outputs, for_each/count, terraform fmt/validate/plan/apply, .tftest.hcl tests, importing existing cloud resources, or refactoring monoliths into reusable modules."
version: 1.0.0
license: MPL-2.0
tags: [terraform, hcl, iac, infrastructure-as-code, hashicorp, modules, terraform-test, devops, aws, cloud]
source: https://github.com/hashicorp/agent-skills
derived_from: awesomeclaude
prerequisites:
  commands: [terraform]
---

# Terraform

HashiCorp's official agent guidance for authoring, testing, importing, and
refactoring Terraform infrastructure-as-code. Follows the official
[Terraform Style Guide](https://developer.hashicorp.com/terraform/language/style).

## When to use

- Writing or reviewing any `.tf` / HCL configuration.
- Generating resources, variables, outputs, modules.
- Importing existing (unmanaged) cloud resources into Terraform.
- Writing `.tftest.hcl` tests or refactoring configs into reusable modules.

## File organization

One concern per file (do not cram everything into `main.tf`):

| File | Purpose |
|------|---------|
| `terraform.tf` | `required_version` + `required_providers` constraints |
| `providers.tf` | Provider configurations |
| `main.tf` | Primary resources and data sources |
| `variables.tf` | Input variables (alphabetical) |
| `outputs.tf` | Outputs (alphabetical) |
| `locals.tf` | Local values |

## Generation strategy (in order)

1. Provider config + version constraints.
2. Data sources before the resources that depend on them.
3. Resources in dependency order.
4. Outputs for key attributes.
5. Variables for every configurable value.

## Style rules

- Two spaces per nesting level, no tabs; align `=` for consecutive args.
- Block order inside a resource: meta-arguments (`count`/`for_each`) first,
  then arguments, then nested blocks, then `lifecycle` last.
- Names: lowercase_with_underscores, descriptive nouns, singular, exclude the
  resource type. Use `main` when only one instance exists and no better name fits.
  Bad: `aws_instance.web_apis`; Good: `aws_instance.web_api`, `aws_vpc.main`.
- Every **variable** has `type` + `description` (and `validation` where useful);
  mark secrets `sensitive = true`.
- Every **output** has `description`; mark secret outputs `sensitive = true`.

## Dynamic creation

- Prefer `for_each` (named, stable keys) over `count` for multiple resources.
- Use `count = condition ? 1 : 0` only for conditional creation.

## Version pinning

```hcl
terraform {
  required_version = ">= 1.14"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
```

Operators: `=` exact, `>=` floor, `~> 1.0` pessimistic (rightmost increments),
`>= 1.0, < 2.0` range. Use latest provider major + latest Terraform minor unless
constrained by the lock file or dependent modules.

## Validate before commit

```bash
terraform fmt -recursive
terraform validate
```

Optional: `tflint` (lint), `checkov` / `tfsec` (security scan).

## Version control hygiene

- Never commit: `terraform.tfstate*`, `.terraform/`, `*.tfplan`, sensitive `*.tfvars`.
- Always commit: all `.tf` files and `.terraform.lock.hcl`.

## Testing (`.tftest.hcl`)

Terraform's built-in framework runs against temporary resources, protecting real
state. Concepts: a **test file** holds `run` blocks; each `run` is one scenario
with optional `variables`/`providers` and `assert` blocks; mode is `apply`
(default, real resources) or `plan` (logic only). **Mock providers** simulate a
provider without real infra (Terraform 1.7.0+ only). Run with `terraform test`.

## Importing existing resources (Search + bulk import)

For bringing unmanaged infra under Terraform / migrating to IaC:

1. Identify the target resource type (e.g. `aws_s3_bucket`).
2. Verify provider list-resource support FIRST — requires Terraform >= 1.14 and a
   provider with list-resource support (latest provider version).
3. Use Terraform Search (`list` / `tfquery` block) to discover resources, then
   generate config + `import` blocks for bulk import.

## Code review checklist

- [ ] `terraform fmt` clean, `terraform validate` passes.
- [ ] Standard file layout; vars have type+description; outputs have description.
- [ ] Descriptive snake_case names; version constraints pinned.
- [ ] Secrets marked `sensitive`; no hardcoded credentials.

## Notes / gotchas

- The upstream repo splits Terraform into many sub-skills under
  `terraform/` (code-generation: style-guide, test, search-import,
  azure-verified-modules; module-generation: refactor-module, terraform-stacks;
  provider-development: provider-resources/actions/docs/tests, new-terraform-provider).
  Helper scripts and deep references (e.g. `terraform-search-import/scripts/list_resources.sh`,
  `terraform-test/references/{MOCK_PROVIDERS,CI_CD,EXAMPLES}.md`,
  `terraform-stacks/references/*`) live at those source paths — fetch on demand
  rather than duplicating here.
- Terraform Cloud/Enterprise work can use `terraform-mcp-server` with
  `TFE_TOKEN` + `TFE_ADDRESS` env vars.
- For provider *development* (Go) or Terraform Stacks orchestration, pull the
  dedicated sub-skill from the source repo.
