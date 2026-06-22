---
name: Tunnel Doctor (Tailscale ⨯ proxy/VPN conflicts, macOS)
description: Use when Tailscale coexists with a proxy/VPN (Shadowrocket/Clash/Surge/OrbStack) on macOS and connectivity breaks — tailscale ping works but SSH/HTTP times out, browser 503 but curl works, git push "failed to begin relaying via HTTP", docker pull/build timeouts, or ~60s DNS-resolution stalls.
tags: [tailscale, proxy, vpn, macos, ssh, dns, shadowrocket, clash, docker, no_proxy, tun, networking]
source: daymade/claude-code-skills
derived_from: tunnel-doctor
---

Diagnose and fix conflicts when Tailscale coexists with proxy/VPN tools on macOS. (General diagnostic discipline lives in debugging-network-issues; this is the macOS Tailscale⨯proxy domain layer.)

## Five conflict layers
| Layer | Breaks | Still works | Root cause |
|-------|--------|-------------|------------|
| 1. Route table | Everything | `tailscale ping` | proxy adds `en0` route overriding Tailscale utun |
| 2. HTTP env vars | curl, Python/Node fetch | SSH, browser | `http_proxy` set without `NO_PROXY` for Tailscale |
| 3. System proxy | Browser (503) | SSH, curl | DIRECT rule routes via Wi-Fi not utun |
| 4. SSH ProxyCommand double tunnel | git push/pull | `ssh -T` | `connect -H` redundant with Shadowrocket TUN |
| 5. VM/container proxy | docker pull/build | host curl | OrbStack/Docker injects/caches proxy config |

## Symptom → step
- `tailscale ping` works, SSH/TCP times out → route conflict (2B).
- ping works, curl/HTTP times out → HTTP env var (2A).
- browser 503, curl+SSH work → system proxy bypass (2C).
- git push fails `failed to begin relaying via HTTP` → SSH double tunnel (2F).
- `git clone` `Connection closed by 198.18.x.x` → TUN DNS hijack (2H).
- docker build `RUN apk/apt` Connection refused instantly → OrbStack transparent proxy + TUN (fix: `--network host`).
- docker pull TLS handshake timeout → VM proxy misconfig (fix: docker.json with `host.internal`).
- ssh/curl/git hang ~60s before resolving but `nslookup` instant → stalled resolver chain (2I).

## Diagnosis discipline
Don't commit to a hypothesis from circumstantial evidence — verify with the component's own health check first: HTTP proxy `curl -x http://127.0.0.1:<port> -m 10 https://api.github.com`; Tailscale `tailscale status`; a DNS resolver `dig @<ns> +tries=1 +timeout=3 example.com`; routing `route -n get <ip>`. If DNS is involved at all, run the per-nameserver bisection (2I) first — it rules in/out the largest class of macOS-on-China failures in <15s.

**TUN measurement contamination:** in TUN/global mode, probes lie. `nc -z` `0.00s` to an overseas host = you hit the local TUN, not the node (light alone is tens of ms). `ping` near-zero loss, `curl -w %{remote_ip}` (always loopback), and foreign IP-geo (reports exit IP) are all fabricated. Trust `time_appconnect`/`time_starttransfer`, an in-region IP-geo source, and the decoded proxy config + GUI. Ask "is this number physically possible if the packet really traversed?"

## Key fixes
- **2A NO_PROXY:** `export NO_PROXY=localhost,127.0.0.1,.ts.net,100.64.0.0/10,192.168.*,10.*,172.16.*`. Go's `net/http` ignores CIDR in NO_PROXY — use MagicDNS hostnames or explicit IPs for Go tools.
- **2C system proxy:** add `100.64.0.0/10` to `skip-proxy` in the proxy tool (NOT `tun-excluded-routes` — that adds a competing en0 route and breaks everything).
- **2D auth redirect to localhost:** SSH local forward `ssh -NL 3010:localhost:3010 <tailscale-ip>` (or autossh) — avoids all conflict layers, no .env change.
- **2F git push:** remove `ProxyCommand`, switch to `ssh.github.com:443`.
- **2G docker:** build → `--network host`; pull → `~/.orbstack/config/docker.json` with `http-proxy: host.internal:<port>` + `no-proxy` including `host.internal`; clear BOTH uppercase AND lowercase proxy env vars in containers (healthcheck wget uses lowercase).
- **2H DNS hijack:** pin GitHub SSH IP in `~/.ssh/config` (`HostName 140.82.112.35`, `Port 443`) or add IP-CIDR DIRECT rules.
- **2I stalled resolver:** bisect with `for ns in <each>; do dig @$ns +tries=1 +timeout=3 ...; done` (dead one returns after exactly ~3s). `ping <resolver-ip>` can succeed while port 53 is dead (utun answers ICMP locally) — test the service, not ICMP. Fix by restarting the owning app (`osascript -e 'quit app "Tailscale"' && sleep 3 && open -a Tailscale`) so its cleanup runs — flushing DNS cache does NOT remove the dead resolver from `scutil --dns`.

## Universal rule
Add to any proxy tool: `IP-CIDR,100.64.0.0/10,DIRECT` and `IP-CIDR,fd7a:115c:a1e0::/48,DIRECT`. Verify `route -n get <tailscale-ip>` shows Tailscale's utun (MTU 1280), not en0 or Shadowrocket's utun (MTU 4064).
