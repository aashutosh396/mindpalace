---
name: Repomix Safe Mixer (credential-scan before packing)
description: Use when packaging a codebase with repomix for distribution or creating a shareable reference package — scans for hardcoded credentials first, blocks packing if secrets found, packs only when clean.
tags: [repomix, secrets, credentials, security, scan, packaging, api-keys, distribution, env-vars]
source: daymade/claude-code-skills
derived_from: repomix-safe-mixer
---

Safely package code with repomix by detecting and removing hardcoded credentials before packing. Prevents accidental credential exposure when sharing code.

## Core workflow (scan → report → pack)
```bash
python3 scripts/safe_pack.py <directory>
```
Scans for hardcoded secrets → reports file/line details → **blocks packaging if secrets found** → packs with repomix only if clean.

Options: `--output package.xml`, `--config repomix.config.json`, `--exclude '.*test.*' '.*\.example'`, `--force` (⚠️ skips scan, not recommended).

## Standalone scanning (no pack)
```bash
python3 scripts/scan_secrets.py <directory>          # human output
python3 scripts/scan_secrets.py <directory> --json   # exit 1 if secrets (good for pre-commit hook)
```

## Detected secret types
Cloud (AWS `AKIA...`, Cloudflare R2, Supabase URLs/keys), API keys (Stripe `sk_live_`, OpenAI `sk-`, Gemini `AIza...`, generic), auth (JWT `eyJ...`, OAuth client secrets, private keys `-----BEGIN PRIVATE KEY-----`, Turnstile `0x...`).

## Skipped false positives
Placeholders (`your-api-key`, `<YOUR_API_KEY>`, `${API_KEY}`, `TODO: add key`), test/example/sample files, comment lines, env-var references (`process.env.X`, `import.meta.env.VITE_X`, `Deno.env.get(...)`). Add more via `--exclude`.

## Handling detected secrets
1. Review each finding — confirm it's a real credential, not a placeholder.
2. Replace with env vars: `const URL = import.meta.env.VITE_SUPABASE_URL` (+ validation logging if missing).
3. Create `.env.example` with placeholders + "copy to .env, never commit" instructions.
4. Re-scan to confirm removal.
5. Safe pack.

## Post-exposure actions (if already leaked)
Rotate credentials immediately → revoke old → audit logs for unauthorized access → set monitoring/alerts → redeploy with new creds → document the incident.

## Security note
Detects common patterns, not all credential types. Not a replacement for CI/CD secret scanning, git-history scanning, or full security audits. Always review findings manually and rotate exposed credentials.
