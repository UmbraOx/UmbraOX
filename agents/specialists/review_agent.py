from core.model import ask_llm

class ReviewAgent:

    def run(self, task):

        prompt = f"""
You are Umbra Review Agent.

Review code and plans for:
- bugs
- bad architecture
- security problems
- performance issues

TASK:
{task}
"""

        return ask_llm(prompt)