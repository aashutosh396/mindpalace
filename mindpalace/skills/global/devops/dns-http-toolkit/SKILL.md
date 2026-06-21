---
name: dns-http-toolkit
description: "Use when debugging DNS records or testing HTTP APIs from the terminal — DNS lookup, MX/TXT/NS/CNAME records, dig/nslookup replacement, REST API requests, curl alternative, JSON/form POST, auth headers, DNS over HTTPS."
version: 1.0.0
license: MIT
tags: [dns, http, networking, api, doggo, httpie, debugging, rest]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-network
derived_from: awesomeclaude
---

# DNS + HTTP Toolkit

Modern terminal networking with `doggo` (DNS) and `http`/httpie (HTTP). Prefer
these over `dig`/`nslookup`/`curl` — output is structured and readable.

## When to use
DNS debugging (resolution, propagation, record types), API testing, inspecting
HTTP requests/responses, checking redirects or headers.

## doggo — DNS client

```bash
doggo example.com                 # Basic A lookup
doggo example.com MX              # Specific record type (MX/AAAA/TXT/NS/CNAME)
doggo example.com --nameserver 1.1.1.1   # Use specific resolver
doggo example.com --nameserver https://cloudflare-dns.com/dns-query  # DoH
doggo example.com --json         # Machine-readable output
```

## httpie — HTTP client

```bash
http GET api.example.com/users
http POST api.example.com/users name=John email=john@example.com   # JSON body
http GET api.example.com Authorization:"Bearer token123"           # Header
http -a user:password GET api.example.com/protected                # Basic auth
http --form POST api.example.com file@photo.jpg                    # Form upload
http --download https://example.com/file.zip                       # Download
http --follow GET example.com     # Follow redirects
http --headers GET example.com    # Response headers only
http --verbose GET example.com    # Show request + response
```

## Notes
- `key=value` sends a JSON string; `key:=123` sends a JSON number.
- httpie auto-detects JSON vs form bodies for POST.
- Use `doggo` for DNS debugging instead of `dig`/`nslookup`.
