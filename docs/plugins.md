# Plugins

Extend mindpalace without forking. A plugin can add skills, agents, gateways, commands, or hooks.

- **Bundled:** `mindpalace/plugins/contrib/*.py`
- **User:** `~/.mindpalace/plugins/*.py` (private, per-instance)

```python
from mindpalace.plugins.base import Plugin

class HelloPlugin(Plugin):
    name = "hello"
    def register(self, ctx):
        ctx.add_skill_dir("/path/to/skills")
        ctx.add_command("hello", lambda *a: print("hi"))
```
The loader finds every `Plugin` subclass and calls `register(ctx)` at startup. See
`mindpalace/plugins/base.py` for the full `ctx` surface.
