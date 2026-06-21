---
name: lightning-architecture-review
description: Use when reviewing or comparing Bitcoin Lightning Network protocol designs and channel factory approaches — analyze Layer 2 scaling tradeoffs across trust models, on-chain footprint, consensus/soft-fork requirements, HTLC/PTLC compatibility, liveness, unilateral-exit cost, and watchtower support. Reference point: the SuperScalar channel-factory architecture.
version: 1.0.0
license: MIT
tags: [bitcoin, lightning-network, architecture-review, channel-factories, superscalar, layer2, tradeoffs, watchtower]
source: https://github.com/8144225309/superscalar-mcp
derived_from: awesomeclaude
---

# Lightning Architecture Review

Use this to **evaluate and compare** Lightning Layer 2 / channel-factory designs
along a consistent set of axes. SuperScalar is the worked reference
implementation to benchmark against.

- Source: https://github.com/8144225309/SuperScalar
- Website: https://SuperScalar.win
- Proposal: https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143

## Review checklist (score each design on these axes)

1. **Consensus requirements** — does it need a soft fork (new opcodes like
   CTV/APO/covenants) or does it run on Bitcoin today? SuperScalar needs
   **none** — Taproot + MuSig2 only.
2. **On-chain footprint** — funding cost per onboarded user; one shared UTXO vs
   N individual opens. Channel factories amortize one funding tx over N users.
3. **Unilateral exit cost** — transactions needed when cooperation fails.
   SuperScalar: O(log N) via the invalidation tree vs O(N) flat constructions.
4. **Trust model** — who can grief or steal, and what protects against it?
   Distinguish coordinator (LSP) liveness assumptions from custody. Factories
   are non-custodial but rely on an LSP for cooperative paths.
5. **Liveness / timeout behavior** — what happens if the coordinator disappears?
   Timeout-signature trees give a CLTV fallback so clients can exit; note the
   factory-refresh cycle before timeout expiry.
6. **Payment compatibility** — HTLC and PTLC support, routability with existing
   Lightning. Confirm leaf channels are standard Poon-Dryja.
7. **Watchtower / breach handling** — is there breach detection for offline
   clients, and how cheap are the breach hints to store?
8. **Privacy** — does key-path MuSig2 make cooperative spends look like a single
   signer? Are factory members distinguishable on-chain?

## SuperScalar as a reference point

| Axis | SuperScalar |
|---|---|
| Soft fork | Not required (Taproot + MuSig2/BIP-327) |
| Structure | Decker-Wattenhofer invalidation trees + timeout-signature trees + Poon-Dryja leaf channels |
| Unilateral exit | O(log N) on-chain txs |
| Liveness | N-of-N MuSig2 key path cooperative; CLTV script path fallback |
| Payments | Full HTLC; PTLC via Schnorr adaptor signatures |
| Watchtower | Yes — compact breach hints, justice txs |
| Transport | Noise NK, forward secrecy, ~54 message types |

## How to run a review

- Map the design onto the 8 axes above; flag any axis the design is silent on.
- For each tradeoff, state what is gained and what is given up (e.g. shared UTXO
  cuts footprint but adds coordinator-liveness dependence).
- Compare against SuperScalar and other approaches (Decker-Wattenhofer alone,
  John Law's timeout-tree covenants, ark-style designs) rather than scoring in
  isolation.
- Conclude with the conditions under which each design is the right choice.
