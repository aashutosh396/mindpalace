---
name: Terraform Operational Traps
description: Use when writing Terraform provisioners (null_resource/remote-exec/local-exec/file), setting up fresh instances with cloud-init, building multi-environment IaC, or debugging containers Restarting/unhealthy after terraform apply — exact-error → root-cause → copy-paste fix.
tags: [terraform, iac, provisioner, cloud-init, docker, multi-environment, cloudflare, caddy, tls, deployment]
source: daymade/claude-code-skills
derived_from: terraform-skill
---

Failure patterns from real deployments. Each item caused an incident. Format: **exact error → root cause → fix**.

## Provisioner traps
- **`docker: not found` in remote-exec** — cloud-init still installing. Gate: `"cloud-init status --wait || true"`, `"which docker || { echo FATAL; exit 1; }"`.
- **`rsync: connection unexpectedly closed` in local-exec** — Terraform holds the SSH connection; a second rsync gets rejected. Never use local-exec for remote file transfer. Use tarball + `file` provisioner + remote-exec untar. (macOS BSD tar: `--exclude` BEFORE the source arg.)
- **`cloud-init status` "running" forever** — `apt-get -y` doesn't suppress debconf TTY prompts. Use `DEBIAN_FRONTEND=noninteractive` + `debconf-set-selections`. Offenders: iptables-persistent, postfix, mysql-server, wireshark-common.
- **`EACCES` in container, Restarting** — host volume dirs root-owned, container runs uid 1001. `mkdir -p` + `chown -R 1001:1001` before `docker compose up`. (Find UID via `USER`/`adduser -u` in Dockerfile.)
- **Provisioner fails, no diagnostic output** — `set -e` exits on first error, hiding `docker logs`. Use `set -u` (not `-e`), one verification gate at the end (`docker ps --filter ... | grep -q healthy || exit 1`).
- **Container Restarting, tables missing** — migrations not in provisioner; PG `docker-entrypoint-initdb.d` only runs on empty data dir. Explicitly `CREATE DATABASE` + run idempotent migrations tracked in `schema_migrations`.
- **`docker compose build` ignores env override** — compose reads build args from `.env`, not shell env. Append to `.env`, don't `VAR=x docker compose build`.

## TLS / Cloudflare / OAuth
- **`Invalid format for Authorization header`** — Caddy DNS-01 ACME needs a Cloudflare **API Token** (`cfut_` prefix, Bearer), not a Global API Key (37 hex, X-Auth-Key → HTTP 400 Code:6003). Prod may work via cached certs; fresh envs fail on first cert. Verify: `echo "$TOKEN" | grep -q "^cfut_"`.
- **TLS works on prod, fails on staging** — hardcoded domains in Caddyfile/compose. Staging Caddy tries to get certs for domains it doesn't own. Caddyfile: use `{$VAR}` (Caddy evals env at startup). Compose: `${VAR:?required}` (fail-fast). Pass the env var into the gateway container.
- **`Social sign in failed`** — Casdoor `init_data.json` has hardcoded redirect URIs; `--createDatabase=true` only applies init_data on first-ever DB creation, not restarts. Fix via SQL `UPDATE application SET redirect_uris = REPLACE(...)`. Also `AUTH_CASDOOR_ISSUER` must match the auth subdomain, not the app root.

## Multi-environment isolation
Before a second env, grep `.tf` for hardcoded names. Globally-unique resources fail on apply (SSH key pair, SLS log project, CloudMonitor contact) — namespace with `"${env}-..."`. **DNS duplication trap:** two envs creating A records for the same name in one zone → two record IDs → round-robin → ~50% traffic to the wrong instance. Use subdomain isolation or separate zones; create records for ALL Caddy-served subdomains. **Snapshot cross-contamination:** unfiltered snapshot data source returns ALL account snapshots; new env inherits an old large one. Gate with a variable (don't add `count` to the data source — it changes the state address and causes drift).

## Pre-deploy validation (before apply)
`terraform validate`; no hardcoded domains in Caddyfiles/compose; required env vars present; CF token format (not Global Key); DNS records for all Caddy domains; Casdoor issuer matches `auth.*`; SSH key exists. Run as `make pre-deploy ENV=staging` before `make apply`.

## Zero-to-deployment (fresh disks expose implicit deps)
`mkdir -p` data dirs in cloud-init (file provisioner fails if target missing); explicit `CREATE DATABASE`; idempotent migrations; `depends_on` between resources sharing Docker networks; stop non-critical containers during build on ≤8GB instances; every domain `{$VAR}`/`${VAR:?required}`; Caddy needs API Token (`cfut_`).
