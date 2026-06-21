---
name: emblem-agent-wallet
description: "Use when connecting to EmblemVault to manage a multi-chain crypto wallet across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin — checking addresses, balances, portfolio snapshots, recent activity, or running operator-confirmed wallet actions. Triggers: 'use my Emblem wallet', 'connect to EmblemVault', 'create an agent wallet', 'what are my wallet addresses', 'show balances across chains'."
version: 1.0.0
license: MIT
tags: [crypto, wallet, multi-chain, web3, solana, ethereum, bitcoin, agent-wallet]
source: https://github.com/EmblemCompany/Agent-skills/tree/main/skills/emblem-ai-agent-wallet
derived_from: awesomeclaude
prerequisites: ["Node.js >= 18", "@emblemvault/agentwallet CLI (emblemai)", "internet access"]
---

# EmblemAI Agent Wallet

Wallet-aware assistant for EmblemVault. Manage balances, addresses, portfolio
snapshots, recent activity, and operator-confirmed actions across Solana,
Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. Profile-scoped local auth,
zero-config agent provisioning, review-first for any value-moving action.

## When to use
- "Use my Emblem wallet to check balances"
- "Connect to EmblemVault" / "Create or use my agent wallet profile"
- "What are my wallet addresses?" / "Show recent wallet activity"

## Security model (review-first)
- Transaction previews shown before signing; explicit user confirmation required.
- No transaction broadcast without operator approval.
- Profile isolation = separate credentials per wallet context.
- Short-lived session tokens (15-min JWT, 7-day refresh).
- Sensitive files use 0600/0700 permissions.
- Never paste passwords, seed phrases, or private keys into chat; never echo raw secrets.

## Install
```bash
npm install -g @emblemvault/agentwallet@<pinned-version>
npm audit signatures   # verify npm provenance attestations
```
Do not use `sudo`; configure a user-owned npm prefix instead. The CLI exposes
one command: `emblemai`.

## First run
1. Install the CLI.
2. Create/pick a profile: `emblemai profile create motoko`
3. Run interactive `emblemai --profile motoko` OR single-shot
   `emblemai --agent --profile motoko -m "What are my wallet addresses?"`
4. Type `/help` for all commands.
5. Back up profile auth immediately after first wallet creation.

## Profiles (multi-agent isolation)
```bash
emblemai profile list | create <name> | use <name> | inspect [name] | delete <name>
emblemai --profile <name> ...
```
Fail-closed rule: if more than one profile exists in `~/.emblemai`, every
`--agent` invocation MUST include `--profile <name>`. Agent mode never guesses.

## Authentication
**Browser auth (interactive, recommended).** Run `emblemai --profile <name>`
without `-p`; opens a modal at `127.0.0.1:18247` supporting EVM wallets
(MetaMask, WalletConnect), Solana (Phantom, Solflare), Hedera, Bitcoin (PSBT),
OAuth (Google, Twitter/X), email/password+OTP, and guest fingerprint sessions.
Use this to connect/switch an existing wallet.

**Agent mode (zero-config, password-auth only).** Resolves per profile:
1. explicit password flag / env override,
2. stored encrypted password in `~/.emblemai/profiles/<name>/.env` + `.env.keys`,
3. none present → auto-generate a 32-byte password, store encrypted, authenticate,
   create a new vault.
One command creates a working wallet:
```bash
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```

## Wallet data safety (critical)
- Logout via `/auth` → option 9 (clears the profile's `session.json`).
- NEVER `rm -rf ~/.emblemai` as a logout step.
- Never delete credential material unless the user explicitly asks to destroy it.
- The auto-generated password in `.env`/`.env.keys` is the only key to that
  wallet. Lose it without backup = wallet unrecoverable.

## Common workflows (run CLI directly; do not prompt the LLM for these)
- **Backup auth** (do this right after first wallet creation):
  `emblemai --profile motoko` → `/auth` → option 8.
- **Restore** (profile-aware; creates profile if missing):
  `emblemai --profile motoko --restore-auth ~/emblemai-auth-backup.json`
- **Switch wallet / re-login**: logout via CLI flow, then relaunch
  `emblemai --profile <name>` and pick a provider in the modal.
- **Check wallet/session**: `/wallet`, or `/auth` → 2 (Vault Info), 3 (Session Info).

## Usage patterns
Single-shot agent query:
```bash
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```
Interactive session for multi-step or provider switching:
```bash
emblemai --profile motoko
```
