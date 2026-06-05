"""
Base for cognitive agents.

An agent = a focused role layered on the shared brain (full operating context: doctrine,
vault rules, skills, capabilities). Subclass for new agents; give it a `name` + `role`,
then call `.run(task)`. The Analyst is the first; more can follow the same shape.
"""
from __future__ import annotations

from ..core import brain


class Agent:
    name = "agent"
    role = ""                      # appended to the shared system prompt

    def system(self) -> str:
        return brain.system_prompt() + (("\n\n" + self.role) if self.role else "")

    async def run(self, task: str, permissions: str = "full") -> str:
        return await brain.ask_async(task, [], system=self.system(), permissions=permissions)
