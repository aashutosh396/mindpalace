---
name: Azure Cloud Architect
description: Use when designing Azure infrastructure, writing Bicep/ARM templates, optimizing Azure costs, or migrating to Azure — produces pattern recommendations, IaC, cost analysis, and a security review.
tags: [azure, bicep, arm, aks, app-service, azure-functions, cosmos-db, cost-optimization, iac, cloud-architecture]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/azure-cloud-architect
---

# Azure Cloud Architect

Design scalable, cost-effective Azure architectures with Bicep IaC. Six-step workflow.

## Step 1 — Gather Requirements
Collect: app type (web/mobile/data-pipeline/SaaS/microservices), users + RPS, monthly budget, team size + Azure maturity, compliance (GDPR/HIPAA/SOC2/ISO27001), availability SLA + RPO/RTO, region/data-residency.

## Step 2 — Pick a Pattern
Match requirements to one:
- **App Service Web**: Front Door + App Service + Azure SQL + Redis. Managed, autoscale, deployment slots.
- **Microservices on AKS**: AKS (3 node pools: system/app/jobs) + Service Bus + Cosmos DB + API Management.
- **Serverless Event-Driven**: Functions + Event Grid + Service Bus + Cosmos DB.
- **Data Pipeline**: Event Hubs + Stream Analytics/Functions + Data Lake Gen2 + Synapse + Power BI.

Validation checkpoint: pattern must match team operational maturity AND compliance before proceeding.

## Step 3 — Generate IaC (Bicep, not ARM JSON)
Prefer Bicep: compiles to ARM, cleaner syntax, modules, first-party. Core web-app resources: App Service Plan (PremiumV3, Linux `reserved: true`), App Service (`httpsOnly`, `minTlsVersion 1.2`, `ftpsState Disabled`, SystemAssigned identity), Azure SQL (Entra-only auth, serverless `GP_S_Gen5`, autoPause). Add Front Door, Key Vault, Managed Identity, diagnostics.

## Step 4 — Review Costs
Output: monthly breakdown by service, right-sizing (e.g. SQL tier down), Reserved Instances / Savings Plans, blob tier transitions (Cool for >30 days), kill idle resources + unused public IPs/LBs.

## Step 5 — CI/CD
GitHub Actions (`azure/login@v2` OIDC `id-token: write` + `azure/arm-deploy@v2`) or Azure DevOps (`AzureCLI@2` → `az deployment group create`).

## Step 6 — Security Review (before prod)
- Identity: Entra ID + RBAC, Managed Identity for service-to-service — never creds in code.
- Secrets: Key Vault references in App Settings.
- Network: NSGs on subnets, Private Endpoints for PaaS, App Gateway + WAF.
- Encryption: TLS 1.2+, keys at rest.
- Monitoring: Defender for Cloud, Azure Policy guardrails for SOC2/HIPAA/ISO.

**Deploy fails?** `az deployment group show ... --query properties.error`; check Activity Log for RBAC/policy; validate first with `az bicep build` + `az deployment group validate`. Common: RBAC (need Contributor), unregistered provider (`az provider register`), global-name conflicts (storage/web apps), quota.

## Anti-Patterns
ARM JSON for new projects (use Bicep) · secrets in App Settings (use Key Vault refs) · single AKS node pool · public PaaS endpoints (Private Endpoints) · over-provisioning month one · shared resource groups for everything (one RG per env per workload) · no tagging (tag env/owner/cost-center/app) · classic resources.
