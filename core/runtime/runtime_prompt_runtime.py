from core.runtime.runtime_autonomous_brain import RuntimeAutonomousBrain


class RuntimePromptRuntime:
    def __init__(self):
        self.brain = RuntimeAutonomousBrain()
        self.prompt_history = []

    def submit_prompt(self, prompt: str):
        result = self.brain.execute_objective(prompt)

        self.prompt_history.append({
            "prompt": prompt,
            "result": result
        })

        return result

    def get_prompt_history(self):
        return self.prompt_history