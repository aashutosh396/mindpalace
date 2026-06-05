"""Plugin system — extend mindpalace (skills, agents, gateways, commands, hooks) without
touching core. See loader.load() + base.Plugin. Drop user plugins in ~/.mindpalace/plugins/."""
from .loader import load  # noqa: F401
