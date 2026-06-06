"""
`mindpalace` — the one command.

  mindpalace            first run → setup; then terminal chat (auto-starts the bg daemon)
  mindpalace setup      re-run onboarding
  mindpalace gateway discord|terminal   configure/switch interface
  mindpalace daemon     run the background daemon in the FOREGROUND (for systemd/launchd)
  mindpalace stop       stop the background daemon
  mindpalace service install|uninstall|status   install as a reboot-persistent OS service
  mindpalace add-bot / bots             scoped bots
  mindpalace add-admin <id> / admins / remove-admin <id>
  mindpalace add-webhook <name> <url> / notify "msg"
  mindpalace status / version
"""
import sys

from . import config, __version__


def _status():
    print(f"mindpalace {__version__}")
    print(f"  data home : {config.home()}")
    if config.is_initialized():
        from .core import service, daemon
        print(f"  identity  : {'yes' if config.USER_FILE().exists() else 'no'}")
        print(f"  discord   : {'configured' if daemon.discord_configured() else 'not configured'}")
        print(f"  daemon    : {'running' if service.is_running() else 'stopped'}")
        hb = config.heartbeat_minutes()
        print(f"  heartbeat : {'every ' + str(hb) + ' min' if hb else 'off'}")
        print(f"  concurrency: {config.concurrency()} parallel agents")
        print("  terminal  : always available (`mindpalace`)")
    else:
        print("  (not initialized — run `mindpalace` to set up)")


def _run():
    config.ensure_dirs()        # idempotent — creates vault etc. for existing installs
    from .core import service, daemon
    # Discord (if configured) runs as a BACKGROUND service so the terminal stays free.
    if daemon.discord_configured():
        if service.spawn():
            print("✅ Discord live in the background — you can chat there too.")
        elif service.is_running():
            print("✅ Discord daemon already running in the background.")
    # The terminal chat is ALWAYS available.
    from .gateways import terminal
    terminal.run()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else ""

    if cmd in ("version", "-v", "--version"):
        print(__version__); return
    if cmd in ("status", "-s"):
        _status(); return
    if cmd == "setup":
        from . import setup
        setup.run(); return
    if cmd == "gateway" or cmd in ("discord", "terminal"):
        target = (argv[1] if cmd == "gateway" and len(argv) > 1 else
                  cmd if cmd in ("discord", "terminal") else "")
        from . import setup
        cfg = config.load_config()
        if target == "discord":
            if not config.read_secret("bot_main.token"):
                cfg.update(setup._discord_gateway())     # asks token + home channel
            cfg["gateway"] = "discord"
            config.save_config(cfg)
            print("✅ Discord configured — it runs in the BACKGROUND.")
            print("   `mindpalace` → terminal chat (auto-starts the bot); chat from Discord too.")
            print("   `mindpalace service install` → keep it running across reboots.")
        elif target == "terminal":
            cfg["gateway"] = "terminal"; config.save_config(cfg)
            print("gateway → terminal. (Discord, if configured, still runs in the background.)")
        else:
            print("usage: mindpalace gateway <terminal|discord>")
        return
    if cmd in ("add-bot", "addbot"):
        from . import bots
        bots.add_bot_interactive(); return
    if cmd == "bots":
        from . import bots
        reg = bots.registry()
        if not reg:
            print("no bots yet — `mindpalace add-bot` to add one (main is created at setup).")
        for name, b in reg.items():
            print(f"  {name:14} {b.get('permissions','?'):9} trigger={b.get('trigger','?')}")
        return

    # --- admin management (local terminal is trusted; gates remote/Discord use) ---
    if cmd == "admins":
        a = config.admins()
        print("admins:", a or "(none — first to chat is allowed until you add one)")
        return
    if cmd == "add-admin":
        if len(argv) < 2:
            print("usage: mindpalace add-admin <discord-user-id>"); return
        print("added" if config.add_admin(argv[1]) else "already an admin"); return
    if cmd == "remove-admin":
        if len(argv) < 2:
            print("usage: mindpalace remove-admin <discord-user-id>"); return
        print("removed" if config.remove_admin(argv[1]) else "not an admin"); return
    if cmd == "add-webhook":
        if len(argv) < 3:
            print("usage: mindpalace add-webhook <name> <discord-webhook-url>"); return
        config.set_webhook(argv[1], argv[2]); print(f"webhook '{argv[1]}' saved"); return
    if cmd == "notify":
        from .core import notify
        notify.main(argv[1:]); return
    if cmd == "concurrency":
        if len(argv) > 1 and argv[1].isdigit():
            cfg = config.load_config(); cfg["concurrency"] = max(1, int(argv[1]))
            config.save_config(cfg)
            print(f"concurrency = {cfg['concurrency']} parallel agents (restart the daemon to apply)")
        else:
            print(f"concurrency: {config.concurrency()} parallel agents  ·  set with `mindpalace concurrency <n>`")
        return
    if cmd == "heartbeat":
        if len(argv) > 1 and argv[1].isdigit():
            cfg = config.load_config(); cfg["heartbeat_minutes"] = int(argv[1])
            config.save_config(cfg)
            print(f"autonomous heartbeat every {argv[1]} min" if int(argv[1]) > 0 else "heartbeat off")
            print("(restart the daemon for it to take effect)")
        else:
            print(f"heartbeat: {config.heartbeat_minutes()} min  ·  set with `mindpalace heartbeat <minutes>` (0 = off)")
        return

    # --- self-update (git) ---
    if cmd == "update-interval":
        if len(argv) > 1 and argv[1].isdigit():
            cfg = config.load_config(); cfg["update_check_minutes"] = int(argv[1])
            config.save_config(cfg)
            print(f"update check every {argv[1]} min" if int(argv[1]) > 0 else "update checks off")
            print("(restart the daemon for it to take effect)")
        else:
            from .core import updater
            print(f"update check: {updater.interval_minutes()} min  ·  "
                  "set with `mindpalace update-interval <minutes>` (0 = off)")
        return
    if cmd == "update":                         # manual: pull now + restart
        from .core import updater
        info = updater.check()
        if not info:
            print("already up to date."); return
        print(f"{info['behind']} new change(s):")
        for s in info["log"]:
            print(f"  • {s}")
        print(updater.accept())
        return
    if cmd == "restart":
        from .core import service
        service.stop(); service.spawn(); print("daemon restarted."); return

    # --- background daemon (discord bot + job watcher) ---
    if cmd == "daemon":                         # foreground; run by systemd/launchd or spawned
        from .core import daemon
        daemon.run(); return
    if cmd == "start":                          # detached background, no terminal (no systemd)
        from .core import service
        if service.is_running():
            print("already running"); return
        service.spawn(); print("daemon started in background. `mindpalace stop` to halt."); return
    if cmd in ("stop", "daemon-stop"):
        from .core import service
        print("stopped" if service.stop() else "not running"); return
    if cmd == "service":
        from .core import service
        sub = argv[1] if len(argv) > 1 else "status"
        if sub == "install":
            print(service.install())
        elif sub == "uninstall":
            print(service.uninstall())
        else:
            print("daemon running" if service.is_running() else "daemon stopped")
        return
    if cmd in ("help", "-h", "--help"):
        print(__doc__); return

    # default: first-run setup, then start
    if not config.is_initialized():
        from . import setup
        setup.run()
    _run()


if __name__ == "__main__":
    main()
