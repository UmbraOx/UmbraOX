from core.model import ask_llm

class ArchitectAgent:

    def run(self, task):

        prompt = f"""
You are Umbra Software Architect.

Design systems, file structures, and architecture.

TASK:
{task}
"""

        return ask_llm(prompt)