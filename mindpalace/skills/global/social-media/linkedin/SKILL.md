---
name: linkedin
description: Use when the user wants to automate LinkedIn — fetch profiles, search people/companies, send messages or InMail, manage connections, create/react/comment on posts, pull SSI/performance stats, or run Sales Navigator lookups via the Linked API cloud browser and linkedin-cli.
version: 1.0.0
license: MIT
tags: [linkedin, automation, social-media, lead-gen, sales-navigator, outreach, cli, vendor-locked]
source: https://github.com/Linked-API/linkedin-skills/blob/main/linkedin/SKILL.md
derived_from: awesomeclaude
platforms: [linkedapi.io]
prerequisites: [node, "@linkedapi/linkedin-cli"]
---

# LinkedIn Automation

`linkedin` is a CLI that drives LinkedIn through Linked API's real cloud browser. Use it to
fetch profiles, search people and companies, message, manage connections, post, react,
comment, and read stats. Operations are NOT instant — a real browser navigates LinkedIn, so
expect 30 seconds to several minutes per action.

Install if missing: `npm install -g @linkedapi/linkedin-cli`

## Authentication

Exit code 2 = auth error. Have the user sign up at [app.linkedapi.io](https://app.linkedapi.io),
connect their LinkedIn account, copy the **Linked API Token** and **Identification Token**, then:

```bash
linkedin setup --linked-api-token=TOKEN --identification-token=TOKEN
```

## Conventions

Run every command with `--json -q` for machine output, and prefix with
`LINKEDAPI_CLIENT=skill:linkedin` so usage is attributed:

```bash
LINKEDAPI_CLIENT=skill:linkedin linkedin <command> --json -q
```

Other flags: `--fields name,url,...` (select fields), `--account "Name"` (pick account),
`--no-color`.

Output is `{"success": true, "data": {...}}` or `{"success": false, "error": {"type":...}}`.
Exit 0 means the API call worked — ALWAYS check the `success` field (an action can still fail,
e.g. person not found). Non-zero exits: 1 general, 2 bad tokens, 3 plan required, 4 account
issue, 5 bad args, 6 rate limited, 7 network, 8 workflow timeout (returns workflowId).

## Core commands

```bash
# Person — add data flags only when needed (each adds time)
linkedin person fetch <url> [--experience --education --skills --languages \
  --posts --posts-limit N --comments --reactions] --json -q
linkedin person search --term "product manager" --locations "San Francisco" \
  [--position --industries --current-companies --previous-companies --schools --limit N] --json -q

# Company
linkedin company fetch <url> [--employees --dms --posts] [--employees-position ... \
  --employees-locations ... --dms-limit N --posts-limit N] --json -q
linkedin company search --term "fintech" --sizes "11-50,51-200" [--locations --industries --limit N] --json -q
# sizes: 1-10,11-50,51-200,201-500,501-1000,1001-5000,5001-10000,10001+

# Messaging (text ≤1900 chars; single-quote text args)
linkedin message send <person-url> 'Hey, loved your post!' --json -q
linkedin message get <person-url> [--since TIMESTAMP] --json -q   # first call syncs, slower

# Connections
linkedin connection status <url> --json -q
linkedin connection send <url> [--note 'text'] [--email user@example.com] --json -q
linkedin connection list [--limit N --since TS --position --locations --current-companies ...] --json -q
linkedin connection pending --json -q
linkedin connection withdraw <url> [--no-unfollow] --json -q   # default also unfollows
linkedin connection remove <url> --json -q

# Posts
linkedin post fetch <url> [--comments --comments-sort mostRecent|mostRelevant \
  --comments-replies --comments-limit N --reactions --reactions-limit N] --json -q
linkedin post create '<text>' [--company-url <url>] \
  [--attachments "url:type[:name]"] --json -q
# attachments: image|video|document; ≤9 images OR 1 video OR 1 document, no mixing
linkedin post react <url> --type like|love|support|celebrate|insightful|funny [--company-url <url>] --json -q
linkedin post comment <url> 'Great insights!' [--company-url <url>] --json -q   # ≤1000 chars

# Stats
linkedin stats ssi --json -q            # Social Selling Index
linkedin stats performance --json -q    # views, impressions, search appearances
linkedin stats usage --start TS --end TS --json -q
```

## Sales Navigator (requires Sales Nav subscription; uses hashed URLs)

```bash
linkedin navigator person fetch <hashed-url> --json -q
linkedin navigator person search --term "VP Marketing" --locations "United States" \
  [--years-of-experience lessThanOne|oneToTwo|threeToFive|sixToTen|moreThanTen ...] --json -q
linkedin navigator company fetch <hashed-url> [--employees --dms \
  --employees-positions ... --dms-limit N] --json -q
linkedin navigator company search --term "fintech" [--sizes --locations --industries \
  --revenue-min N --revenue-max N] --json -q   # revenue in M USD
linkedin navigator message send <person-url> '<text>' --subject '<subject>' --json -q  # InMail, subject ≤80
linkedin navigator message get <person-url> [--since TS] --json -q
```

## Custom workflows & accounts

```bash
linkedin workflow run --file workflow.json --json -q   # or pipe via stdin / inline echo
linkedin workflow status <id> [--wait] --json -q
# Workflow JSON schema: https://linkedapi.io/docs/building-workflows/

linkedin account list           # * marks active
linkedin account switch "Name"
linkedin account rename "Name" --name "New Name"
linkedin reset [--all]
```

## Behavior to respect

- **Sequential per account** — all ops for one account queue and run one at a time.
- **Slow** — real browser; 30s to minutes per op. Set expectations.
- **UTC** timestamps everywhere.
- **Single-quote** message/post/comment text to avoid shell mangling.
- **Action limits** are configurable per account on the platform; `limitExceeded` = cap hit.
- URLs in responses are normalized to `https://www.linkedin.com/...` without trailing slash.
- Missing fields come back `null` or `[]`, never omitted.
