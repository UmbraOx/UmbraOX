class AgentCodeGenerator:

    def generate(
        self,
        name
    ):

        class_name = "".join(
            p.capitalize()
            for p in name.split("_")
        )

        code = f'''
class {class_name}Agent:

    def execute(self):

        print("[AGENT] running")
'''

        return {
            "path": f"core/agents/{name}.py",
            "code": code.strip()
        }