"""
Plugin loader — discovers + loads plugins from two places:
  • bundled : mindpalace/plugins/contrib/*.py
  • user    : ~/.mindpalace/plugins/*.py   (per-instance, never in the core repo)

Each .py module should define a `Plugin` subclass. The loader instantiates each and calls
`register(ctx)`, returning a populated PluginContext the host can consult.
"""
from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

from .. import config
from .base import Plugin, PluginContext


def _dirs():
    bundled = Path(__file__).resolve().parent / "contrib"
    user = config.home() / "plugins"
    return [d for d in (bundled, user) if d.exists()]


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"mp_plugin_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load() -> PluginContext:
    ctx = PluginContext()
    for d in _dirs():
        for path in sorted(d.glob("*.py")):
            if path.name.startswith("_"):
                continue
            try:
                mod = _load_module(path)
                for _, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, Plugin) and obj is not Plugin:
                        obj().register(ctx)
                        print(f"plugin loaded: {path.stem}")
            except Exception as e:
                print(f"plugin {path.name} failed: {e}")
    return ctx
