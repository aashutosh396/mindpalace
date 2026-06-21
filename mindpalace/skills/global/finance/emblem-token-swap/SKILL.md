---
name: emblem-token-swap
description: "Use when swapping or exchanging crypto tokens, converting between currencies, or bridging assets cross-chain via EmblemAI across Solana, Ethereum, Base, BSC, Polygon, and Hedera (cross-chain via ChangeNow). Triggers: 'swap SOL to USDC', 'exchange ETH for USDT', 'convert my tokens', 'bridge tokens to Base'."
version: 1.0.0
license: MIT
tags: [crypto, token-swap, dex, cross-chain, bridge, multi-chain, web3, wallet]
source: https://github.com/EmblemCompany/Agent-skills/tree/main/skills/emblem-token-swap
derived_from: awesomeclaude
prerequisites: ["Node.js >= 18", "@emblemvault/agentwallet CLI (emblemai)", "internet access"]
---

# Emblem Token Swap

Guided token swapping via EmblemAI with automatic route optimization. Swap on
Solana, Ethereum, Base, BSC, Polygon, and Hedera; bridge cross-chain via
ChangeNow (500+ currencies).

**Requires:** `npm install -g @emblemvault/agentwallet`

## When to use
- "Swap SOL to USDC" / "Exchange ETH for USDT"
- "Convert my tokens" / "Bridge tokens to Base"

## Chain → tools
| Chain | Quote | Swap | Balance | Token search |
|---|---|---|---|---|
| Solana | `splBuyIntent` (quote mode) | `splBuyIntent` | `solanaBalances` | `findSolanaSwapToken` |
| Ethereum | `ethSwapQuote` | `ethSwap` | `ethGetBalances` | `searchCryptoByName` |
| Base | `baseSwapQuote` | `baseSwap` | `baseGetBalances` | `searchEvmTokensBirdeye` |
| BSC | `bscSwapQuote` | `bscSwap` | `bscGetBalances` | `searchEvmTokensBirdeye` |
| Polygon | `polygonSwapQuote` | `polygonSwap` | `polygonGetBalances` | `searchEvmTokensBirdeye` |
| Hedera | `hederaTokensSwapQuote` | `hederaTokensSwap` | `hederaGetBalances` | `hederaFindTokens` |
| Cross-chain | `getChangeNowSwapQuote` | `swapUsingChangeNow` | — | `getChangeNowSupportedCurrencies` |

Notes: Solana's `splBuyIntent` handles both quote and execution and accepts
name/symbol/CA plus flexible amounts ($USD, SOL, or token quantity). EVM chains
route through automatic DEX aggregation. Bitcoin has balances
(`getBTCBalances`) but no on-chain swap — use ChangeNow to bridge BTC.

## Safe swap workflow (review-first)
1. **Check balance** — confirm enough of the source token (e.g. `solanaBalances`).
2. **Get a quote** — preview before executing (e.g. `splBuyIntent` quote mode).
3. **Execute** — safe mode requires explicit confirmation before swapping.
4. **Verify** — re-check balances after.

## Quick start
```bash
npm install -g @emblemvault/agentwallet
# Solana swap
emblemai --agent --profile default -m "Use splBuyIntent to swap 5 SOL for USDC on Solana"
# Cross-chain bridge quote
emblemai --agent --profile default -m "Use getChangeNowSwapQuote to quote bridging 0.05 ETH from Ethereum to SOL on Solana"
```

## Patterns
```bash
# Solana — by token amount / dollar amount / token name
emblemai --agent --profile default -m "Use splBuyIntent to swap 0.5 SOL for USDC"
emblemai --agent --profile default -m "Use splBuyIntent to swap \$20 of SOL for JUP"
emblemai --agent --profile default -m "Use splBuyIntent to swap 100 USDC for BONK"
# EVM — quote then execute
emblemai --agent --profile default -m "Use ethSwapQuote to quote 0.01 ETH to USDC, then use ethSwap to execute"
emblemai --agent --profile default -m "Use baseSwapQuote to quote 0.005 ETH to USDC on Base"
emblemai --agent --profile default -m "Use bscSwapQuote to quote 0.1 BNB to USDT on BSC"
```

## Notes
- Pass an explicit `--profile` when more than one profile exists.
- Never broadcast a value-moving swap without explicit user confirmation.
