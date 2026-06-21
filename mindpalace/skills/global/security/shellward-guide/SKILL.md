---
name: shellward-guide
description: "Use when securing or hardening an OpenClaw / ShellWard installation — auditing exposed gateway ports, container isolation, plaintext secrets, audit logs, plugin risks, or patch/version status; triggers on shellward, openclaw security, harden, security checklist, /security, /audit, /harden, /scan-plugins, /check-updates."
version: 1.0.0
license: MIT
tags: [security, hardening, openclaw, shellward, audit, secrets, docker, firewall, plugins, vulnerabilities]
source: https://github.com/jnMetaCode/shellward/tree/main/skills/security-guide
derived_from: awesomeclaude
prerequisites:
  commands: [docker, ufw, chmod]
---

# ShellWard Security Deployment Guide

Produces a complete security-hardening checklist for an OpenClaw installation guarded by ShellWard. Inspect the current system state with available tools, then give actionable, command-level recommendations. Prioritize critical issues first; ask for confirmation before any destructive operation.

## When to use
- User asks to secure / harden / audit an OpenClaw or ShellWard install.
- Reviewing exposed gateway ports, container isolation, leaked secrets, audit logging, plugin risk, or version/patch status.
- User runs ShellWard quick commands: `/security`, `/audit`, `/harden`, `/scan-plugins`, `/check-updates`.

## Security checklist

### 1. Network control
- Check whether OpenClaw gateway ports (19000 / 19001) are exposed to the public network.
- Bind to `127.0.0.1` or front with an authenticated reverse proxy.
- Firewall: `ufw allow from 127.0.0.1 to any port 19000`
- Cloud servers: review security-group / inbound rules.

### 2. Container isolation
Run OpenClaw in Docker with dropped capabilities and a read-only rootfs:
```
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE \
  --read-only --tmpfs /tmp \
  -u 1000:1000 \
  --memory=2g --cpus=1 \
  openclaw
```
Mount only the directories actually required.

### 3. Credential management
- Scan for plaintext secrets in `.env`, `.bashrc`, and environment variables.
- Move secrets to a manager (Vault, Doppler, etc.).
- Sensitive files must be mode `0600`: `chmod 600 ~/.env ~/.ssh/* ~/.aws/credentials`

### 4. Audit logging
- Confirm the ShellWard audit log is active at `~/.openclaw/shellward/audit.jsonl`.
- Show recent security events.
- Set up log rotation + backup; forward critical events to an external SIEM.

### 5. Plugin security
- List installed plugins; flag known-risky ones.
- Disable plugin auto-update; install only from trusted sources.
- Scan plugin code for suspicious patterns.

### 6. Patch management
- Check the current OpenClaw version and report known vulnerabilities for it.
- Recommend an upgrade path.
- Verify Node.js `>= 22.12`.

## ShellWard quick commands
- `/security` — full security status overview
- `/audit [count] [filter]` — view audit log
- `/harden` — scan for issues; `/harden fix` to auto-fix
- `/scan-plugins` — scan plugins for security risks
- `/check-updates` — check versions and vulnerabilities

## Response style
- Concise and actionable; critical issues first.
- For each issue, give the exact fix command.
- Detect and match the user's language (original skill is bilingual EN / 中文).
- Confirm before executing destructive operations.

## Gotchas
- This skill targets the OpenClaw runtime specifically — ports, log paths, and `/`-commands assume a ShellWard-instrumented OpenClaw host. Adapt paths for other stacks.
