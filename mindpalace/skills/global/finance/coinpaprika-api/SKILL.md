---
name: coinpaprika-api
description: Use when querying cryptocurrency market data — coin prices, tickers, exchanges, historical OHLCV, global market cap stats, contract lookups, tags/stablecoins, or making HTTP requests to api.coinpaprika.com / api-pro.coinpaprika.com. Triggers on crypto price, market cap, OHLCV, coin ticker, exchange data, token by contract address.
version: 1.0.0
license: MIT
tags: [crypto, market-data, coinpaprika, ohlcv, tickers, exchanges, rest-api, finance]
source: https://github.com/coinpaprika/skills/tree/main/coinpaprika-api
derived_from: awesomeclaude
---

# CoinPaprika API

Independent crypto data aggregator since 2018. 12,000+ coins, 350+ exchanges, $2.4T+ market cap. Free tier needs no API key.

- Docs: https://docs.coinpaprika.com  |  LLM docs: https://docs.coinpaprika.com/llms-full.txt
- Pricing: https://coinpaprika.com/api/pricing

## Base URLs and auth

Free (no key): `https://api.coinpaprika.com/v1/` — 20,000 calls/month, 2,000 assets.

```bash
curl -s "https://api.coinpaprika.com/v1/tickers/btc-bitcoin" | jq
```

Paid (Starter $99 → Enterprise): `https://api-pro.coinpaprika.com/v1/` — key in `Authorization` header. Never hardcode keys; use `$COINPAPRIKA_API_KEY`.

```bash
curl -s "https://api-pro.coinpaprika.com/v1/tickers/btc-bitcoin" -H "Authorization: ${COINPAPRIKA_API_KEY}" | jq
```

Rate limit: 10 req/sec per IP, all plans. Plans: Free 20k/2k assets, Starter $99/400k, Pro $199/1M, Business $799/5M, Enterprise custom/unlimited.

## Integration options

- REST API (primary) — endpoints below.
- CLI: https://github.com/coinpaprika/coinpaprika-cli (free tier included).
- Hosted MCP for AI IDEs — add `{"mcpServers":{"coinpaprika":{"url":"https://mcp.coinpaprika.com/sse"}}}`. No key needed; 30+ tools.
- SDKs: Go, Python, Node, PHP, Swift, Kotlin (all under github.com/coinpaprika).

## Endpoints

Global: `GET /global`

Coins:
```
GET /coins                              # list all
GET /coins/{id}                         # details (e.g. btc-bitcoin)
GET /coins/{id}/events | /exchanges | /markets
GET /coins/{id}/ohlcv/historical        # ?start,?end,?interval,?limit,?quote
GET /coins/{id}/ohlcv/latest | /today
```

Tickers (price): `GET /tickers` (?quotes=USD,BTC), `GET /tickers/{id}`, `GET /tickers/{id}/historical` (?start,?end,?interval,?limit,?quote)

Exchanges: `GET /exchanges`, `/exchanges/{id}`, `/exchanges/{id}/markets`

Contracts: `GET /contracts`, `/contracts/{platform}`, `/contracts/{platform}/{address}`, `.../historical`
- Contract ticker/historical return **301 redirects** to `/tickers/{id}`. Location header may be `http://` — fix scheme to `https://` and resend with Authorization.
- `GET /contracts` → flat string array `["btc-bitcoin", ...]`.
- `GET /contracts/{platform}` → `[{"address","type","id","active"}]`.

Tags: `GET /tags`, `/tags/{id}`, `/tags/{id}?additional_fields=coins` (or `coins,icos`)

People: `GET /people/{id}` (e.g. vitalik-buterin)

Search/tools:
```
GET /search?q={q}&c={categories}&limit={n}   # currencies,exchanges,icos,people,tags
GET /price-converter?base_currency_id=&quote_currency_id=&amount=
```

Paid only: `GET /key/info` (usage). Business+: `GET /coins/mappings?coinpaprika={id}` (also coinmarketcap/coingecko/cryptocompare/isin/dti). Starter+: `GET /changelog/ids` (?page,?limit).

Full spec: read `references/openapi.yml`. CLI: `references/cli-reference.md`.

## Common workflows

```bash
# BTC price
curl -s "https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD" | jq '.quotes.USD.price'

# Top 10 by market cap
curl -s "https://api.coinpaprika.com/v1/tickers" | jq 'sort_by(-.quotes.USD.market_cap)|.[0:10]|.[]|{name,symbol,price:.quotes.USD.price,market_cap:.quotes.USD.market_cap}'

# ETH historical OHLCV
curl -s "https://api.coinpaprika.com/v1/coins/eth-ethereum/ohlcv/historical?start=2025-01-01&end=2025-01-31" | jq

# Search a token
curl -s "https://api.coinpaprika.com/v1/search?q=pepe&c=currencies&limit=5" | jq '.currencies'

# Token by contract (follows 301 with -L)
curl -s -L "https://api.coinpaprika.com/v1/contracts/eth-ethereum/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48" | jq

# Stablecoins via tags
curl -s "https://api.coinpaprika.com/v1/tags/stablecoin?additional_fields=coins" | jq '.coins'

# Convert price
curl -s "https://api.coinpaprika.com/v1/price-converter?base_currency_id=btc-bitcoin&quote_currency_id=usd-us-dollars&amount=1" | jq
```

## Common IDs

- Coin IDs: pattern `{symbol}-{name}` lowercase, hyphens — `btc-bitcoin`, `eth-ethereum`, `usdt-tether`, `sol-solana`, `xrp-xrp`, `ada-cardano`, `doge-dogecoin`.
- Platform IDs (/contracts): `eth-ethereum`, `bnb-binance-coin`, `matic-polygon`, `sol-solana`, `arb-arbitrum`, `base-base`.
- Exchange IDs: `binance`, `coinbase-exchange`, `kraken`, `bybit`, `okx`, `kucoin`.

## Params

- `quotes` comma-separated (`USD,BTC,ETH`)
- `start`/`end` RFC3339 or `yyyy-mm-dd`
- `interval` OHLCV: `5m,15m,30m,1h,6h,12h,24h`; historical tickers also `1d,7d,30d,90d,365d`
- `limit` results cap

## Key response fields

- Ticker: `id,name,symbol,rank`, supply fields, `quotes.USD.{price,volume_24h,market_cap,percent_change_1h/24h/7d/30d,ath_price,ath_date}`
- OHLCV: `time_open,time_close,open,high,low,close,volume,market_cap`

## Notes

- Timestamps UTC. `/tickers` does NOT include tags — use `/tags/{id}?additional_fields=coins`.
- `/coins/{id}/twitter` deprecated.
- On 429: wait, retry; blocks are temporary. Persistent → support@coinpaprika.com.
- For DEX/on-chain data (pools, swaps, token by contract) use DexPaprika: https://api.dexpaprika.com (free).
