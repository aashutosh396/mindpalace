---
name: CI/CD Pipeline Builder
description: Use when setting up CI for a new project, refactoring existing pipelines, or standardizing deployment workflows across repos — generates GitHub Actions / GitLab CI from detected stack signals.
tags: [ci-cd, github-actions, gitlab-ci, pipeline, deployment, stack-detection, caching, deploy-gates, lint-test-build]
source: alirezarezvani/claude-skills
derived_from: ci-cd-pipeline-builder
---

# CI/CD Pipeline Builder

Generate pragmatic CI/CD pipelines from detected stack signals, not guesswork. Fast baseline generation, repeatable checks, environment-aware deployment stages.

## When to use
Bootstrapping CI for a new repo · replacing brittle copied pipeline files · migrating between GitHub Actions and GitLab CI · auditing whether pipeline steps match the actual stack · creating a reproducible baseline before custom hardening.

## Workflow
1. **Detect stack** from repository files (language/runtime/tooling) → text or JSON detection output.
2. **Generate pipeline** from the detection payload → GitHub Actions or GitLab CI YAML, with caching + matrix strategy based on the detected stack. (End-to-end from repo directly is also supported.)
3. **Validate before merge**: confirm `test`/`lint`/`build` commands actually exist in the project, run the pipeline locally where possible, document required secrets/env vars, keep deploy jobs gated by protected branches/environments.
4. **Add deployment stages safely**: start CI-only (lint/test/build) → add staging deploy with explicit environment context → add production deploy with a manual gate/approval → keep rollout/rollback commands explicit and auditable.

## Principles
Pipeline logic stays aligned with project lockfiles + build commands. Emit machine-readable detection for automation. Prefer incremental hardening over copying someone else's pipeline.
