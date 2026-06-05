---
name: connect-tailscale
description: Connect one or many computers (Macs, laptops, a company's central server) to a VPS over Tailscale for secure two-way file access (ssh/rsync). Multi-user, multi-machine. Reference recipe — derive a per-machine user skill from it.
tags: [tailscale, vpn, ssh, rsync, networking, files, vps]
created: 2026-06-05
---

# Connect computer(s) to a VPS over Tailscale

> GLOBAL reference. When you wire up a real machine, draft a tailored user skill
> (`~/.mindpalace/skills/tailscale-<machine>.md`, `derived_from: connect-tailscale`) with the
> actual Tailscale IPs, hostnames, and which dirs are shared. File the VPS + each machine in
> `infra/` and log it.

Tailscale = a WireGuard mesh. Every machine that joins the tailnet gets a stable `100.x` IP
and can reach the others directly — **no public ports opened** (all dial outbound). Ideal for:
letting people send files to the VPS, pulling files back, or hooking a **company central
server** to the VPS.

## 1. Install (each machine + the VPS)
- Linux/VPS: `curl -fsSL https://tailscale.com/install.sh | sh`
- macOS: `brew install --cask tailscale` (standalone, **not** the App Store build — you need the CLI)
- Windows: installer from tailscale.com/download

## 2. Join the tailnet (one account owns it; others are invited/shared)
- `sudo tailscale up` (Linux) or open the app (mac) → authenticate in the browser (Google/GitHub).
- Headless VPS: `tailscale up` prints a login URL — open it, approve the device.
- Confirm: `tailscale status` lists every node + its `100.x` IP.
- **Disable key expiry** for always-on nodes (admin console → Machines → ⋯ → Disable key expiry)
  so the link never drops.

## 3. Two-way access (ssh + rsync over the tailnet)
- A → B: `ssh <user>@<B-tailscale-ip>` (the target must have its SSH server / Remote Login on).
  - macOS target: System Settings → General → Sharing → **Remote Login = ON**.
- Put each source machine's SSH **public key** in the target's `~/.ssh/authorized_keys`.
- Files both ways:
  `rsync -az -e "ssh -i <key>" ~/local/dir/ <user>@<peer-ip>:~/dest/`
- A shared drop folder works well: e.g. each machine ↔ `VPS:/srv/dropbox/` (one dir, everyone rsyncs).

## 4. Multiple people / multiple computers
- Each person installs Tailscale + joins (invite them to the tailnet, or **share** specific
  machines via the admin console → Machines → Share).
- Each computer = its own node + key in the relevant `authorized_keys`. No limit for normal use.
- **Company central server → VPS:** install Tailscale on the server, `tailscale up`, then the VPS
  reaches it at its `100.x` IP (and vice-versa) for backups, syncs, or pushing builds.

## 5. Lock it down (recommended)
- Tailscale **ACLs** (admin console) restrict who/what can reach whom (e.g. only the VPS may SSH
  the central server, port 22 only).
- Scope a leaked key: in `authorized_keys`, prefix with `from="100.0.0.0/8",no-port-forwarding`.
- Keep secrets out of shared dirs; tokens belong in `secrets/`.

## Gotchas
- macOS drops the tailnet on sleep → a laptop is unreachable while asleep (use `caffeinate` if it
  must stay reachable; a server won't sleep).
- Self-ssh over a public IP that's firewalled to specific IPs can fail — use the `100.x` tailnet IP
  or `localhost`.
- One bare key with no trailing newline in `authorized_keys` will concatenate with the next — keep
  one key per line.
