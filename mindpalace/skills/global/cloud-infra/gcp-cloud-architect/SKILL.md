---
name: GCP Cloud Architect
description: Use when designing Google Cloud infrastructure, deploying to Cloud Run/GKE, building BigQuery pipelines, or optimizing GCP cost — runs a 6-step requirements→pattern→cost→IaC→CI/CD→security workflow with Terraform/gcloud templates.
tags: [gcp, google-cloud, cloud-run, gke, bigquery, terraform, cloud-build, cost-optimization, iac, firestore]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/gcp-cloud-architect
---

# GCP Cloud Architect

Design scalable, cost-effective Google Cloud architectures with IaC.

## 6-step workflow

### 1. Gather requirements
App type · expected users + RPS · monthly budget · team size/GCP experience · compliance (GDPR/HIPAA/SOC2) · availability (SLA, RPO/RTO).

### 2. Choose a pattern
- **Serverless Web** ($15-40/mo): Cloud Storage + Cloud CDN + Cloud Run + Firestore + Identity Platform.
- **Microservices on GKE** ($500-2000/mo): GKE Autopilot + Cloud SQL (read replicas) + Memorystore + Pub/Sub.
- **Serverless Data Pipeline:** Pub/Sub + Dataflow + BigQuery + Looker.
- **ML Platform:** Vertex AI + Cloud Storage + BigQuery + Cloud Functions.

**Checkpoint:** confirm pattern matches team's ops maturity + compliance before proceeding.

### 3. Estimate cost
Break down by service; surface right-sizing, committed-use discounts (1yr/3yr), sustained-use discounts (auto 20-30%), storage class transitions (Nearline for >90d objects), egress optimization.

### 4. Generate IaC
Terraform (Google provider ~> 5.0) or gcloud CLI. Cloud Run service with min/max instances; Firestore native DB. Example deploy:
```bash
gcloud run deploy my-app-api --image gcr.io/$PROJECT_ID/my-app:latest \
  --region us-central1 --platform managed --memory 512Mi --cpu 1 \
  --min-instances 0 --max-instances 10
```

### 5. CI/CD
Cloud Build (`cloudbuild.yaml`: docker build → push → `gcloud run deploy`) or GitHub Actions. Create trigger on `^main$`.

### 6. Security review
Checklist: IAM least-privilege (predefined > basic roles) · Workload Identity for GKE (not key files) · VPC Service Controls on sensitive APIs · Cloud KMS CMEK · Audit Logs on all admin activity · org policies block public access · Secret Manager for all credentials.

**On deploy failure:** `gcloud run services describe`; read Cloud Logging (`resource.type=cloud_run_revision`). Common causes: IAM perms, quota, container startup, region/API not enabled (`gcloud services enable`).

## Anti-patterns
| Anti-pattern | Better |
|---|---|
| Default VPC in prod | Custom VPC + private subnets |
| Over-provisioned GKE node pools | Autopilot or cluster autoscaler |
| Secrets in env vars | Secret Manager + Workload Identity |
| Single-region SaaS | Multi-region + Cloud Load Balancing |
| BigQuery on-demand at scale | Flat-rate slots |
| Cloud Functions for >60s tasks | Cloud Run (9-min CF timeout) |
