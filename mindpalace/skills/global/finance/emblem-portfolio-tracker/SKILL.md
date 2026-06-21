---
name: emblem-portfolio-tracker
description: "Use when tracking a crypto portfolio across multiple chains (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin) via EmblemAI — aggregated balances with USD values, conditional trade P&L, and DeFi positions. Triggers: 'check my portfolio', 'show balances across all chains', 'what's my P&L', 'show my trade positions'."
version: 1.0.0
license: MIT
tags: [crypto, portfolio, multi-chain, balances, pnl, defi, wallet, web3]
source: https://github.com/EmblemCompany/Agent-skills/tree/main/skills/emblem-portfolio-tracker
derived_from: awesomeclaude
prerequisites: ["Node.js >= 18", "@emblemvault/agentwallet CLI (emblemai)", "internet access"]
---

# Emblem Portfolio Tracker

Cross-chain crypto portfolio monitoring via EmblemAI. Aggregated balances with
USD values across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin.
Conditional-trade P&L and DeFi position viewing (via Nansen).

**Requires:** `npm install -g @emblemvault/agentwallet`

## When to use
- "Check my portfolio" / "Show balances across all chains"
- "What's my P&L?" / "Show my trade positions"

## Capabilities → tools
| Capability | Tool(s) |
|---|---|
| Wallet addresses (all chains) | `wallet` |
| Solana / ETH / Base / BSC / Polygon balances + USD | `solanaBalances`, `ethGetBalances`, `baseGetBalances`, `bscGetBalances`, `polygonGetBalances` |
| Hedera balances | `hederaGetBalances` |
| Bitcoin balances | `getBTCBalances` |
| Crypto price lookup | `getCryptoPrice` |
| Conditional trade positions & P&L | `getAllPositions`, `listPositions` |
| DeFi positions (LP, staking, farming) | `nansen_defi_portfolio` |

## Not supported (no backing tools)
- Transaction history / tax exports (no historical tx data).
- Unrealized P&L on held tokens (only realized P&L from conditional trades).
- 24h portfolio change (no balance snapshots; current balances only).
- Allocation % (agent must compute from per-chain balance calls).

## Quick start
```bash
npm install -g @emblemvault/agentwallet
# All balances at once
emblemai --agent --profile default -m "Show my balances across all chains with USD values. Use solanaBalances, ethGetBalances, baseGetBalances, bscGetBalances, polygonGetBalances, hederaGetBalances, getBTCBalances"
# Trade positions
emblemai --agent --profile default -m "Use getAllPositions to show my open and closed trade positions with P&L"
```

## Workflow: full portfolio review
1. **Addresses:** `emblemai --agent --profile default -m "Use wallet to list all my wallet addresses across every chain"`
2. **Balance snapshot:** name each tool explicitly for reliable execution
   (`solanaBalances`, `ethGetBalances`, `baseGetBalances`, `bscGetBalances`,
   `polygonGetBalances`, `hederaGetBalances`, `getBTCBalances`).
3. **Positions & P&L:** `getAllPositions` — only covers conditional trades
   (limit/stop-loss/take-profit) created through EmblemAI; wallet holdings have
   no cost basis.
4. **DeFi (optional):** for Nansen-indexed wallets,
   `nansen_defi_portfolio` for wallet `[ADDRESS]` on `[CHAIN]`.

## Quick daily check
```bash
emblemai --agent --profile default -m "Quick portfolio check — use solanaBalances, ethGetBalances, and getBTCBalances to show my main holdings"
```

## Notes
- Always pass an explicit `--profile` when more than one profile exists.
- Read-only by design — no value-moving actions here.
