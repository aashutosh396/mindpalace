# Gateways

The **terminal** is always available. **Discord** runs as a background service once configured —
both share one brain, memory, and vault, so you're reachable from either at once.

## Switch / configure
```bash
mindpalace gateway terminal
mindpalace gateway discord     # prompts for bot token + home channel id
```

## Background service (Discord / headless)
```bash
sudo mindpalace service install   # systemd (Linux) / launchd (macOS), reboot-persistent
mindpalace start | stop           # detached background without systemd
mindpalace daemon                 # run the daemon in the foreground (for your own supervisor)
```

## Discord behavior
- **Main bot, home channel:** answers every message; posts all its updates there.
- **Main bot, other channels:** answers only when `@mentioned`.
- **Scoped bots:** `@mention`-triggered anywhere; the main bot supervises ones mentioned in the
  home channel and reports when they finish.
