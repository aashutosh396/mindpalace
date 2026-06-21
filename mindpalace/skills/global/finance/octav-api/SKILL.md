---
name: octav-api
description: Use when integrating the Octav API for crypto portfolio tracking, wallet balances, net worth across chains, DeFi protocol positions (Aave, Uniswap), transaction history, or historical portfolio snapshots. Triggers on "Octav API", "crypto portfolio API", "blockchain portfolio tracking", "DeFi analytics API", "wallet balance API", "transaction history API", "multi-chain portfolio", "net worth across chains".
version: 1.0.0
license: MIT
tags: [crypto, defi, portfolio, wallet, blockchain, transactions, octav, web3]
source: https://github.com/Octav-Labs/octav-api-skill
derived_from: awesomeclaude
---

# Octav API Integration

REST API for crypto portfolio tracking, transaction history, and DeFi analytics across 65+ chains.

## What / When
Use to track wallet net worth, list DeFi positions, query/filter transaction history, fetch historical snapshots, or analyze token holdings across EVM chains + Solana.

## Quick Reference
- Base URL: `https://api.octav.fi`
- Auth: `Authorization: Bearer YOUR_API_KEY` (store in `OCTAV_API_KEY`, never hardcode)
- Rate limit: 360 req/min/key
- Credit-based pricing (~$0.02–0.025/credit); credits never expire
- Dev portal: https://data.octav.fi · Docs: https://docs.octav.fi

## Endpoints
| Endpoint | Method | Cost | Description |
|---|---|---|---|
| `/v1/portfolio` | GET | 1 cr | Holdings across chains/protocols |
| `/v1/nav` | GET | 1 cr | Net asset value (single number) |
| `/v1/transactions` | GET | 1 cr | Transaction history with filtering |
| `/v1/token-overview` | GET | 1 cr | Token breakdown by protocol (PRO) |
| `/v1/historical` | GET | 1 cr | Historical snapshot (subscription) |
| `/v1/sync-transactions` | POST | 1+ cr | Trigger transaction sync |
| `/v1/status` | GET | free | Sync status |
| `/v1/credits` | GET | free | Credit balance |

## Portfolio
```javascript
const res = await fetch(
  `https://api.octav.fi/v1/portfolio?addresses=${address}`,
  { headers: { Authorization: `Bearer ${apiKey}` } }
);
const p = await res.json(); // p.networth, p.assetByProtocols, p.chains
```
Params: `addresses` (required, comma-separated EVM/Solana), `includeNFTs`, `includeImages`, `waitForSync`.

Response: `{ networth, assetByProtocols: { wallet:{...}, aave_v3:{...} }, chains: { ethereum:{...}, arbitrum:{...} } }`. Each protocol has `key,name,value,assets[]`; each asset has `balance,symbol,price,value,contractAddress,chain`.

## NAV
`GET /v1/nav?addresses=${address}` → single number (net worth).

## Transactions
```javascript
const params = new URLSearchParams({ addresses:'0x...', limit:'50', offset:'0', sort:'DESC', hideSpam:'true' });
const res = await fetch(`https://api.octav.fi/v1/transactions?${params}`,
  { headers:{ Authorization:`Bearer ${apiKey}` } });
```
Required: `addresses`, `limit` (1–250), `offset`. Optional filters: `sort` (DESC/ASC), `networks`, `txTypes`, `protocols`, `hideSpam`, `hideDust`, `startDate`/`endDate` (ISO 8601), `initialSearchText`.

Returns an array of tx objects: `{ hash, timestamp, chain{key,name}, type, protocol{key,name}, fees, feesFiat, assetsIn[], assetsOut[] }`.

Paginate by looping offset += batch.length until a batch is shorter than `limit`.

## Sync workflow (avoid wasted credits)
1. Check `/v1/status` (free) → `transactionsLastSync`, `syncInProgress`.
2. Only POST `/v1/sync-transactions` (body `{ addresses:[...] }`) if data is stale (>10 min) and not already syncing.
Sync cost: 1 credit + 1 credit per 250 txs on first-time indexing.

## Transaction types (for `txTypes` filter)
`TRANSFERIN, TRANSFEROUT, SWAP, DEPOSIT, WITHDRAW, STAKE, UNSTAKE, CLAIM, ADDLIQUIDITY, REMOVELIQUIDITY, BORROW, LEND, BRIDGEIN, BRIDGEOUT, APPROVAL, MINT`.

## Supported chains
Full (portfolio + tx): ethereum, arbitrum, base, polygon, optimism, avalanche, binance, solana, blast, linea, gnosis, sonic, starknet, fraxtal, unichain. Portfolio-only: scroll, zksync, mantle, manta, fantom, cronos, celo, +40 more. Use keys in `networks` filter.

## Errors
- 401 invalid/missing key · 402 insufficient credits · 403 needs PRO · 429 rate limit (honor `Retry-After`, wait + retry) · 404 address not indexed (>100k txs).
Wrap calls in retry logic that backs off on 429 and throws `error.message` otherwise.

## Cost optimization
1. Batch addresses in one call: `?addresses=0x1,0x2,0x3` (1 credit, not 3).
2. Use free `/v1/status` and `/v1/credits`.
3. Filter server-side via `networks`/`txTypes` rather than client-side.
4. Cache: portfolio ~1 min, transactions ~10 min.
5. Check status before syncing.

## Resources
Dev portal https://data.octav.fi · Docs https://docs.octav.fi · Protocols https://protocols.octav.fi
