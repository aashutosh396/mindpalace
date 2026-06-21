---
name: optimize-cloud-costs
description: "Use when cloud/Kubernetes spend is growing without matching value — for cost visibility (Kubecost/OpenCost), right-sizing, HPA/VPA autoscaling, spot/preemptible instances, resource quotas, budget alerts, and showback/chargeback FinOps. Triggers: cloud costs, FinOps, right-sizing, over-provisioning, Kubecost, spot instances, cost allocation."
version: 1.0.0
license: MIT
tags: [cost-optimization, finops, kubecost, hpa, vpa, spot-instances, kubernetes, resource-management]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/optimize-cloud-costs
derived_from: awesomeclaude
---

# Optimize Cloud Costs

Reduce cloud spend on Kubernetes workloads through visibility, right-sizing, autoscaling, spot capacity, and quotas — without breaking SLOs.

## When to Use

- Cloud costs growing without corresponding business value
- Need cost allocation by team, app, or environment
- Resource requests/limits misaligned with actual usage
- Manual scaling causing over-provisioning
- Implementing showback/chargeback or a FinOps culture

## Inputs

- Required: running cluster, cloud billing API access, metrics-server or Prometheus
- Optional: historical usage, allocation requirements, SLOs, budget targets

## Procedure

### Step 1 — Deploy cost visibility
Install Kubecost or OpenCost (Helm), wired to Prometheus, and configure cloud billing integration (AWS Athena/CUR, GCP service account, Azure config). Initial cloud sync can take 24-48h. Verify the UI shows cost by namespace/deployment/pod and the allocation API returns data.

### Step 2 — Analyze utilization
Compare requests vs actual usage (`kubectl top pods`, Kubecost request-sizing recommendations at `/model/savings/requestSizing?window=7d`). Identify over-provisioned and idle resources. Wait at least 7 days of data before acting.

### Step 3 — Horizontal Pod Autoscaling (HPA)
Scale replicas on CPU/memory or custom metrics for stateless, scalable workloads. Set sensible min/max replicas and target utilization based on P95/P99, not average.

### Step 4 — Vertical Pod Autoscaling (VPA)
Right-size per-pod requests/limits. Start in "Off" (recommendation) mode, review for ~30 days, then apply gradually. Never run VPA and HPA on the same metric.

### Step 5 — Spot / preemptible instances
Move fault-tolerant, stateless workloads to spot capacity for large savings. Never databases, stateful, or single-replica critical services. Always use PodDisruptionBudgets and node affinity/taints.

### Step 6 — Resource quotas and budget alerts
Apply ResourceQuotas per namespace/team and LimitRanges for defaults. Configure budget alerts in Kubecost/cloud billing. Start with showback (informational) before chargeback.

## Validation

- [ ] Cost visibility tool reporting per-namespace/team allocation
- [ ] Right-sizing recommendations reviewed against SLOs
- [ ] HPA configured with appropriate min/max and percentile targets
- [ ] VPA validated in Off mode before applying
- [ ] Spot only on fault-tolerant workloads with PDBs
- [ ] Quotas and budget alerts in place

## Common Pitfalls

- Aggressive right-sizing causing OOMKills/throttling — apply gradually.
- HPA + VPA on the same metric conflict.
- Spot for stateful/critical services.
- Acting on too little data (need 7-30-90 day windows).
- Sizing on average instead of P95/P99 (burst throttling).
- Ignoring egress, storage (unused PVCs), and total cost of ownership.
- Quotas too restrictive; chargeback before teams trust the data.

## Related

- conduct-post-mortem — for cost-incident retrospectives
