# Plugins

Extend mindpalace without forking it. A plugin can add **skills**, **agents**, **gateways**,
**commands**, or **hooks**.

## Where they live
- **Bundled:** `mindpalace/plugins/contrib/*.py` (ship with the core).
- **User:** `~/.mindpalace/plugins/*.py` (per-instance, private, never in the repo).

## Write one
```python
from mindpalace.plugins.base import Plugin

class HelloPlugin(Plugin):
    name = "hello"
    description = "adds a skills dir + a command"

    def register(self, ctx):
        ctx.add_skill_dir("/path/to/my/skills")
        ctx.add_command("hello", lambda *a: print("hi"))
```
The loader finds every `Plugin` subclass in those folders, instantiates it, and calls
`register(ctx)` at startup. See `base.py` for everything `ctx` exposes.
