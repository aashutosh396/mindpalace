---
name: lightning-channel-factories
description: Use when working with Bitcoin Lightning Network channel factories, multi-party channels, LSP architectures, the SuperScalar protocol, or Layer 2 scaling without soft forks — covers Decker-Wattenhofer invalidation trees, timeout-signature trees, MuSig2/BIP-327 key aggregation, Poon-Dryja channels, HTLC/PTLC forwarding, Taproot, and watchtower breach detection.
version: 1.0.0
license: MIT
tags: [bitcoin, lightning-network, channel-factories, superscalar, layer2, musig2, taproot, watchtower]
source: https://github.com/8144225309/superscalar-mcp
derived_from: awesomeclaude
---

# Lightning Channel Factories (SuperScalar)

Technical reference for Lightning Network channel factories: many users sharing
one on-chain UTXO so Lightning onboards N users with a single transaction. The
canonical implementation is **SuperScalar** (C, 400+ tests, MuSig2, Taproot,
Noise NK transport, SQLite, regtest/signet/testnet/mainnet).

- Source: https://github.com/8144225309/SuperScalar
- Website: https://SuperScalar.win
- Proposal: https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143

## When to use

Reach for this when answering questions about channel-factory mechanics, how an
LSP coordinates N clients in one UTXO, or how to scale Lightning onboarding
**without consensus changes** (works on Bitcoin today via Taproot + MuSig2).

## Architecture — three combined mechanisms

1. **Decker-Wattenhofer invalidation trees**
   - Alternating kickoff and state transaction layers.
   - Each layer uses decreasing timelocks so newer states confirm faster.
   - No penalty mechanism needed (unlike Poon-Dryja revocation).
   - Supports N-party updates with one coordinator (the LSP).
   - O(log N) on-chain transactions for unilateral exit vs O(N) flat.

2. **Timeout-signature trees** — each Taproot output has two spend paths:
   - **Key path**: N-of-N MuSig2 aggregate key — cooperative, instant, cheapest.
   - **Script path**: CLTV timelock fallback — unilateral exit if the LSP
     disappears or refuses to sign. Creates a natural factory refresh cycle:
     users re-enter new factories before expiry.

3. **Poon-Dryja payment channels** at the tree leaves:
   - Each leaf output funds a 2-of-2 channel between LSP and one client.
   - Full HTLC support; PTLC via Schnorr adaptor signatures.
   - Standard commitment tx (to_local/to_remote), revocation-based invalidation
     (separate from the tree invalidation).
   - Fully routable like any other Lightning channel.

## Key properties

- No soft fork — uses existing Bitcoin script (Taproot, MuSig2/BIP-327).
- One LSP + N clients share a single UTXO, cutting chain footprint.
- Full Lightning compatibility: HTLC forwarding, watchtowers, standard ops.

## Supporting components

- **MuSig2 (BIP-327)**: two-round N-of-N signing (nonce exchange + partial sigs)
  producing a single Schnorr signature; also adaptor sigs for PTLCs.
- **Watchtower**: monitors chain for revoked-state broadcasts, builds/broadcasts
  justice transactions, stores compact breach hints (not full txs).
- **Transport**: Noise NK handshake (client knows LSP static pubkey in advance),
  forward secrecy, ~54 message types for the factory lifecycle.

## On-chain savings (rough model)

Individual opens cost `N x avg_tx_vbytes` (≈154 vB/P2TR open). A factory costs
`factory_base (≈200 vB) + N x per_user (≈43 vB Taproot output)` in ONE tx.
Savings grow with N. Actual numbers depend on tree depth and cooperative vs
unilateral close paths.

## Background reading

- Decker-Wattenhofer duplex micropayment channels (ETH Zürich paper).
- Timeout trees — John Law: https://github.com/JohnLaw2/ln-scaling-covenants
- MuSig2: https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
- Related stacks: LDK, Core Lightning, LND.
