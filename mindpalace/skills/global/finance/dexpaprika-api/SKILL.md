---
name: dexpaprika-api
description: Use when querying DEX / on-chain crypto data — liquidity pools, DEX token prices by contract address, pool OHLCV, swaps/transactions, networks, or streaming real-time token prices and pool reserves via api.dexpaprika.com / streaming.dexpaprika.com / dexpaprika-cli. Triggers on DEX pools, token price by contract, on-chain liquidity, pool reserves, Uniswap/Raydium data.
version: 1.0.0
license: MIT
tags: [crypto, dex, on-chain, dexpaprika, liquidity-pools, ohlcv, streaming, finance]
source: https://github.com/coinpaprika/skills/tree/main/dexpaprika-api
derived_from: awesomeclaude
---

# DexPaprika API

Free DEX data: 34 chains, 213 DEXes, 30M+ pools, 27.7M+ tokens. By the CoinPaprika team. No key. Free tier 10,000 req/day; Enterprise (api-pro.dexpaprika.com) unlimited with key.

- Docs: https://docs.dexpaprika.com  |  Agents: https://agents.dexpaprika.com

> **Field naming:** URL paths use `network` and `token_address`; JSON responses return `chain` and `id` for the same values.

## Integration options

### CLI (recommended for agents)
```bash
curl -sSL https://raw.githubusercontent.com/coinpaprika/dexpaprika-cli/main/install.sh | sh
```
Always pass `--output json --raw`. `dexpaprika-cli onboard` for quick-start.
```bash
dexpaprika-cli search USDC --output json --raw
dexpaprika-cli token ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --output json --raw
dexpaprika-cli pools ethereum --limit 10 --output json --raw
dexpaprika-cli pool-ohlcv ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --start 2025-01-27 --output json --raw
dexpaprika-cli top-tokens ethereum --limit 20 --output json --raw
dexpaprika-cli filter-tokens ethereum --volume-24h-min 100000 --output json --raw
dexpaprika-cli pool-filter ethereum --volume-24h-min 500000 --liquidity-usd-min 50000 --output json --raw
dexpaprika-cli prices ethereum --tokens 0xc02...,0xa0b... --output json --raw
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
dexpaprika-cli status
```
Full CLI ref: `references/cli-reference.md`.

### REST API
Base: `https://api.dexpaprika.com` — no auth, JSON.

| Need | Endpoint |
|------|----------|
| All networks | `GET /networks` |
| DEXes on network | `GET /networks/{network}/dexes` |
| Top pools | `GET /networks/{network}/pools` |
| Filter pools | `GET /networks/{network}/pools/filter` |
| Pool details | `GET /networks/{network}/pools/{pool_address}` |
| Pool OHLCV | `GET /networks/{network}/pools/{pool_address}/ohlcv` |
| Pool transactions | `GET /networks/{network}/pools/{pool_address}/transactions` |
| Token price + data | `GET /networks/{network}/tokens/{token_address}` |
| Pools containing token | `GET /networks/{network}/tokens/{token_address}/pools` |
| Filter tokens | `GET /networks/{network}/tokens/filter` |
| Top tokens | `GET /networks/{network}/tokens/top` |
| Batch prices | `GET /networks/{network}/multi/prices?tokens={a},{b}` |
| Pools for a DEX | `GET /networks/{network}/dexes/{dex}/pools` |
| Search | `GET /search?query={term}` |
| Platform stats | `GET /stats` |

Full spec: `references/openapi.yml`.

### Hosted MCP (AI IDEs)
`{"mcpServers":{"dexpaprika":{"url":"https://mcp.dexpaprika.com/sse"}}}` — no key. Tools for networks, pools, tokens, OHLCV, transactions, search.

### Streaming (real-time)
Base: `https://streaming.dexpaprika.com`. Two SSE feeds: `/sse/prices` (~1s token prices), `/sse/reserves` (block-level pool reserves with USD deltas). Limits: 25 subs/POST, 10 concurrent streams/IP, `ping` every 15s.

```bash
# single token price (GET) — HTTP/1.1 required
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/prices?method=token_price&chain=ethereum&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
# multiple (POST, ≤25)
curl --http1.1 -N -X POST "https://streaming.dexpaprika.com/sse/prices" \
  -H "Accept: text/event-stream" -H "Content-Type: application/json" \
  -d '[{"chain":"ethereum","address":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","method":"token_price"}]'
# pool reserves
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/reserves?method=pool_reserves&chain=ethereum&address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
```

- `token_price` event: `address,chain,price` (USD string), `timestamp,timestamp_price` (unix). Legacy `t_p`/`/stream` deprecated — do not use.
- Reserves feed uses **method-named events** (old `reserve_update` is gone): match `pool_reserves` (nested `tokens[]`) and `token_reserves` (flat per token). Raw `reserve`/`delta`/`block` exceed `Number.MAX_SAFE_INTEGER` — parse with `BigInt`.
- Optional `request_id` (uint32) echoes back on data events only.
- **Requires HTTP/1.1** (`--http1.1`). One invalid asset cancels the whole stream (400). SSE parsers must buffer one message between blank lines — both `event:`/`data:` orderings are valid.

Full streaming ref: `references/streaming-api.md`.

### SDKs
Go, Python, TypeScript, PHP, Rust (all under github.com/coinpaprika).

## Common workflows

```bash
# token price
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" | jq '.summary.price_usd'
# search (fuzzy name+symbol — filter exact symbol client-side)
curl -s "https://api.dexpaprika.com/search?query=PEPE" | jq '.tokens[:5]'
# pool OHLCV
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv?start=2025-01-01&interval=1h&limit=24" | jq
# batch prices (returns an ARRAY, max 10 tokens)
curl -s "https://api.dexpaprika.com/networks/ethereum/multi/prices?tokens=0xc02...,0xa0b..." | jq
```

OHLCV params: `start` (required), `end`, `interval` (`1m,5m,10m,15m,30m,1h,6h,12h,24h`), `limit` (max 366), `inversed` (bool, flips price ratio for stablecoin-paired USD prices).

## Common addresses (don't guess — use search)

| Token | Chain | Address |
|-------|-------|---------|
| WETH | ethereum | 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 |
| USDC | ethereum | 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 |
| USDC | solana | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| SOL | solana | So11111111111111111111111111111111111111112 |

Networks (lowercase): `ethereum, solana, bsc, polygon, arbitrum, base, avalanche, optimism, sui, ton, tron`. Full list: `GET /networks`.

## Pagination / timestamps / errors

- List endpoints: `?page=1&limit=10&order_by=volume_usd&sort=desc` (1-indexed, max 1000 pages). `order_by`: `volume_usd, liquidity_usd, price_usd, transactions, last_price_change_usd_24h, created_at`. Filter endpoints use `sort_by`/`sort_dir`.
- Timestamps: Unix, RFC3339, or `yyyy-mm-dd`. OHLCV max 366 points/request.
- Errors: 200 OK, 400 bad params, 404 not found, 429 rate limited (wait+retry), 500 server. Health: `GET /stats` or `dexpaprika-cli status`.
