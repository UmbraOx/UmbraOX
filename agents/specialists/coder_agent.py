from agents.base_agent import BaseAgent

from core.tool_router import ToolRouter
from core.plugin_registry import PluginRegistry


class CoderAgent(BaseAgent):

    def __init__(self):

        super().__init__("coder")

        self.router = ToolRouter()

        self.plugins = PluginRegistry()

    def execute(self, task, plan=None):

        print(f"[CODER] Task: {task}")

        if plan:

            result = self.router.run_plan(plan)

            print(f"[CODER] Execution result: {result}")

        return True