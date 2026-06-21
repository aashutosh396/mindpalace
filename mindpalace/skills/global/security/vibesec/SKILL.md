---
name: vibesec
description: "Use when writing, reviewing, or auditing web app code for security — secure coding, vulnerability scan, security audit, IDOR/access control, XSS, CSRF, SSRF, SQL injection, XXE, path traversal, open redirect, insecure file upload, JWT, mass assignment, GraphQL, security headers, secret exposure."
version: 1.0.0
license: Apache-2.0
tags: [security, secure-coding, web, vulnerabilities, owasp, xss, csrf, sqli, ssrf, jwt, audit]
source: https://github.com/BehiSecc/VibeSec-Skill
derived_from: awesomeclaude
---

# VibeSec — Secure Coding Guide for Web Apps

Approach code from a bug hunter's perspective and make web apps as secure as possible without breaking functionality.

## When to use
- Writing or modifying any web application code (backend or frontend).
- User asks for a security scan, audit, or vulnerability review.
- Reviewing auth, file uploads, redirects, DB queries, XML/JWT handling, or API endpoints.

## Core principles
- Defense in depth — never rely on a single control.
- Fail securely — fail closed (deny on error).
- Least privilege — minimum permissions necessary.
- Validate all input server-side; never trust client validation.
- Encode output for its rendering context (HTML/JS/URL/CSS).

## Access control (IDOR / privilege escalation)
- Verify resource ownership at the data layer on every request, not just the route.
- Check org membership for multi-tenant apps; re-validate after any privilege change.
- Use UUIDv4 (non-guessable) IDs, not sequential, unless user explicitly asks.
- Return 404 (not 403) for unauthorized resources to prevent enumeration.
- On user removal / account deletion: revoke all tokens, sessions, API keys.
- Watch: horizontal access (User A → User B same level), vertical access (user → admin), mass assignment.

## XSS
- Sanitize every user-controllable input (direct: forms, search, filenames; indirect: URL params/fragments, headers, third-party API data, postMessage, storage; overlooked: error messages, PDF/email generators, SVG uploads, markdown-with-HTML).
- Context-specific output encoding; prefer framework escaping (JSX, Vue `{{ }}`).
- Strong CSP: `default-src 'self'`, avoid `'unsafe-inline'`/`'unsafe-eval'`, use nonces/hashes, `frame-ancestors 'none'`.
- Use DOMPurify for HTML; whitelist tags/attrs for rich text. Add `X-Content-Type-Options: nosniff`.

## CSRF
- Protect ALL state-changing endpoints (POST/PUT/PATCH/DELETE, uploads, settings, payments) AND pre-auth actions (login, signup, password reset/change, verification, OAuth callback).
- Cryptographically random token tied to session, validated server-side; missing token = reject; regenerate on auth change.
- `SameSite=Strict; Secure; HttpOnly` cookies + tokens (defense in depth).
- JSON APIs are NOT immune — validate Origin/Referer AND use tokens. Never put tokens in URLs; prefer `X-CSRF-Token` header. Never change state on GET.

## Secret / sensitive data exposure
- Never in client code: API keys, DB strings, JWT secrets, encryption/OAuth secrets, internal URLs.
- Never expose: full card/SSN, passwords (even hashed), security answers, unmasked PII, internal IPs, schemas, stack traces, server versions.
- Secrets hide in: JS bundles + source maps, HTML comments, hidden fields, data attrs, local/session storage, SSR hydration state, `NEXT_PUBLIC_*`/`REACT_APP_*` build vars.
- Keep secrets in `.env`; make secret-requiring calls server-side only.

## Open redirect
- Allowlist hostnames, or accept relative paths only (start with `/`, no `//`), or indirect ref maps (`?redirect=dashboard`).
- Block bypasses: `@` symbol, subdomain abuse, `javascript:`/`data:`, double-encoding, backslash, null byte, tab/newline, protocol-relative `//evil.com`, fragment `#@evil.com`, IDN homographs (convert to Punycode first).

## SSRF
- Vulnerable: webhooks, URL previews, PDF/image fetch from URL, import-from-URL, feed readers, proxies.
- Prefer allowlist of approved domains; isolate URL-fetching services from internal network.
- HTTP/HTTPS scheme only; resolve DNS and reject private/internal IPs; block cloud metadata `169.254.169.254` (+ `metadata.google.internal`); limit/disable redirects (validate each hop); set timeout + response size cap.
- Block IP encodings: decimal `2130706433`, octal, hex, IPv6 `[::1]`/`[::ffff:127.0.0.1]`, short `127.1`. Prevent DNS rebinding: pin resolved IP for the request.

## Insecure file upload
- Validate extension (allowlist, single extension) AND magic bytes AND size — never just one. Match magic bytes to type (JPEG `FF D8 FF`, PNG `89 50 4E 47`, PDF `25 50 44 46`, ZIP/DOCX `50 4B 03 04`).
- Block: double extension `shell.jpg.php`, null byte, MIME spoof, polyglot files, SVG-with-JS (sanitize or disallow), XXE via DOCX/XLSX, ZIP slip, filename injection.
- Store: rename to random UUID, outside webroot / separate domain; serve `Content-Disposition: attachment` + `nosniff`; non-executable perms.

## SQL injection
- PRIMARY DEFENSE: parameterized queries / prepared statements. Never concatenate user input.
- ORM auto-parameterizes — be careful with raw query methods.
- Can't parameterize ORDER BY, table/column names, LIMIT — whitelist these. Escape LIKE wildcards `%` `_`.
- Least-privilege DB user; never expose SQL errors.

## XXE
- Disable DTD processing, external entity + DTD resolution, and XInclude.
- Vulnerable: SOAP/XML-RPC, XML uploads, RSS/Atom, plus DOCX/XLSX/SVG/SAML (XML under the hood).
- Per-parser: Python use `defusedxml` or `resolve_entities=False, no_network=True`; Java `disallow-doctype-decl=true`; PHP `libxml_disable_entity_loader(true)`; .NET `DtdProcessing.Prohibit`, `XmlResolver=null`. Prefer JSON where possible.

## Path traversal
- Never put user input directly in file paths; prefer indirect ref maps.
- Canonicalize (`os.path.realpath`) then assert `commonpath([base, target]) == base`.
- Reject `..`, absolute indicators (`/`, `C:`); whitelist filename chars; validate extension.

## JWT
- Whitelist allowed algorithm on verify (e.g. `algorithms: ['HS256']`); reject `alg: none`; never derive alg from token.
- 256+ bit random secret (not a passphrase); always set + validate `exp`; add `jti` for revocation.
- Store in httpOnly + Secure + SameSite=Strict cookies, NOT localStorage. Rotate refresh tokens (invalidate old on use).

## API
- Mass assignment: whitelist updatable fields (`pick(req.body, allowed)`); never `User.update(req.body)` — blocks `{role:"admin"}`.
- GraphQL: disable introspection in prod; enforce query depth limit (~10), cost/complexity limits, and per-request batch limits.

## Security headers (all responses)
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: [see XSS]
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Cache-Control: no-store   (sensitive pages)
```

## Password storage
- Argon2id, bcrypt, or scrypt. Never MD5/SHA1/plain SHA256. Min 8 chars (12+ recommended), no low max, allow all chars.

## Gotcha
When unsure, choose the more restrictive/secure option and leave a comment noting the security consideration.
