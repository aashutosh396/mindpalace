---
name: AWS Solution Architect
description: Use when designing serverless/AWS architecture, writing CloudFormation/CDK/Terraform, optimizing AWS costs, or migrating to AWS — pattern recommendations, IaC, cost analysis, deployment with failure handling.
tags: [aws, serverless, cloudformation, cdk, lambda, dynamodb, ecs, aurora, cost-optimization, iac]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/aws-solution-architect
---

# AWS Solution Architect

Scalable, cost-effective AWS architectures with IaC. Six-step workflow.

## Step 1 — Requirements
App type, users + RPS, monthly budget, team size + AWS maturity, compliance (GDPR/HIPAA/SOC2), availability SLA + RPO/RTO.

## Step 2 — Pick a Pattern
- **Serverless Web**: S3 + CloudFront + API Gateway + Lambda + DynamoDB + Cognito. Low ops, pay-per-use, autoscale; cons: cold starts, 15-min Lambda limit, eventual consistency.
- **Event-Driven Microservices**: EventBridge + Lambda + SQS + Step Functions.
- **Three-Tier**: ALB + ECS Fargate + Aurora + ElastiCache.
- **GraphQL Backend**: AppSync + Lambda + DynamoDB + Cognito.

Validation checkpoint: pattern must match team maturity + compliance before IaC.

## Step 3 — Generate IaC
Serverless via SAM/CloudFormation: `AWS::Serverless::Function` (handler, runtime, memory, timeout, env, DynamoDBCrudPolicy, Api event `/{proxy+}`) + `AWS::DynamoDB::Table` (PAY_PER_REQUEST, pk/sk). Three-tier via CDK: VPC (maxAzs 2) → ECS Cluster → Aurora ServerlessCluster (Postgres, minCapacity 0.5/max 4). Full templates add API Gateway, Cognito, least-privilege IAM, CloudWatch.

## Step 4 — Review Costs
Monthly breakdown by service + right-sizing (e.g. RDS down) + Compute Savings Plans + S3 lifecycle (Glacier for >90 days) + kill idle resources + NAT Gateway alternatives.

## Step 5 — Deploy
`aws cloudformation create-stack --capabilities CAPABILITY_IAM` / `cdk deploy` / `terraform apply`.

## Step 6 — Validate & Handle Failures
Check stack status, set CloudWatch alarms. **Fails?** `describe-stack-events --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'`; check Lambda/ECS logs; fix; delete failed stack (`delete-stack` + `wait stack-delete-complete`) before redeploy. Common: IAM (need CAPABILITY_IAM + trust policies), resource-limit (Service Quotas), invalid syntax (`validate-template` first).

## Output Formats
Architecture: pattern + rationale, ASCII service-stack diagram, monthly cost + trade-offs. IaC: CloudFormation YAML (SAM/CFN), CDK TypeScript, Terraform HCL. Cost: spend breakdown + priority action list (high/med/low).

## Quick Starts
MVP <$100/mo: Lambda + API GW + DynamoDB + Cognito + S3/CloudFront. Scaling $500-2K/mo: ECS Fargate + Aurora Serverless + ElastiCache + CloudFront + CodePipeline + multi-AZ.
