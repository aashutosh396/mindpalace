---
name: Cloudflare Troubleshooting (API-driven)
description: Use when diagnosing Cloudflare issues — ERR_TOO_MANY_REDIRECTS, SSL/TLS errors, DNS, origin 5xx — by querying the Cloudflare API for actual config before concluding, then applying targeted fixes and purging cache.
tags: [cloudflare, redirect-loop, ssl-tls, dns, origin-errors, cloudflare-api, evidence-driven, purge-cache]
source: daymade/claude-code-skills
derived_from: cloudflare-troubleshooting
---

# Cloudflare Troubleshooting

**Investigate with evidence, not assumptions.** Always query the Cloudflare API for actual config before diagnosing. (Domain layer on top of evidence-driven network diagnosis: falsification, layered isolation.)

## Setup
Get domain, account email, Global API Key (or scoped Token — recommend tokens). Get zone ID:
```bash
curl -s "https://api.cloudflare.com/client/v4/zones?name=<domain>" \
  -H "X-Auth-Email: <email>" -H "X-Auth-Key: <key>" | jq '.result[0].id'
```

## Redirect loops (ERR_TOO_MANY_REDIRECTS)
Evidence: GET `/settings/ssl` (`.result.value`), `/settings/always_use_https`, `/pagerules` (look for `forwarding_url`/`always_use_https`), test origin `curl -I -H "Host: <domain>" https://<origin_ip>`.
Diagnosis: **SSL mode "flexible" + origin enforces HTTPS = loop** (common with GitHub Pages/Netlify/Vercel). Multiple redirect rules conflict.
Fix: `PATCH /settings/ssl --data '{"value":"full"}'` then purge cache.

## DNS issues
List `/dns_records`; check `dig <domain>` / `dig @8.8.8.8 <domain>`; `/dnssec`. Look for missing A/AAAA/CNAME, wrong proxy status (proxied vs DNS-only), conflicting records, TTL.

## SSL cert errors
`/ssl/certificate_packs`; origin cert `openssl s_client -connect <ip>:443 -servername <domain>`; min TLS version. Error 526 = strict mode + invalid origin cert; 525 = origin handshake fail; Universal SSL provisioning = wait 15-30min.

## Origin 502/503/504
Origin reachable (`curl -I -H "Host:..." https://<ip>`); DNS points right; load balancer config; `/firewall/rules`.

## Fix discipline
GET to understand state → PATCH/POST to fix one thing → purge cache (`POST /purge_cache -d '{"purge_everything":true}'`) for SSL/redirect changes → re-query + external (dig/curl) to verify. Inform wait times: edge 30-60s, DNS up to 48h, browser cache manual.

## Security
Never log API keys. Prefer scoped API Tokens over Global Key. Use read-only ops for investigation. Prefer direct curl/Bash over scripts for transparency; `scripts/check_cloudflare_config.py` and `scripts/fix_ssl_mode.py` are reference implementations only.
