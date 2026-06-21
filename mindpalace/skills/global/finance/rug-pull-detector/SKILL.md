---
name: rug-pull-detector
description: Use when checking if a smart contract, liquidity pool, DeFi token, or newly launched project is safe to invest in before committing capital — rug pull risk, exit scam, liquidity drain, honeypot, token launch / IDO / presale vetting, or LP security. Triggers on a contract or LP address paired with investment intent or phrases like "is this legit", "should I ape in", "is this pool safe", "just launched".
version: 1.0.0
license: MIT
tags: [web3, crypto, rug-pull, defi, smart-contract, honeypot, liquidity-pool, on-chain, fraud-detection]
source: https://github.com/ChainAware/behavioral-prediction-mcp
derived_from: awesomeclaude
prerequisites:
  - ChainAware MCP server (predictive_rug_pull, predictive_fraud tools) at https://prediction.mcp.chainaware.ai/sse
  - CHAINAWARE_API_KEY environment variable (get one at https://chainaware.ai/pricing)
---

# Rug Pull Detector

Assess whether a smart contract, liquidity pool, or DeFi project is likely to
rug pull — *before* the user commits capital. Analyze three layers at once:

1. **Contract layer** — bytecode patterns, admin keys, mint functions, honeypot signals
2. **Deployer layer** — the deploying wallet's cross-chain behavioral history
3. **Liquidity layer** — LP wallet behavior, lock status, withdrawal velocity

Core insight: **bad actors cannot create good contracts.** A deployer's on-chain
history across chains reveals who they are, regardless of how polished the
website or whitepaper looks.

## Tools & networks
- **Primary:** `predictive_rug_pull` — scores the contract / LP address
- **Secondary:** `predictive_fraud` — scores the deployer wallet for context
- **Networks (rug pull):** ETH · BNB · BASE · HAQQ
- Auth via `CHAINAWARE_API_KEY` env var. If missing, ask the user to set it
  (key from https://chainaware.ai/pricing). Never log or print the key.

## Workflow
1. Extract the contract address and network. Clarify network if ambiguous — ask once.
2. Run `predictive_rug_pull` on the contract address.
3. Run `predictive_fraud` on the deployer address if available in `forensic_details`.
4. Combine both scores into a single unified verdict.
5. Return structured output with a clear invest / caution / avoid recommendation.

## Risk thresholds
| probability | Risk | Verdict | Action |
|---|---|---|---|
| 0.00–0.20 | 🟢 Low | Appears Safe | Proceed — standard due diligence still advised |
| 0.21–0.50 | 🟡 Medium | Caution | Verify LP lock, check deployer history manually |
| 0.51–0.80 | 🔴 High | High Risk | Do not deposit — warn community prominently |
| 0.81–1.00 | ⛔ Critical | Rug Pull Likely | Avoid entirely — flag to launchpad/DEX |

## Deployer risk amplifier
If the deployer's `predictive_fraud` score is **0.5+**, escalate the overall
verdict by one level regardless of the contract score. Serial rug pullers deploy
clean-looking contracts — the deployer history is often the most reliable signal.
Example: contract 0.35 (Medium) + deployer 0.72 (High) → combined 🔴 HIGH RISK.

## Output format
```
## Rug Pull Check: [contract address]
**Network:** [network]
**Contract Type:** [LP Pool / Token Contract / Unknown]
**Rug Pull Probability:** [0.00–1.00]
**Status:** [Fraud / Not Fraud]
**Risk Level:** 🟢 / 🟡 / 🔴 / ⛔

### Deployer Assessment (if available)
- Deployer: [address] · Fraud Probability: [0.00–1.00] · Risk: 🟢/🟡/🔴/⛔

### Red Flags Detected
- [signals from forensic_details — e.g. mint function present, LP unlocked, admin key active]

### Verdict
⛔ AVOID / 🔴 HIGH RISK / 🟡 PROCEED WITH CAUTION / 🟢 APPEARS SAFE
[one clear sentence explaining why]

### Recommended Action
[specific next step — e.g. "Do not deposit", "Check LP lock expiry", "Safe to proceed"]
```

## Limitations
- Rug pull scoring supports **ETH, BNB, BASE, HAQQ only**. For POLYGON, TON,
  TRON, SOLANA, run `predictive_fraud` on the deployer wallet instead and note
  the limitation clearly.
- New contracts with minimal history may return low scores — treat unscored new
  contracts as medium risk by default.

## Batch screening
For multiple contracts, screen in sequence and return a summary table:
Contract | Network | Rug Pull Prob | Deployer Fraud | Risk | Verdict, followed by
a summary (count screened, count high/critical, overall recommendation).

## Example triggers
- "Will this new BNB pool rug pull? Contract: 0x123..."
- "Is this ETH token contract safe before I ape in?"
- "Should I invest in this IDO? Contract address: 0x456..."
- "Our launchpad needs a safety check on 0x789... before listing."
