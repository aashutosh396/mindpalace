---
name: wallet-fraud-detector
description: Use when checking if a blockchain wallet address is safe, fraudulent, or sanctioned — AML screening, counterparty verification, pre-transaction safety checks, or onboarding wallet vetting. Triggers on any wallet address (0x..., ENS, Solana) paired with words like safe, trust, check, verify, screen, AML, fraud, risk, or suspicious.
version: 1.0.0
license: MIT
tags: [web3, crypto, fraud-detection, aml, wallet-screening, on-chain, compliance, blockchain]
source: https://github.com/ChainAware/behavioral-prediction-mcp
derived_from: awesomeclaude
prerequisites:
  - ChainAware MCP server (predictive_fraud tool) at https://prediction.mcp.chainaware.ai/sse
  - CHAINAWARE_API_KEY environment variable (get one at https://chainaware.ai/pricing)
---

# Wallet Fraud Detector

Fast, narrow Web3 fraud screening: assess whether a wallet address is fraudulent
using ChainAware's AI fraud engine (~98% accuracy on ETH, ~96% on BNB). Answers
one question well: **is this wallet safe?** For full behavioral profiling or
contract rug-pull checks, hand off to the wallet-auditor / rug-pull detector.

## When to use
- Pre-transaction safety check before sending funds to an address
- AML / compliance verification of a counterparty
- Onboarding or allowlist wallet screening (e.g. NFT drop, presale)
- Any blockchain address provided with a safety concern

## Tool & networks
- **Tool:** `predictive_fraud` (args: `apiKey`, `network`, `walletAddress`)
- **Networks:** ETH · BNB · POLYGON · TON · BASE · TRON · HAQQ
- Auth via `CHAINAWARE_API_KEY` env var. If missing, ask the user to set it
  (key from https://chainaware.ai/pricing). Never log or print the key.

## Workflow
1. Extract wallet address and network from the message.
2. Clarify the network if ambiguous — ask once; don't guess for high-stakes checks.
3. Call `predictive_fraud` with `apiKey`, `network`, `walletAddress`.
4. Return a structured verdict (below).
5. Recommend next steps based on risk level.

## Key response fields
| Field | Notes |
|-------|-------|
| `status` | "Not Fraud" · "Fraud" · "New Address" |
| `probabilityFraud` | parse as float, e.g. "0.0179" → 0.018 |
| `chain` | e.g. "ETH" |
| `lastChecked` / `checked_times` / `createdAt` | scoring history |
| `sanctionData[].isSanctioned` | true = on a sanctions list |
| `forensic_details` | 19 AML flags, each "0" (clean) or "1" (flagged) |

### forensic_details flags (each "1" = flagged)
`cybercrime`, `money_laundering`, `number_of_malicious_contracts_created`,
`gas_abuse`, `financial_crime`, `darkweb_transactions`, `reinit`,
`phishing_activities`, `fake_kyc`, `blacklist_doubt`, `fake_standard_interface`,
`stealing_attack`, `blackmail_activities`, `sanctioned`,
`malicious_mining_activities`, `mixer` (e.g. Tornado Cash), `fake_token`,
`honeypot_related_address`, plus `data_source` (source label).

## Risk thresholds
| probabilityFraud | Risk | Action |
|---|---|---|
| 0.00–0.20 | 🟢 Low | Proceed normally |
| 0.21–0.50 | 🟡 Medium | Proceed carefully; consider monitoring |
| 0.51–0.80 | 🔴 High | Flag for manual review; warn user prominently |
| 0.81–1.00 | ⛔ Critical | Block immediately; do not interact |

**New Address** = insufficient history to score → treat as medium risk by default.

## Output format
```
## Fraud Check: [address]
**Chain:** [chain]
**Status:** [Fraud / Not Fraud / New Address]
**Risk Level:** 🟢 / 🟡 / 🔴 / ⛔
**Fraud Probability:** [parsed float]
**Sanctioned:** [Yes / No]
**Last Checked / Times Checked:** [...]

### Verdict
[safe to proceed / proceed with caution / block this address]

### Key Signals
- [forensic_details flags set to "1"; if none, "No AML flags detected"]
- [note if isSanctioned is true]

### Recommended Action
[specific next step for the risk level]
```

## Batch screening
For multiple addresses, screen in sequence and return a summary table with
columns: Address | Chain | Status | Probability | Sanctioned | Risk, followed by
a summary (count screened, count high/critical, overall recommendation).

## Example triggers
- "Is 0xd8dA...96045 safe on Ethereum?"
- "Run an AML check on this BNB wallet: 0x123..."
- "Screen these 5 wallets before our NFT drop allowlist goes live."
- "Check fraud risk for this TRON address before we whitelist it."
