---
name: Helm Chart Builder
description: Use when creating/reviewing Helm charts, designing values.yaml, writing template helpers, managing subcharts, or auditing chart security (RBAC, pod security, network policies) — opinionated, secure-by-default.
tags: [helm, kubernetes, chart, values-yaml, rbac, pod-security, network-policy, subcharts, helm-lint, devops]
source: alirezarezvani/claude-skills
derived_from: engineering/helm-chart-builder
---

# Helm Chart Builder

Production-grade Helm charts, sensible defaults, secure by design, no cargo-culting. Turns ad-hoc K8s manifests into maintainable, testable, reusable charts.

## /helm:create — scaffolding
1. **Identify workload type:** web service (Deployment+Service+Ingress) / worker (Deployment, no Service) / CronJob / stateful (StatefulSet+PVC+headless) / library (helpers only).
2. **Scaffold:** Chart.yaml, values.yaml, values.schema.json, .helmignore, templates/ (_helpers.tpl, deployment, service, ingress, serviceaccount, hpa, pdb, networkpolicy, configmap, secret, NOTES.txt, tests/), charts/.
3. **Chart.yaml:** apiVersion v2 (never v1); name = dir name; semver chart version; appVersion; description; type application|library. Pin deps `~X.Y.Z`; use `condition:` for optional subcharts; `alias:` for multiple instances; run `helm dependency update`.
4. **values.yaml:** inline comment per value; dev-friendly defaults; override-friendly (flat where possible); no hardcoded cluster values (registry/domain/storageClass).
5. **Validate:** `helm lint`, `helm template --debug`.

## /helm:review — analysis (severity-ranked)
Critical: no resource requests/limits. High: missing _helpers.tpl, hardcoded values/image tags in templates, missing standard `app.kubernetes.io/*` labels, missing liveness/readiness probes. Medium: no NOTES.txt, missing Chart.yaml fields, no imagePullPolicy, no anti-affinity, duplicate template code.

## /helm:security — audit
**Pod security (Critical/High):** no securityContext → add `runAsNonRoot`, `readOnlyRootFilesystem`; running as root → `runAsNonRoot: true`, `runAsUser: 1000`; privileged → false; capabilities → drop ALL, add only needed; `allowPrivilegeEscalation: false`; `seccompProfile.type: RuntimeDefault`.
**RBAC:** dedicated ServiceAccount (not default); `automountServiceAccountToken: false` unless K8s API needed; namespace Role over ClusterRole; no wildcard permissions (Critical).
**Network/secrets:** add NetworkPolicy (default-deny + allow); no secrets in values.yaml (use external/sealed secrets — Critical); add PodDisruptionBudget; remove hostNetwork/hostPID/hostIPC.

## Values design principles
Flat over nested (max 3 levels); group by resource (service.*, ingress.*); `enabled: true/false` for optional; camelCase keys; document every key; sensible dev defaults. Anti-patterns: hardcoded URLs/domains, secrets as defaults, undocumented values, values that don't work without overrides.

## Proactive triggers (flag unasked)
No _helpers.tpl · hardcoded image tag · no resource requests/limits · running as root · no NOTES.txt · secrets in values defaults · no probes · missing `app.kubernetes.io` labels.
