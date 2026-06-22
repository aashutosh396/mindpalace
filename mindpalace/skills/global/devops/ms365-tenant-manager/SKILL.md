---
name: Microsoft 365 Tenant Manager
description: Use when administering a Microsoft 365 / Azure AD tenant — generates PowerShell (Microsoft Graph) for tenant setup, bulk user provisioning, Conditional Access / MFA policies, security hardening, and offboarding.
tags: [microsoft-365, office-365, azure-ad, entra-id, powershell, conditional-access, mfa, exchange-online, tenant-admin]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/ms365-tenant-manager
---

# Microsoft 365 Tenant Manager

Automation for M365 Global Admins. Prefer the `Microsoft.Graph` module over legacy MSOnline. Test in a non-prod tenant first. Never hardcode credentials — use Key Vault or `Get-Credential`.

## Required modules
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

## Workflow 1 — New tenant setup
1. **Checklist + prereqs:** Global Admin secured with MFA; custom domain purchased; license SKUs confirmed (E3 vs E5).
2. **DNS:** add domain in admin center, verify MX/TXT(SPF) via `nslookup`/`Resolve-DnsName`. Wait for propagation (up to 48h) before bulk user creation.
3. **Security baseline:** block legacy auth (Conditional Access on `exchangeActiveSync`/`other` → block); enable unified audit log (`Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true`).
4. **Provision users** from CSV with `New-MgUser` + `Set-MgUserLicense`, wrapped in try/catch, forcing password change.
5. **Validate:** spot-check 3-5 accounts show "Active" license in portal.

## Workflow 2 — Security hardening
1. **Audit:** `Connect-MgGraph -Scopes "Directory.Read.All","Policy.Read.All","AuditLog.Read.All","Reports.Read.All"`. Export CA policy inventory; export users without MFA (`Get-MgReportAuthenticationMethodUserRegistrationDetail` where `-not IsMfaRegistered`).
2. **MFA policy — report-only first:** create CA policy with `State = "enabledForReportingButNotEnforced"`.
3. **Validate 48h** in Entra sign-in logs, then flip `State = "enabled"`.
4. **Secure Score:** `Get-MgSecuritySecureScore -Top 1`; work top improvement actions.

## Workflow 3 — User offboarding
1. **Block + revoke:** `Update-MgUser -AccountEnabled:$false`; `Invoke-MgInvalidateAllUserRefreshToken`.
2. **Preview** license removal (dry-run with `-WhatIf` mindset before executing).
3. **Execute:** remove licenses (`Set-MgUserLicense ... -RemoveLicenses`), convert mailbox to shared (`Set-Mailbox -Type Shared`), remove from all groups.
4. **Validate:** account "Blocked", no licenses, mailbox "Shared".

## CA policy template (MFA for admins)
```powershell
$adminRoles = (Get-MgDirectoryRole | Where-Object { $_.DisplayName -match "Admin" }).Id
New-MgIdentityConditionalAccessPolicy -BodyParameter @{
  DisplayName = "Require MFA for Admins"
  State = "enabledForReportingButNotEnforced"   # start report-only
  Conditions = @{ Users = @{ IncludeRoles = $adminRoles } }
  GrantControls = @{ Operator = "OR"; BuiltInControls = @("mfa") }
}
```

## Best practices
- Start every CA policy in report-only; review sign-in logs 48h before enforcing.
- For bulk user creation, validate every entry first (`is_valid` true) before generating the script.
- Use `-WhatIf` / dry-run before destructive bulk operations; include try/catch + `Write-Warning` logging for audit trails.
- Use separate admin accounts with PIM; apply least privilege.

## Constraints: Global Admin needed for full setup; Graph API throttles bulk ops; E3/E5 gate advanced features; hybrid AD needs extra config.
