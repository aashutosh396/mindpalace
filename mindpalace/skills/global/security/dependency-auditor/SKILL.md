---
name: Dependency Auditor
description: Use when auditing third-party packages before release, investigating a CVE, planning a major version bump, or running a license-compliance review across multi-language projects.
tags: [dependencies, security, cve, vulnerability, license, gpl, upgrade, supply-chain, audit, semver]
source: alirezarezvani/claude-skills
derived_from: dependency-auditor
---

# Dependency Auditor

Offline, deterministic dependency auditing across 8+ ecosystems. Pattern-matchers over manifests/lockfiles — they do NOT call live advisory APIs, so always pair with `npm audit` / `pip-audit` / `cargo audit` for current CVE coverage.

## Flow: scan → license check → upgrade plan
1. **Scan** for vulnerabilities (built-in offline CVE pattern set; fail on high severity). Findings drive which packages to pin/patch now.
2. **License check** for compliance + conflicts (strict policy for permissive projects). Conflicts go to the user as a legal-risk list.
3. **Upgrade plan** from the scanner inventory, ordered by risk with rollback notes. `--security-only` limits to fixes.
4. **Verification loop**: after applying upgrades, re-run the scan and assert 0 high-severity findings before closing.

## Supported ecosystems
JS/Node (package.json, lockfiles), Python (requirements.txt, pyproject.toml, Pipfile.lock, poetry.lock), Go (go.mod/go.sum), Rust (Cargo.toml/.lock), Ruby (Gemfile/.lock), Java (pom.xml, gradle.lockfile), PHP (composer.json/.lock), C#/.NET (packages.config, project.assets.json).

## License classification
- **Permissive**: MIT, Apache 2.0, BSD, ISC
- **Copyleft strong**: GPL v2/v3, AGPL v3 — flags contamination risk in permissive projects
- **Copyleft weak**: LGPL, MPL 2.0
- **Proprietary / Dual / Unknown** — unknown licenses surfaced for manual review

Analyze license inheritance through dependency chains; emit conflict pairs with remediation.

## Upgrade risk matrix
| Risk | Update type | Handling |
|---|---|---|
| Low | Patch, security fix | Apply immediately |
| Medium | Minor + features | Batch into scheduled update |
| High | Major, API changes | Dedicated migration task + tests |
| Critical | Known breaking | Planned migration with rollback |

Priority: security patches > bug fixes > feature updates > major rewrites; deprecated features get immediate attention.

## Cadence & best practices
- Security scans per commit; license audits monthly; full audit quarterly.
- High/critical findings immediately; license compliance before functionality.
- Incremental upgrades with thorough testing; feature flags for risky bumps.
- Whitelist false positives WITH documentation; contact maintainers on license ambiguity.

## CI gate
Run the scanner with fail-on-high and the license checker with strict policy as merge gates.
