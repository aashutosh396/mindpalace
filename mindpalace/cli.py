"""
`mindpalace` — the one command.

  mindpalace            first run → setup; then terminal chat (auto-starts the bg daemon)
  mindpalace setup      re-run onboarding
  mindpalace gateway discord|terminal   configure/switch interface
  mindpalace whatsapp setup   configure WhatsApp Cloud API; `mindpalace whatsapp` runs the webhook (VPS)
  mindpalace goal "<task>"   ralph-wiggum loop: iterate until done (--max N, --until PROMISE)
  mindpalace daemon     run the background daemon in the FOREGROUND (for systemd/launchd)
  mindpalace stop       stop the background daemon
  mindpalace service install|uninstall|status   install as a reboot-persistent OS service
  mindpalace add-bot / bots             scoped bots
  mindpalace add-admin <id> / admins / remove-admin <id>
  mindpalace add-webhook <name> <url> / notify "msg"
  mindpalace status / version
  mindpalace usage [N]  per-turn session-continuity + token stats for the last N turns (soak view)
  mindpalace voice lean|full   switch reply style (brief vs chatty); applies on the next message
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
    if cmd == "whatsapp":
        sub = argv[1] if len(argv) > 1 else "run"
        if sub == "setup":
            def ask(p, d=""):
                try:
                    v = input(p).strip()
                except EOFError:
                    v = ""
                return v or d
            print("\n=== WhatsApp Cloud API setup ===")
            print("From Meta (developers.facebook.com → your app → WhatsApp → API Setup):")
            cfg = config.load_config(); wa = cfg.setdefault("whatsapp", {})
            pid = ask("Phone number ID: ")
            if pid:
                wa["phone_id"] = pid
            tok = ask("Access token (permanent recommended): ")
            if tok:
                config.write_secret("whatsapp_token", tok)
            vt = ask(f"Verify token (you choose; default 'mindpalace'): ", "mindpalace")
            wa["verify_token"] = vt
            sec = ask("App secret (optional, for signature checks; Enter to skip): ")
            if sec:
                config.write_secret("whatsapp_app_secret", sec)
            port = ask("Port to listen on (default 8080): ", "8080")
            wa["port"] = int(port) if port.isdigit() else 8080
            config.save_config(cfg)
            print("\n✓ saved. Now, on the VPS:")
            print(f"   1) run:  mindpalace whatsapp")
            print(f"   2) Meta → WhatsApp → Configuration → Webhook:")
            print(f"        Callback URL:  https://<your-host>/webhook")
            print(f"        Verify token:  {vt}")
            print(f"      then Subscribe to the 'messages' field.")
            print("   3) Message your number from WhatsApp — first sender becomes the owner.\n")
            return
        if not config.whatsapp_configured():
            print("WhatsApp not configured — run `mindpalace whatsapp setup` first."); return
        from .gateways import whatsapp
        whatsapp.run(); return

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
    if cmd == "model":
        if len(argv) > 1:
            val = config.set_main_model(argv[1])
            print(f"model = {val} (effective next reply)" if val
                  else "invalid — use sonnet|opus|haiku|<full-id>|default")
        else:
            print(f"model: {config.main_model() or '(CLI default)'}  ·  power: {config.power_model()}  ·  background: {config.background_model()}")
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

    if cmd == "voice":                          # A/B switch: lean (brief) vs full (chatty) replies
        sub = argv[1].lower() if len(argv) > 1 else ""
        if sub in ("lean", "brief", "terse", "on"):
            cfg = config.load_config(); cfg["lean_voice"] = True; config.save_config(cfg)
            from .core import brain
            brain.reset_sessions()
            print("voice → lean (brief, to-the-point). Applies on your next message.")
        elif sub in ("full", "chatty", "rich", "verbose", "off"):
            cfg = config.load_config(); cfg["lean_voice"] = False; config.save_config(cfg)
            from .core import brain
            brain.reset_sessions()
            print("voice → full (chatty, high-personality). Applies on your next message.")
        else:
            print(f"voice: {'lean' if config.lean_voice() else 'full'}  ·  "
                  "switch with `mindpalace voice lean|full` (takes effect on the next message)")
        return

    if cmd == "usage":                          # soak dashboard — session continuity + token stats
        from .core import telemetry
        n = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 50
        print(telemetry.summarize(n)); return

    if cmd == "mcp":                            # MCP server registry — catalog + enable/disable
        from . import mcp as reg
        sub = argv[1].lower() if len(argv) > 1 else "list"
        en = reg.enabled()
        if sub in ("list", "ls"):
            print(f"MCP catalog ({len(reg.catalog())} servers) — ✓ = enabled:")
            for c in reg.catalog():
                mark = "✓" if c["slug"] in en else " "
                need = (" [needs: " + ",".join(reg.missing_env(c["slug"])) + "]") if (c["slug"] in en and reg.missing_env(c["slug"])) else ""
                print(f"  {mark} {c['slug']:18} {c['category']:13} {c['description'][:54]}{need}")
            print("\n  mindpalace mcp enable <slug> [KEY=val ...] | disable <slug> | info <slug>")
            return
        if sub == "info":
            c = reg.get(argv[2]) if len(argv) > 2 else None
            if not c:
                print("usage: mindpalace mcp info <slug>"); return
            import json as _j
            print(f"{c['name']} ({c['slug']}) — {c['category']}\n{c['description']}\nenv: {c['env'] or 'none'}\n"
                  f"homepage: {c['homepage']}\nconfig:\n{_j.dumps(c['config'], indent=2)}")
            return
        if sub == "enable":
            if len(argv) < 3:
                print("usage: mindpalace mcp enable <slug> [KEY=val ...]"); return
            slug = argv[2].lower()
            kv = {}
            for tok in argv[3:]:
                if "=" in tok:
                    k, v = tok.split("=", 1); kv[k] = v
            if not reg.enable(slug, kv or None):
                print(f"no such server '{slug}' — see `mindpalace mcp list`"); return
            miss = reg.missing_env(slug)
            print(f"enabled '{slug}'." + (f" still needs creds: {', '.join(miss)} "
                  f"→ `mindpalace mcp enable {slug} {miss[0]}=...`" if miss else " ready."))
            print("(restart the daemon to wire it into running turns: mindpalace restart)")
            return
        if sub == "disable":
            if len(argv) < 3:
                print("usage: mindpalace mcp disable <slug>"); return
            reg.disable(argv[2].lower()); print(f"disabled '{argv[2].lower()}'."); return
        print("usage: mindpalace mcp [list | info <slug> | enable <slug> [KEY=val] | disable <slug>]"); return

    if cmd == "goal":                               # ralph-wiggum loop: grind a task until done
        rest, mx, promise, parts = argv[1:], None, None, []
        i = 0
        while i < len(rest):
            if rest[i] == "--max" and i + 1 < len(rest):
                mx = int(rest[i + 1]) if rest[i + 1].isdigit() else None; i += 2
            elif rest[i] == "--until" and i + 1 < len(rest):
                promise = rest[i + 1]; i += 2
            else:
                parts.append(rest[i]); i += 1
        task = " ".join(parts).strip()
        if not task:
            print('usage: mindpalace goal "<task>" [--max N] [--until PROMISE]'); return
        import asyncio
        from .core import goal

        async def _prog(line):
            print(f"  {line}")
        res = asyncio.run(goal.run_goal(task, _prog, promise=promise or goal.DEFAULT_PROMISE, max_iter=mx))
        print(f"\n{'✅ goal done' if res['done'] else '⚠️ stopped at cap'} after "
              f"{res['iterations']} iteration(s):\n")
        print(res["result"])
        return

    if cmd == "project":                            # active project → claude understands it (--add-dir)
        if len(argv) > 1:
            arg = argv[1]
            if arg in ("none", "clear", "off"):
                config.set_active_project("")
                print("active project cleared — vault only.")
            else:
                p = config.set_active_project(arg)
                import os as _os
                ok = _os.path.isdir(p)
                print(f"active project → {p}" + ("" if ok else "  ⚠️ (path not found yet)"))
                print("  claude now loads its CLAUDE.md + MCP from anywhere; cwd stays the vault.")
        else:
            print(f"active project: {config.active_project() or '(none — vault only)'}  ·  "
                  "set with `mindpalace project <path>` · clear with `mindpalace project none`")
        return

    if cmd == "workspace":
        if len(argv) > 1:                           # set + confirm a permanent workspace
            d = config.set_workspace(argv[1])
            print(f"workspace set to {d} (project code lives here)")
        else:
            d = config.workspace_dir()
            tag = "confirmed" if config.workspace_confirmed() else "default (not yet confirmed)"
            print(f"workspace: {d}  ·  {tag}  ·  set with `mindpalace workspace <path>`")
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

    if cmd in ("halt", "stop-task", "abort"):       # EMERGENCY STOP — kill running work, keep daemon
        from .core import service
        pid = service.running_pid()
        if not pid:
            print("daemon not running — nothing to halt."); return
        n = service.kill_descendants(pid)
        print(f"🛑 halted {n} running process(es) — daemon still up." if n else "nothing was running.")
        return

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
