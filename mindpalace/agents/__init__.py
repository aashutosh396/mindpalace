"""
Cognitive agents — background workers that make mindpalace smarter.

Today: the Analyst (reflect after each task + review on heartbeat). Tomorrow: more
(researcher, maintainer, etc). Each agent is a module exposing async entry points and
(optionally) subclassing agents.base.Agent. Register new agents in AGENTS below.
"""
from . import analyst  # noqa: F401

AGENTS = {"analyst": analyst}
