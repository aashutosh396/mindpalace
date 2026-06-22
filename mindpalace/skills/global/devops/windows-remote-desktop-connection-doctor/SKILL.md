---
name: Windows App / AVD Connection Doctor (macOS)
description: Use when a Windows App / AVD / W365 / RDP connection on macOS is slow, shows WebSocket instead of UDP Shortpath, fails to establish Shortpath, or has unexpectedly high RTT — diagnoses transport selection and VPN/proxy interference.
tags: [avd, rdp, windows-app, w365, vdi, macos, shortpath, udp, websocket, stun, vpn, latency]
source: daymade/claude-code-skills
derived_from: windows-remote-desktop-connection-doctor
---

Diagnose Windows App (AVD/WVD/W365) connection quality on macOS, focused on transport optimization. AVD transport priority: **UDP Shortpath > TCP > WebSocket**. WebSocket fallback (TCP 443 via gateway) adds significant latency.

## Workflow
**Step 1 — Connection Info** (signal icon in Windows App toolbar): Transport Protocol, RTT, Bandwidth, Gateway, Service Region. If transport is `UDP`/`UDP Multicast` → optimal, stop. If `WebSocket`/`TCP` → continue.

**Step 2 — Network evidence (in parallel, no assumptions):**
- Routing/interfaces: `ifconfig | grep -E "^[a-z]|inet |utun"`, `netstat -rn | head -40`, `scutil --proxy`. Look for utun VPN tunnels, default-route priority, split routing (`0/1 + 128.0/1 → utun`), system proxy.
- RDP process/connections: `ps aux | grep -iE 'msrdc|Windows'` (new client process is "Windows"), `lsof -i UDP -n -P`. Source IP `198.18.0.x` = routed through proxy TUN; no UDP from Windows process = Shortpath not established; only TCP 443 = WebSocket fallback.
- VPN/proxy: `env | grep -i proxy`, `scutil --proxy`. Tailscale: `tailscale status`, `tailscale netcheck` (reveals NAT type, UDP support).

**Step 3 — Windows App logs (most critical).** Location: `~/Library/Containers/com.microsoft.rdc.macos/Data/Library/Logs/Windows App/`. Key patterns: `Passed: InternetConnectivity` (health OK), `STUN/TURN Traffic Routed Through VPN: Yes` (VPN intercepts negotiation), `FetchClientOptions exception: Request timed out` (**critical** — can't get transport options from gateway), `Certificate validation failed` (TLS interception/DNS poisoning). Compare a working (UDP) log vs current — broken logs may show missing health-check block or cert/timeout errors.

## Root-cause categories
- **A. VPN/proxy interference** — source IP `198.18.0.x`, STUN/TURN via VPN, no UDP. Fix: add DIRECT rules for `*.wvd.microsoft.com`, `microsoft.com`, `13.104.0.0/14` in the proxy tool; verify by temporarily disabling VPN and reconnecting.
- **B. ISP/network UDP restriction** — WebSocket even with all VPNs off, `FetchClientOptions` timeout. Verify with a STUN connectivity test to `stun.l.google.com:19302`. Fix: try mobile hotspot, check NAT type (Full Cone preferred), enable UPnP, try IPv6, contact ISP.
- **C. Client health-check failure** — cert errors at startup, missing health block. Causes: ISP HTTPS MITM, DNS poisoning, firewall on MS telemetry. Fix: DNS to 8.8.8.8/1.1.1.1, route MS traffic through a clean proxy.
- **D. Server-side Shortpath not enabled** — no STUN/TURN entries at all, health passes, no errors. Requires admin action in Azure portal.

## Verify fix
Reconnect → Transport should be `UDP`/`UDP Multicast`, RTT drops sharply, `lsof -i UDP -n -P | grep -i Windows` shows UDP connections.

> For general network-debugging methodology (falsification, layered isolation), see the debugging-network-issues skill.
