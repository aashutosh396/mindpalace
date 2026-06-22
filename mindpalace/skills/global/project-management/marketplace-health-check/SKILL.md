---
name: Repo Health Check (parallel fan-out audit)
description: Use when asked to run a full health check / audit / sweep of a skills-marketplace repo before a release — fans out six parallel inspectors (code safety, doc/SSOT consistency, PII, PR triage, issue triage, manifest integrity), then counter-reviews the serious findings.
tags: [audit, health-check, repo, fan-out, workflow, pii, pr-triage, issue-triage, ssot, security]
source: daymade/claude-code-skills
derived_from: marketplace-health-check
---

Run a comprehensive, evidence-based health check of a Claude Code skills-marketplace repo via a parallel fan-out workflow. Six independent inspectors run in parallel; then YOU verify the serious findings and report by priority.

## Six dimensions
1. **Code & script safety** — dangerous deletes, secret leaks, hardcoded real paths, bare `except`, injection, missing shebangs.
2. **Doc / SSOT consistency** — version coherence across marketplace.json / READMEs / CHANGELOG / git release, skill+plugin counts, broken refs, derived-value drift.
3. **Security / PII** — keyword-free leaks gitleaks can't catch (real names, private domains), scan-marker gaps.
4. **Open-PR triage** — worth-merging / needs-changes / decline-as-promotion.
5. **Open-issue triage** — real bugs vs skill-requests vs promotion, broken-install-command bug class.
6. **Marketplace-manifest integrity** — manifest validation, orphans, suite registration.

## Must run inline
It orchestrates parallel agents via the Workflow tool; a forked subagent cannot spawn subagents — `context: fork` would silently break the fan-out. A user asking to "run the health check" IS the required Workflow opt-in.

## How to run
**Step 1 — Scout scale** (one quick pass, shared by all agents):
```bash
gh repo view --json nameWithOwner,stargazerCount,isPrivate | jq -c .
echo "skills: $(find . -name SKILL.md -not -path '*-workspace/*' | wc -l)"
echo "open PRs: $(gh pr list --state open --json number | jq length)"
echo "open issues: $(gh issue list --state open --json number | jq length)"
```
Confirm `isPrivate: false` before treating PII as a publishing risk.

**Step 2 — Launch** the bundled workflow inline via the `script` param, passing `{repo, scale}`. ~15-20 min, ~400-500k output tokens (tell user the cost up front). Returns one structured result per dimension: `health + summary + findings[] + stats`.

**Step 3 — Counter-Review BEFORE reporting.** Agent findings are HYPOTHESES, never relay verbatim. For every high/critical: verify yourself with a 1-line command (grep the leaked value, `sed -n` the line, `gh repo view`). Filter each finding through four questions: probability, cost, real-scenario, verifiable. This catches false alarms AND wrong recommendations.

## Report format
Lead with a one-line verdict + 6-dimension health table (good/minor/needs-attention/critical). Then: 🔴 Must-fix (verified high/crit + location + concrete fix), 🟠 Backlog (PR/issue triage, outward-facing decisions), 🟢 Optional (nits), 💡 Key insights (structural blind spots, recurring bug classes). Tag each item ✅ real / ⚠️ partly / ❌ false-alarm. Surface real risks the owner didn't know — don't forward 25 raw findings.

## Judgment principles
- **Anti-target:** never "fix" a PII leak by listing the real value in a public allowlist (e.g. `.gitleaks.toml`) — that's itself a leak. Sanitize in place.
- **History note:** sanitizing the working copy doesn't clean git history; flag history exposure honestly, never force-push history unprompted.
- **Scan marker = necessary-not-sufficient:** "no known-format secret found" ≠ "sanitized"; pair with a semantic read of any real-data examples.
- **Mandatory version bump:** any change to a skill's files requires bumping its version + CHANGELOG.
- **Promotion declined by default** for third-party directory/tool/marketplace PRs.

Follow-ups are owner decisions (fix verified HIGHs, triage backlog) — surface as options, don't auto-fix or auto-comment on outward-facing PRs/issues.
