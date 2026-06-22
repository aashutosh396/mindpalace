---
name: Atlassian Administrator
description: Use when adding/removing users in Jira, changing Confluence permissions, configuring SSO/SCIM, managing groups or marketplace apps, or handling org-wide Atlassian governance — admin workflows via admin.atlassian.com + REST API (admin ops are not available via the Atlassian MCP).
tags: [atlassian, jira, confluence, admin, sso, scim, permissions, provisioning, governance, audit-log]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/atlassian-admin
---

# Atlassian Administrator

Org-wide administration of Jira, Confluence, Bitbucket, Trello: users, groups, permissions, SSO, apps, governance. Admin operations run through `admin.atlassian.com` or REST APIs — **not** the Atlassian Remote MCP (which has no admin tools). MCP can only assist read-side: resolve accountIds, find a leaver's open issues, inventory projects/spaces.

## Core workflows
**User provisioning** — invite (`POST /rest/api/3/user`) → add to groups → assign product access → set default permissions → notify team leads → verify active at `admin.atlassian.com/o/{orgId}/users`.

**User deprovisioning** — *first* audit owned content/tickets (`GET /rest/api/3/search?jql=assignee={accountId}`; Confluence owned spaces) → reassign project leads, space ownership, open issues (bulk change), filters/dashboards → remove from groups → revoke access → deactivate (`DELETE /rest/api/3/user?accountId=…`) → verify `"active": false` → document in audit log.

**Group management** — create (`POST /rest/api/3/group`); structure by team / role / project; assign default permissions; verify members (`GET /rest/api/3/group/member`); quarterly review.

**Permission schemes** — Jira: Public / Team / Restricted / Admin. Confluence: Public / Team / Personal / Restricted. Always use groups not individuals; least privilege; audit regularly; document rationale.

**SSO** — choose IdP (Okta/Azure AD/Google) → configure SAML (Entity ID, ACS URL, X.509 cert) → test with admin (keep password login active) → test regular user → enable → enforce → configure SCIM auto-provisioning → verify `saml.login.success` in audit log.

**Marketplace apps** — review vendor security (SOC 2, pentest) → sandbox test → purchase/trial → install → configure → train → verify health → review annually.

## Global config & security
Jira: issue types/schemes, global workflows, custom fields, notification schemes. Confluence: global templates/blueprints, themes/branding, macro permissions. Security: password policies, session duration, API token controls, data residency pinning, audit logs (retain ≥7 years for SOC 2/GDPR via `GET /admin/v1/orgs/{orgId}/audit-log`).

## Governance
Quarterly access reviews (export users, remove inactive); limit org admins to 2-3 and audit monthly; require MFA for admins. Naming: Jira project keys 3-4 uppercase, custom fields prefixed; Confluence spaces team/project-prefixed, labels lowercase-hyphenated. Change management: major changes announced 2 weeks ahead with sandbox test + rollback plan; minor changes 48h + change log.

## DR & incident response
Daily backups, weekly verification, 30-day retention, offsite; quarterly recovery drills (measure RTO/RPO). Incident severities: P1 down (15 min) · P2 major (1h) · P3 minor (4h) · P4 enhancement (24h). Steps: acknowledge → assess → communicate → investigate (check product Health + Atlassian Status) → fix → verify → post-mortem.

## Escalation
To Atlassian Support: outages, org-wide degradation, data loss, billing, complex migrations. Involve Security Team for incidents, unusual access, audit prep, new integration review.
