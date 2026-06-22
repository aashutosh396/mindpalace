---
name: Kubernetes Operator
description: Use when building or auditing a Kubernetes Operator — designing a CRD, writing a reconcile loop, choosing a framework (kubebuilder/operator-sdk/KOPF), or scoring against OperatorHub capability levels. Not a generic k8s skill.
tags: [kubernetes, operator, crd, reconcile-loop, controller-runtime, kubebuilder, operator-sdk, kopf, finalizers, capability-levels]
source: alirezarezvani/claude-skills
derived_from: engineering/kubernetes-operator
---

# Kubernetes Operator

Most operator bugs are reconcile-loop bugs, not Kubernetes bugs: missing finalizers, blocking calls, no requeue on transient errors, status drift, RBAC over-grants.

## Core principle: an operator is a reconcile loop, not a script
```
observe(actual) → desired = read(spec) → diff → act → update(status) → requeue / done
```
Operators fail when they: treat reconcile as imperative ("do A then B then C") instead of declarative (make actual=desired, idempotently); don't requeue transient failures; skip finalizers (orphan resources); mutate spec instead of status; skip the status subresource (status updates re-trigger spec reconciles → loop); block in reconcile; forget leader election (split-brain on multi-replica).

## When NOT to use
Plain Helm packaging, standard kubectl/blue-green deploys, general k8s security posture, or just running a workload (that's a Deployment/Job).

## CRD design principles
1. **status = controller's view of the world; spec = what the user wants.**
2. Use the **status subresource** (without it, status updates loop).
3. Use **Conditions** (`Ready`, `Reconciling`, `Degraded`) — each with reason + message.
4. Add **finalizers** (deletion otherwise races the controller, orphans external resources).
5. **Version from day 1** (`v1alpha1`→`v1beta1`→`v1`); plan a conversion webhook.
6. Validate via **OpenAPI v3 schema** (fail at admission, not in the controller).
7. `additionalPrinterColumns` for `kubectl get` (Age, Phase, Ready minimum).
8. Namespace CRDs unless they manage cluster-scoped resources.

## Reconcile loop principles
Idempotent (reconcile same state twice → same result, zero side effects) · read once, decide, act · update status not spec · return errors that requeue (`ctrl.Result{RequeueAfter}`) · never block (no `time.Sleep`, no long uncontexted HTTP) · use the cached client · leader-elect when >1 replica · set OwnerReferences (free cascading deletion).

## Framework choice
Go shop → **kubebuilder** · Python shop → **KOPF** · can't pick a language → **metacontroller** (webhook-based) · OpenShift target → **operator-sdk** · JVM → **java-operator-sdk**. Build a 1-week POC before committing.

## OperatorHub capability levels
L1 Basic Install · L2 Seamless Upgrades (PDBs, conversion webhooks) · L3 Full Lifecycle (backups, restores, recovery) · L4 Deep Insights (metrics, Prometheus rules, alerts) · L5 Auto Pilot. Reach L3 before public release.

## Workflows
**Bootstrap (Go+kubebuilder):** pick Group/Version/Kind → `kubebuilder init` + `create api` → validate the CRD, fix every WARN before controller code → implement reconcile (simplest correct version first) → lint the controller → confirm L1 → test in kind → add status conditions, aim for L2 in the same PR.
**Audit:** capability audit + CRD validate + reconcile lint → triage (FAIL blocks release, WARN = issue within 30 days) → document current level → plan one level advancement per quarter.

## Anti-patterns
`time.Sleep` in reconcile (use `RequeueAfter`) · `Client.Update` to set status (use `Status().Update`) · no leader election + 2+ replicas · no finalizer · CRD without status subresource · reconcile >200 lines (extract `reconcileXxx` per condition) · `x-kubernetes-preserve-unknown-fields: true` on spec root · imperative reconcile.
