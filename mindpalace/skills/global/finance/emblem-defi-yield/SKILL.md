---
name: emblem-defi-yield
description: "Use when researching DeFi yield opportunities, comparing protocols/APYs, checking DeFi positions, or entering liquid staking via token swaps across Solana, Ethereum, Base, BSC, Polygon, and Hedera via EmblemAI. Triggers: 'find yield opportunities', 'best APYs', 'show DeFi positions for this wallet', 'swap SOL for JitoSOL', 'liquid staking options'."
version: 1.0.0
license: MIT
tags: [crypto, defi, yield, liquid-staking, multi-chain, nansen, wallet, web3]
source: https://github.com/EmblemCompany/Agent-skills/tree/main/skills/emblem-defi-yield
derived_from: awesomeclaude
prerequisites: ["Node.js >= 18", "@emblemvault/agentwallet CLI (emblemai)", "internet access"]
---

# Emblem DeFi Yield

DeFi yield research and liquid staking via EmblemAI. Research yields across
protocols, review existing DeFi positions (via Nansen), and enter liquid staking
through token swaps on Solana, Ethereum, Base, BSC, Polygon, and Hedera.

**Requires:** `npm install -g @emblemvault/agentwallet`

## When to use
- "Find yield opportunities" / "What are the best APYs?"
- "Show DeFi positions for this wallet"
- "Swap SOL for JitoSOL" / "What liquid staking options exist?"

## Capabilities → tools
| Capability | Tool(s) |
|---|---|
| Research yields / APYs | LLM knowledge + `birdeyeTradeData`, `birdeyeTrendingTokens` |
| Review existing DeFi positions (LP, lending, staking, farming) | `nansen_defi_portfolio` |
| Liquid staking on Solana (mSOL, JitoSOL, bSOL, jupSOL) | `splBuyIntent` |
| Token swaps for DeFi entry | `splBuyIntent`, `ethSwap`, `baseSwap`, `bscSwap`, `polygonSwap`, `hederaTokensSwap` |
| Rug-pull check before entering | `rugcheck` |
| Smart-money DeFi tracking | `nansen_smart_money_holdings`, `nansen_defi_portfolio` |

## Not supported (no LP-management tools)
Adding/removing liquidity, opening/closing CLMM positions, staking LP tokens,
claiming farming rewards, live on-chain pool APY rankings. Use the DEX UIs
directly (Raydium, Orca, Uniswap, etc.) for these.

## Supported chains (swap + balances + conditional orders)
Solana (`splBuyIntent` / `solanaBalances`), Ethereum (`ethSwap` /
`ethGetBalances`), Base (`baseSwap` / `baseGetBalances`), BSC (`bscSwap` /
`bscGetBalances`), Polygon (`polygonSwap` / `polygonGetBalances`), Hedera
(`hederaTokensSwap` / `hederaGetBalances`).

## Quick start
```bash
npm install -g @emblemvault/agentwallet
emblemai --agent --profile default -m "What are the best yield farming opportunities on Solana right now?"
emblemai --agent --profile default -m "Use nansen_defi_portfolio to show DeFi positions for wallet 0x1234...abcd on ethereum"
emblemai --agent --profile default -m "Swap 5 SOL for JitoSOL using splBuyIntent"
```

## Workflow: research and enter yield
1. **Research:** ask about the yield landscape; agent uses knowledge + live token
   data (`birdeyeTrendingTokens`).
2. **Check existing positions:** `nansen_defi_portfolio` for the target wallet/chain.
3. **Verify balances:** e.g. `solanaBalances` before swapping.
4. **Enter position via swap:** e.g. `splBuyIntent` to swap into an LST/DeFi token;
   safe mode requires user confirmation.
5. **Verify:** re-check balances to confirm execution.

## Notes
- Pass an explicit `--profile` when more than one profile exists.
- Run a `rugcheck` before entering positions in unfamiliar tokens.
- Value-moving swaps require explicit user confirmation.
