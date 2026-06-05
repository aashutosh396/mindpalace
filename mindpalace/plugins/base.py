"""
Plugin contract.

A plugin extends mindpalace without touching core: it can add skills, agents, gateways,
CLI commands, or hooks. Drop a plugin in `~/.mindpalace/plugins/<name>.py` (user) or ship
one in `mindpalace/plugins/contrib/` (bundled). Each defines a `Plugin` subclass; the loader
instantiates it and calls `register(app)` at startup.
"""
from __future__ import annotations


class Plugin:
    name = "unnamed"
    version = "0.1.0"
    description = ""

    def register(self, app: "PluginContext") -> None:
        """Wire the plugin in. Override this."""
        raise NotImplementedError


class PluginContext:
    """What a plugin may extend. Populated by the host at load time."""
    def __init__(self):
        self.skills_dirs: list = []     # extra skill directories
        self.agents: dict = {}          # name -> agent module/object
        self.commands: dict = {}        # cli/discord command name -> handler
        self.hooks: dict = {}           # event name -> list[callable]

    def add_skill_dir(self, path):
        self.skills_dirs.append(path)

    def add_agent(self, name, agent):
        self.agents[name] = agent

    def add_command(self, name, handler):
        self.commands[name] = handler

    def on(self, event, fn):
        self.hooks.setdefault(event, []).append(fn)
