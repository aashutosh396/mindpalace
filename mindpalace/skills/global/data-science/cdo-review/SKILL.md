---
name: CDO Review (Forcing Questions)
description: Use when validating training-data rights before model work, choosing warehouse vs lakehouse vs mesh, or valuing data assets for productization or M&A — six decision-driven CDO questions before any data commitment.
tags: [cdo-review, training-data, consent-provenance, data-architecture, data-asset, m&a-diligence, forcing-questions, data-hiring]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cdo-review
---

# CDO Review — Six Forcing Questions

Decision-driven pressure test for any plan touching data strategy. Run before: a new ML training run on customer data, signing a multi-year data-infra SaaS contract, productizing customer data, a major data hire, M&A diligence, or whenever someone says "monetize" near "data."

## The six questions

1. **What decision does this data drive?** If no decision is unblocked, why collect/train/productize? "Might need it later" and "feels like a moat" are not decisions.
2. **Consent provenance for every source?** Origin, consent flow, data class, intended use per source. TOS-only is weaker than explicit opt-in; bundled TOS doesn't cover material new purposes (training on PII for foundation models). Run a training-data audit if any AI use case is in scope.
3. **Who consumes this internally — how many distinct functional domains?** Drives centralize-vs-embed and warehouse-vs-mesh. <5 consumers → warehouse; 5–25 → lakehouse; 25+ with federated culture → mesh. Premature architecture is the #1 cause of data-team burnout.
4. **M&A diligence impact?** If an acquirer asks tomorrow, are you ready? Documented anonymization process? % customers with MSA carve-outs? Current provenance logs? Value the corpus quarterly.
5. **Can the model/decision/report be re-run without this source?** Yes → low blast radius (can change consent posture later). No → high blast radius (structurally committed — vet harder).
6. **What role unblocks this — and is it the right next hire?** Wrong hire (data scientist when the answer is analytics engineer) is a 12-month productivity loss. Confirm prerequisite roles are in place (data engineer before ML engineer, analyst before data scientist).

## Output

Verdict 🟢 SHIP / 🟡 SHARPEN / 🔴 BLOCK. State the decision being made (training | architecture | asset | hire), the relevant audit/recommendation, and 3 concrete next steps. Route productization/licensing to legal; architecture touching customer data to security; build-vs-buy TCO and M&A math to finance.
