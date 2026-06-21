---
name: cloud-architect
description: "Use when designing cloud architectures, planning migrations, optimizing cost, or producing disaster-recovery strategies across AWS, Azure, or GCP. Covers Well-Architected Framework, landing zones, zero-trust security, FinOps, and RTO/RPO. Triggers: AWS, Azure, GCP, cloud migration, cloud architecture, multi-cloud, cloud cost, Well-Architected, landing zone, disaster recovery, serverless architecture."
version: 1.0.0
license: MIT
tags: [cloud, aws, azure, gcp, migration, cost-optimization, disaster-recovery, well-architected]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/cloud-architect
derived_from: awesomeclaude
---

# Cloud Architect

Design cloud architectures, migrations, cost models, and DR strategies across AWS/Azure/GCP.

## When to use

New cloud architecture, migration planning, multi-cloud, cost optimization, DR, security architecture, serverless design.

## Core workflow

1. **Discovery** — current state, requirements, constraints, compliance.
2. **Design** — services, topology, data architecture. Checkpoint: every component has a redundancy strategy; no single points of failure.
3. **Security** — zero-trust, identity federation, encryption.
4. **Cost model** — right-size, reserved capacity, auto-scaling.
5. **Migration** — 6Rs framework, waves; validate connectivity before cutover.
6. **Operate** — monitoring, automation, continuous optimization. After DR test: confirm RTO/RPO met.

```bash
# Validate connectivity before cutover
aws ec2 describe-vpc-peering-connections --filters "Name=status-code,Values=active"
# Verify health after migration
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:...
```

## Constraints

MUST: design for HA (99.9%+); security by design (zero-trust); IaC (Terraform/CloudFormation); cost allocation tags + monitoring; DR with defined RTO/RPO; multi-region for critical workloads; managed services when possible; document decisions.
MUST NOT: credentials in code/public repos; skip encryption (at rest + in transit); single points of failure; ignore cost optimization; deploy without monitoring; over-complex architectures; ignore compliance; skip DR testing.

## Patterns

```hcl
# Least-privilege IAM (zero-trust) — scope to specific resource+actions
resource "aws_iam_role_policy" "app_policy" {
  role = aws_iam_role.app_role.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [{
    Effect = "Allow", Action = ["s3:GetObject","s3:PutObject"],
    Resource = "${aws_s3_bucket.app.arn}/*" }] })
}
# Auto-scaling target tracking
resource "aws_autoscaling_policy" "cpu_target" {
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification { predefined_metric_type = "ASGAverageCPUUtilization" }
    target_value = 60.0 } }
```
```bash
# Cost: top drivers, last 30 days
aws ce get-cost-and-usage --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY --metrics "UnblendedCost" --group-by Type=DIMENSION,Key=SERVICE --output table
```

## Output

Architecture diagram with services/data flow; service selection rationale; security architecture (IAM, segmentation, encryption); cost estimate + optimization; deployment approach + rollback plan.
