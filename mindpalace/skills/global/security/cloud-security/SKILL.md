---
name: Cloud Security Posture (CSPM)
description: Use when assessing cloud infra for misconfigurations — IAM privilege escalation, S3 public exposure, open security groups, or IaC security gaps across AWS/Azure/GCP with MITRE ATT&CK mapping.
tags: [cloud-security, cspm, iam, privilege-escalation, s3-exposure, security-groups, iac-scanning, aws, least-privilege, mitre-attack]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/cloud-security
---

# Cloud Security Posture (CSPM)

Systematically check cloud configs for exploitable misconfigurations: IAM priv-esc, storage exposure, network over-permissioning, IaC. (Preventive — assess before exploitation.) Exit codes: 0 clean, 1 high (24h), 2 critical (immediate).

## IAM Privilege Escalation Patterns (→ MITRE)
Critical two-action combos: `iam:PassRole + lambda:CreateFunction` (T1078.004) · `iam:PassRole + ec2:RunInstances` · `iam:PassRole + cloudformation:CreateStack` · `iam:AttachUserPolicy + sts:GetCallerIdentity` (T1484.001) · `iam:PutUserPolicy + ...` · `iam:CreatePolicyVersion + iam:ListPolicies`. High: `iam:CreateAccessKey + iam:ListUsers` (T1098.001), group membership, password reset, service wildcards (`iam:*`, `s3:*`).
**Analyze the full statement, not individual actions** — PassRole alone isn't critical, the combo is.
Severity: Action=* Resource=* → Critical · Principal:* → Critical · two-action escalation → Critical · priv-esc on wildcard resource → High · data exfil actions (s3:GetObject, secretsmanager:GetSecretValue on *) → High.

## S3 Exposure
public-read-write ACL → Critical · public-read/authenticated-read → High · `Principal:*` Allow → Critical · no encryption → High · any public-access-block flag false → High. **Baseline**: all 4 public-access-block flags true (BlockPublicAcls/BlockPublicPolicy/IgnorePublicAcls/RestrictPublicBuckets) at BOTH account and bucket level, KMS encryption, ACL private. Bucket-level can override account-level — set both.

## Security Group Analysis
Critical (to 0.0.0.0/0): SSH 22 (restrict to VPN/SSM), RDP 3389, all ports 0-65535. High (DB ports to internet): MSSQL 1433, MySQL 3306, Postgres 5432, MongoDB 27017, Redis 6379, ES 9200 — allow from app-tier SG only, move to private subnet.

## Severity Modifiers
`internet-facing` (LB/API gateway/public EC2) and `regulated-data` (PCI/HIPAA/GDPR) each bump every finding one level. Always apply for DMZ + regulated workloads.

## IaC Review (at definition time)
Terraform (aws_iam_policy_document, aws_s3_bucket_acl, aws_security_group) · CloudFormation properties · K8s/Helm (container privileges, network policies, secrets). Bad: `Action="*" Resource="*"`; good: named actions + specific ARN. Run pre-plan/pre-apply/PR gate.

## Provider Coverage
AWS full; Azure/GCP partial (RBAC/IAM bindings, Blob SAS/GCS IAM, NSG/firewall rules, ARM/Bicep/Deployment Manager).

## Anti-Patterns
IAM analysis without checking escalation combos · only bucket-level public-access-block (need account too) · skipping internet-facing modifier · checking only admin policies (priv-esc hides in innocuous combos) · remediating without root cause (gets re-added) · ignoring service-account over-permissioning · skipping regulated-data modifier.
