---
name: Benchmark Due Diligence (adversarial teardown)
description: Use when the user wants to tear down a competitor or role-model they envy — a founder, KOL, company, or product whose claimed success looks inflated — separating marketing bubble from real signal and mapping the validated playbook onto the user's own resources.
tags: [due-diligence, competitor, teardown, adversarial, bubble, attribution, playbook, osint, verification]
source: daymade/claude-code-skills
derived_from: benchmark-due-diligence
---

Take a benchmark the user envies and produce a teardown ending in **"what this means for ME"** — not a neutral report. Answers three questions a balanced briefing never does: how much of this success is real vs marketing bubble? how much is replicable method vs luck/timing? what specifically can the commissioner do with it? **Assume the picture is inflated until proven otherwise.**

## Run inline, never `context: fork`
This is an orchestrator — it spawns parallel collection + verification agents and may invoke other skills. Subagents can't spawn subagents; `context: fork` would silently break the fan-out.

## The one rule that protects the commissioner: two injection channels
| Channel | Content | Injected into |
|---|---|---|
| **FACTS** | Verified *public* facts about the benchmark (relationships, headline claim flagged `⚠️ to-verify`) | Every agent |
| **COMMISSIONER_CONTEXT** | The commissioner's *private* reality — real resources, client names, intent | **Only the final mapping agent (Phase 4)** |
Collection/verification agents run external WebSearch on their input; leaking the commissioner's client names/strategy into them = a privacy breach on the open web. Encode the split in orchestration, don't rely on remembering it.

## Phase 0 — nail the foundation by evidence, not appearance (before any agent)
Two recurring failure modes: (1) inferring relationships from names/domains (a shared domain/name is an *observation*, not ownership — verify A↔B with an authoritative source); (2) treating the commissioner's *client* as the commissioner's *asset*. Establish by evidence: the benchmark's real entity graph (who owns whom vs guests/partners); the **headline-claim attribution** (their whole narrative rests on one trophy stat — are they the founder or the departed growth lead? #1 to-verify, write to FACTS with ⚠️); and what the commissioner truly controls (owned vs client assets).

## Four-phase orchestration
**Phase 1+2 — collect → verify per dimension** (each verifies the moment its collection finishes):
- Collection agent (objective): every finding has a source URL + `source_kind` (self/marketing vs independent vs mixed). Unknowns → `gaps`, never guessed.
- Verification agent (adversarial, default-skeptical): grade every claim L1-L4, rule 坐实/大体可信/存疑/证伪-水分. Actively hunt *falsifying* evidence for headline claims (trophy stat, "#1", funding, user counts). `bubble_summary` names the biggest water.

Typical dimensions: subject background + headline attribution; corporate base (entity/funding/valuation); core product real metrics (cross-verified vs third parties); playbook teardown (platform matrix, persona, how they borrow audiences, IP→product funnel); a comparison peer; sector typical-win/typical-fail patterns.

**Phase 3 — synthesis (due-diligence conclusion):** real relationship map (correcting Phase 0 misreadings); **bubble-busting table** (claim | evidence level | verdict | one-line basis, most-water-first); copyable playbook teardown; **attribution breakdown** — what share is product vs market-timing vs personal-IP-marketing vs operations (% ranges + reasons), explicitly splitting replicable method from luck/timing/non-transferable endowment.

**Phase 4 — what this means for the commissioner** (consumes Phase 3 + COMMISSIONER_CONTEXT): **resource-mapping table** (benchmark's playbook × commissioner's real resources, each cell tagged ✅ borrow-able / ⚠️ not-replicable / 🔄 already-doing / 🚫 bubble-don't-copy); landing points; action list + open questions.

## Reuse, don't rebuild
The edge is the adversarial bubble-busting + attribution + commissioner-mapping. Borrow fan-out/source-governance from a deep-research skill; person-identity checks from an OSINT skill; corporate-registration from a registry skill. Read the evidence-discipline traps (inferring relationships from appearance, headline attribution, client-vs-asset, grade-don't-binary, privacy leak) before running — that's where runs break.
