---
name: lightning-factory-explainer
description: Use when explaining Bitcoin Lightning channel factories or the SuperScalar protocol to someone — scalable Lightning onboarding via shared UTXOs, Decker-Wattenhofer trees, timeout-signature trees, MuSig2, and Taproot, with no soft fork required. Good for teaching, summaries, and answering "what is SuperScalar / how do channel factories scale Lightning".
version: 1.0.0
license: MIT
tags: [bitcoin, lightning-network, channel-factories, superscalar, explainer, musig2, taproot, layer2]
source: https://github.com/8144225309/superscalar-mcp
derived_from: awesomeclaude
---

# Lightning Factory Explainer

Use this to **explain** Lightning channel factories and SuperScalar clearly,
not to design or review one. Reach for it on prompts like "what is SuperScalar",
"how do channel factories scale Lightning", or "explain shared-UTXO onboarding".

- Source: https://github.com/8144225309/SuperScalar
- Website: https://SuperScalar.win

## The one-line answer

A channel factory lets N users share a single on-chain UTXO, so Lightning can
onboard many users with one transaction instead of N channel opens. SuperScalar
implements this **with no consensus changes** — it runs on Bitcoin today using
Taproot and MuSig2.

## How it works (explain in this order)

1. **The problem**: every Lightning channel normally needs its own on-chain
   open. Onboarding N users = N transactions = N UTXOs = lots of block space.
2. **The shared UTXO**: SuperScalar puts one Liquidity Service Provider (LSP)
   and N clients into a single funding UTXO.
3. **Three layers stacked inside that UTXO**:
   - *Decker-Wattenhofer invalidation trees* — update shared state off-chain
     using alternating kickoff/state layers with decreasing timelocks; no
     penalty needed.
   - *Timeout-signature trees* — each node has an N-of-N MuSig2 key-path
     (cooperative, instant) and a CLTV script-path fallback (unilateral exit
     if the LSP stops cooperating).
   - *Poon-Dryja channels* at the leaves — ordinary Lightning channels with
     full HTLC (and PTLC via adaptor signatures) support.
4. **Exit**: cooperative close is off-chain and cheap; if cooperation fails a
   client can exit on-chain in O(log N) transactions after the timeout.

## Why it matters

- No soft fork — works on Bitcoin as it exists now.
- Big reduction in on-chain footprint per onboarded user.
- Fully Lightning-compatible: payments route through the leaf channels normally;
  watchtowers protect offline clients.

## Good analogies to use

- The shared UTXO is like a group apartment lease: one contract on file (one
  on-chain entry), many tenants (clients) with private rooms (their channels).
- The timeout fallback is a "heartbeat": as long as everyone cooperates it stays
  off-chain; if the coordinator goes silent, the timeout lets people walk out.

## Where to point people next

- Original proposal: https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143
- MuSig2 (BIP-327), Decker-Wattenhofer paper, John Law's timeout-tree work.
