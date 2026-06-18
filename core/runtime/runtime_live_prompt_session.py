from core.runtime.runtime_prompt_runtime import RuntimePromptRuntime
from core.runtime.runtime_response_formatter import RuntimeResponseFormatter


class RuntimeLivePromptSession:
    def __init__(self):
        self.runtime = RuntimePromptRuntime()
        self.formatter = RuntimeResponseFormatter()

    def run_prompt(self, prompt: str):
        result = self.runtime.submit_prompt(prompt)

        return self.formatter.format(result)