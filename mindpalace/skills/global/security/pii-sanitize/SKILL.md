---
name: pii-sanitize
description: "Use when asked to redact/sanitize/scrub PII from a file or text before sharing, pasting, logging, or committing — detects credit cards, SSNs, emails, phone numbers, API keys, IP addresses, addresses, DOB, passport/license numbers and replaces each with a numbered placeholder."
version: 1.0.0
license: BSL-1.1
tags: [pii, sanitize, redact, security, privacy, secrets, gdpr, hipaa, scrub, anonymize]
source: https://github.com/openclaw/skills/tree/main/skills/agentward-ai/sanitize
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# pii-sanitize

Detect and redact personally identifiable information (PII) from text files. Each
detected value is replaced with a numbered placeholder like `[CREDIT_CARD_1]` or
`[SSN_2]`. All processing is local, zero network calls, Python stdlib only.

Real source repo: `agentward-ai/agentward`, skill dir `agentward-sanitize-skill/`
(the `openclaw/skills` tree URL is an author-namespaced mirror reference). Helper
script lives at `agentward-sanitize-skill/scripts/sanitize.py` in that repo —
fetch it from there rather than copying it here.

## When to use
- User wants to share, paste, log, screenshot, or commit a file that may contain
  PII or secrets and asks to clean/redact/sanitize/scrub/anonymize it first.
- Preparing patient notes, support tickets, logs, or reports for an LLM or a
  third party while stripping sensitive values.

## CRITICAL — PII safety rules (follow these)
- Do NOT read the raw input file directly — it may contain sensitive PII.
- ALWAYS pass `--output FILE` so sanitized text is written to disk.
- Only read the OUTPUT file; only show the user the redacted output.
- `--json` and `--preview` are safe — they never print raw PII to stdout.
- An entity map (raw PII → placeholder) is written to a sidecar
  `*.entity-map.json` only when `--output` is used. Do NOT read that file.

## How to run

Sanitize a file (recommended form):
```bash
python3 scripts/sanitize.py patient-notes.txt --output clean.txt
```

Preview detected categories/offsets without revealing raw values:
```bash
python3 scripts/sanitize.py notes.md --preview
```

JSON summary (no raw PII in stdout):
```bash
python3 scripts/sanitize.py report.txt --json --output clean.txt
```

Limit to specific categories:
```bash
python3 scripts/sanitize.py log.txt --categories ssn,credit_card,email --output clean.txt
```

## Supported categories (15)
Financial: `credit_card` (Luhn-validated), `cvv`, `expiry_date`, `bank_routing`.
Government IDs: `ssn`, `passport`, `drivers_license`.
Credentials: `api_key` (OpenAI/Anthropic `sk-`/`sk-proj-`/`sk-svcacct-`, GitHub
`ghp_`, Slack `xoxb-`/`xoxp-`, AWS `AKIA`).
Healthcare/Professional: `medical_license`, `insurance_id`.
Contact/Personal: `email`, `phone`, `ip_address`, `date_of_birth`, `address`.

## Gotchas / accuracy notes
- Many patterns are KEYWORD-ANCHORED to cut false positives: cvv, expiry,
  date_of_birth, passport, drivers_license, bank_routing, medical_license,
  insurance_id only match when preceded by a label like "CVV:", "DOB:",
  "Member ID:". Unlabeled values of these types may be missed.
- SSN excludes invalid area numbers (000, 666, 900-999), group 00, serial 0000.
- Credit cards must pass a Luhn checksum; phone needs 7+ digits; IP octets must
  be 0-255 — so some valid-but-odd values can slip through.
- Detection is regex/heuristic, not guaranteed exhaustive. Treat output as a
  strong first pass, not a compliance guarantee; still review before release.
- Requires Python 3.11+. No third-party packages.
