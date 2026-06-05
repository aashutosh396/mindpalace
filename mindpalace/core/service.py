"""
Daemon process management — run the background daemon detached, check it, stop it,
and (optionally) install it as a real OS service so it survives reboots.

  spawn()        start the daemon detached (used automatically by the terminal)
  is_running()   pid alive?
  stop()         stop it
  install()      systemd --user unit (Linux) / launchd agent (macOS)
  uninstall()    remove the service
"""
from __future__ import annotations

import os
import platform
import subprocess
import sys

from .. import config


def _pidfile():
    return config.state_dir() / "daemon.pid"


def running_pid():
    """Live daemon PID from the pidfile, or None."""
    pf = _pidfile()
    if not pf.exists():
        return None
    try:
        pid = int(pf.read_text().strip())
        os.kill(pid, 0)
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        return None


def is_running() -> bool:
    return running_pid() is not None


def spawn() -> bool:
    """Start the daemon detached (new session) so it outlives the terminal. Idempotent."""
    if is_running():
        return False
    config.ensure_dirs()
    log = open(config.logs_dir() / "daemon.log", "a")
    p = subprocess.Popen(
        [sys.executable, "-m", "mindpalace.cli", "daemon"],
        stdout=log, stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL, start_new_session=True,
        env={**os.environ, "MINDPALACE_HOME": str(config.home())})
    _pidfile().write_text(str(p.pid))
    return True


def stop() -> bool:
    pf = _pidfile()
    if not is_running():
        pf.unlink(missing_ok=True)
        return False
    pid = int(pf.read_text().strip())
    try:
        os.kill(pid, 15)
    except ProcessLookupError:
        pass
    pf.unlink(missing_ok=True)
    return True


# ---- OS service install (reboot-persistent) ----
def _path_env() -> str:
    # systemd has a minimal PATH; make sure `claude` (often ~/.local/bin) is reachable.
    extra = os.path.expanduser("~/.local/bin")
    return f"{extra}:/usr/local/bin:/usr/bin:/bin"


def install() -> str:
    py = sys.executable
    home = str(config.home())
    if platform.system() == "Linux":
        body = (
            "[Unit]\nDescription=mindpalace daemon\nAfter=network-online.target\n\n"
            f"[Service]\nEnvironment=MINDPALACE_HOME={home}\nEnvironment=PATH={_path_env()}\n"
            f"ExecStart={py} -m mindpalace.cli daemon\nRestart=always\nRestartSec=5\n")
        if os.geteuid() == 0:
            # SYSTEM service — best for a headless VPS: survives reboot, no login needed.
            unit = "/etc/systemd/system/mindpalace.service"
            with open(unit, "w") as f:
                f.write(body + "\n[Install]\nWantedBy=multi-user.target\n")
            subprocess.run(["systemctl", "daemon-reload"], check=False)
            subprocess.run(["systemctl", "enable", "--now", "mindpalace"], check=False)
            return (f"installed SYSTEM service: {unit}\n"
                    "started + enabled. survives reboot. logs: `journalctl -u mindpalace -f`.\n"
                    "stop: `systemctl stop mindpalace` · status: `systemctl status mindpalace`")
        unit_dir = os.path.expanduser("~/.config/systemd/user")
        os.makedirs(unit_dir, exist_ok=True)
        unit = os.path.join(unit_dir, "mindpalace.service")
        with open(unit, "w") as f:
            f.write(body + "\n[Install]\nWantedBy=default.target\n")
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
        subprocess.run(["systemctl", "--user", "enable", "--now", "mindpalace"], check=False)
        return (f"installed systemd --user unit: {unit}\n"
                "to survive logout/reboot: `loginctl enable-linger $USER`\n"
                "logs: `journalctl --user -u mindpalace -f`")
    if platform.system() == "Darwin":
        plist = os.path.expanduser("~/Library/LaunchAgents/com.mindpalace.daemon.plist")
        with open(plist, "w") as f:
            f.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
                '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
                '<plist version="1.0"><dict>\n'
                '  <key>Label</key><string>com.mindpalace.daemon</string>\n'
                f'  <key>ProgramArguments</key><array><string>{py}</string>'
                '<string>-m</string><string>mindpalace.cli</string><string>daemon</string></array>\n'
                f'  <key>EnvironmentVariables</key><dict><key>MINDPALACE_HOME</key><string>{home}</string></dict>\n'
                '  <key>RunAtLoad</key><true/>\n  <key>KeepAlive</key><true/>\n'
                f'  <key>StandardErrorPath</key><string>{config.logs_dir()}/daemon.log</string>\n'
                '</dict></plist>\n')
        subprocess.run(["launchctl", "unload", plist], check=False, capture_output=True)
        subprocess.run(["launchctl", "load", plist], check=False)
        return f"installed launchd agent: {plist}"
    return "unsupported OS — run `mindpalace daemon` under your own supervisor."


def uninstall() -> str:
    if platform.system() == "Linux":
        if os.geteuid() == 0:
            subprocess.run(["systemctl", "disable", "--now", "mindpalace"], check=False)
            unit = "/etc/systemd/system/mindpalace.service"
            if os.path.exists(unit):
                os.remove(unit)
            subprocess.run(["systemctl", "daemon-reload"], check=False)
            return "removed SYSTEM service"
        subprocess.run(["systemctl", "--user", "disable", "--now", "mindpalace"], check=False)
        unit = os.path.expanduser("~/.config/systemd/user/mindpalace.service")
        if os.path.exists(unit):
            os.remove(unit)
        return "removed systemd --user unit"
    if platform.system() == "Darwin":
        plist = os.path.expanduser("~/Library/LaunchAgents/com.mindpalace.daemon.plist")
        subprocess.run(["launchctl", "unload", plist], check=False, capture_output=True)
        if os.path.exists(plist):
            os.remove(plist)
        return "removed launchd agent"
    return "nothing to remove"
