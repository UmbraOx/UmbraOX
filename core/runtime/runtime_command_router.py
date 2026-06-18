class RuntimeCommandRouter:

    def route(self, prompt):
        prompt = prompt.lower()

        if "gui" in prompt:
            return "ui"

        if "agent" in prompt:
            return "agents"

        if "deploy" in prompt:
            return "deployment"

        return "runtime"