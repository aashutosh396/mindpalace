---
name: aws-cdk
description: "Use when building AWS infrastructure as code with the Cloud Development Kit — creating or refactoring CDK stacks/constructs, defining Lambda in CDK, running cdk synth/cdk deploy, or when the user mentions CDK, CloudFormation, IaC, cdk-nag, NodejsFunction, or programmatic AWS provisioning in TypeScript/Python."
version: 1.0.0
license: MIT
tags: [aws, cdk, cloudformation, iac, infrastructure, devops, lambda, typescript, cdk-nag, deployment]
source: https://github.com/zxkane/aws-skills
derived_from: awesomeclaude
prerequisites:
  commands: [cdk, npm, aws]
---

# AWS CDK Development

Guidance for building AWS infrastructure with the Cloud Development Kit (CDK) in
TypeScript or Python. Pairs well with AWS MCP servers for fetching current AWS
facts beyond the knowledge cutoff.

## When to use

- Creating or refactoring CDK stacks / constructs
- Implementing Lambda functions inside CDK
- Validating a stack before deploy (`cdk synth`, cdk-nag)
- Confirming AWS service capabilities / regional availability before coding

## Verify AWS facts first

Do not answer AWS service questions from memory — APIs, runtimes, limits, and
regional availability change. Use AWS docs MCP tools when available
(`mcp__aws-mcp__*` / `mcp__*awsdocs*__*`). For CDK construct lookups and
best-practice patterns, AWS Labs ships `awslabs.aws-iac-mcp-server` (covers CDK +
CloudFormation; the older `awslabs.cdk-mcp-server` is deprecated):

```bash
claude mcp add aws-iac uvx awslabs.aws-iac-mcp-server@latest
```

Verify before implementing: new service features, region availability, API
params, service limits/quotas, security best practices.

## Core principles

### Resource naming — let CDK generate names

CRITICAL: do NOT set optional resource names (e.g. `functionName`, `tableName`).
Auto-generated names enable reusable patterns, parallel deployments, and stack
isolation without collisions.

```typescript
// BAD — explicit name blocks reuse / parallel deploys
new lambda.Function(this, 'MyFunction', { functionName: 'my-lambda', /* ... */ });

// GOOD — CDK generates StackName-MyFunctionXXXXXX
new lambda.Function(this, 'MyFunction', { /* ... */ });
```

For dev/staging/prod isolation, use separate AWS accounts (Security Pillar), not
name prefixes in one account.

### Lambda constructs (auto-bundle)

- TypeScript/JS: `NodejsFunction` from `aws-cdk-lib/aws-lambda-nodejs` —
  `{ entry: 'lambda/handler.ts', handler: 'handler' }`. Handles bundling +
  transpilation.
- Python: `PythonFunction` from `@aws-cdk/aws-lambda-python-alpha` —
  `{ entry: 'lambda', index: 'handler.py', handler: 'handler' }`. Handles
  dependency packaging.

## Pre-deployment validation (multi-layer)

1. **cdk-nag at synth time** (required). Install and wire via Aspects:
   ```bash
   npm install --save-dev cdk-nag
   ```
   ```typescript
   import { Aspects } from 'aws-cdk-lib';
   import { AwsSolutionsChecks } from 'cdk-nag';
   Aspects.of(app).add(new AwsSolutionsChecks());
   ```
   Available in all CDK languages. Suppress legitimate findings with a documented
   reason via `NagSuppressions.addResourceSuppressions(resource, [{ id, reason }])`.
2. **Build + tests**: `npm run build` (or lang equivalent), then `npm test` /
   `pytest` / `mvn test`.
3. **Synth check**: `cdk synth` (runs cdk-nag automatically through Aspects).
   The source repo also ships a `scripts/validate-stack.sh` meta-check
   (language detection, template size / resource-count analysis, synth success).

## Workflow

Design → verify AWS services (MCP) → implement constructs → validate (above) →
`cdk synth` → review generated CloudFormation → `cdk deploy` → confirm resources.

Stack organization: nested stacks for complex apps, logical construct boundaries,
export cross-stack values, use CDK context for per-environment config. Test by
unit-testing constructs and snapshot-testing synthesized templates.

## Gotchas

- `cdk deploy` hits the live account — confirm identity first:
  `aws sts get-caller-identity --query Account --output text`.
- If `.github/workflows/` exists, make those CI checks pass before committing.

## Source helper files (not copied here)

- `plugins/aws-iac/skills/aws-cdk-development/references/cdk-patterns.md` —
  patterns, anti-patterns, security/cost/perf guidance.
- `plugins/aws-iac/skills/aws-cdk-development/scripts/validate-stack.sh` —
  pre-deploy validation script.
