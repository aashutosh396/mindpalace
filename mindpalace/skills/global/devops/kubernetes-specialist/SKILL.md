---
name: kubernetes-specialist
description: "Use when deploying or managing Kubernetes workloads — deployment manifests, pod security, RBAC, NetworkPolicies, Helm charts, debugging pod crashes, resource right-sizing, GitOps (ArgoCD/Flux), service mesh, multi-cluster. Triggers: Kubernetes, K8s, kubectl, Helm, container orchestration, pod deployment, RBAC, NetworkPolicy, Ingress, StatefulSet, CRD, ArgoCD, Istio, multi-cluster."
version: 1.0.0
license: MIT
tags: [kubernetes, k8s, helm, rbac, networkpolicy, gitops, argocd, service-mesh]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/kubernetes-specialist
derived_from: awesomeclaude
---

# Kubernetes Specialist

Deploy, secure, and operate Kubernetes workloads.

## When to use

Deployment manifests; pod security; RBAC + service accounts; NetworkPolicies; Helm charts; debugging crashes/CrashLoopBackOff; resource limits + right-sizing; GitOps pipelines; service mesh; multi-cluster.

## Core workflow

1. **Define workload** — Deployment/StatefulSet, replicas, probes, resource requests/limits.
2. **Secure** — least-privilege RBAC, ServiceAccount, securityContext (non-root, read-only FS), NetworkPolicy default-deny.
3. **Package** — Helm chart with values per environment.
4. **Debug** — `kubectl describe`/`logs`/`events`; check OOMKills, image pull, probe failures.
5. **Operate** — GitOps (ArgoCD/Flux); right-size from actual usage (VPA/metrics).

## Key practices

- Always set resource requests + limits; liveness/readiness/startup probes.
- securityContext: `runAsNonRoot`, drop capabilities, read-only root FS.
- RBAC least privilege; one ServiceAccount per workload; no cluster-admin for apps.
- NetworkPolicy default-deny, then allow explicitly.
- Helm for templating; GitOps as the deploy mechanism (declarative, auditable).
- Debug crashes: `kubectl logs --previous`, describe for events/OOM, check probes.

## Constraints

MUST: resource requests + limits on every container; readiness + liveness probes; least-privilege RBAC; non-root securityContext; default-deny NetworkPolicy; declarative manifests in Git.
MUST NOT: run as root / privileged without need; `latest` image tags; cluster-admin for apps; secrets in plain manifests (use Secrets/external manager); skip probes; `kubectl apply` ad hoc to prod (use GitOps).

## Output

1. Deployment/StatefulSet manifest (probes + resources + securityContext). 2. RBAC + NetworkPolicy. 3. Helm chart / GitOps wiring. 4. Brief note on security + right-sizing.

## Knowledge

Kubernetes, kubectl, Deployments/StatefulSets, probes, resource requests/limits, RBAC, ServiceAccounts, securityContext, NetworkPolicy, Helm, ArgoCD/Flux GitOps, Istio/Linkerd, VPA/HPA, CRDs.
