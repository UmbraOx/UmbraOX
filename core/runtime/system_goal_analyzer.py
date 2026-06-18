class SystemGoalAnalyzer:

    def analyze(self, prompt: str):
        prompt = prompt.lower()

        scale = "small"

        if "operating system" in prompt:
            scale = "massive"
        elif "studio" in prompt:
            scale = "large"
        elif "runtime" in prompt:
            scale = "medium"

        return {
            "scale": scale,
            "autonomous": "autonomous" in prompt,
            "multi_agent": "agent" in prompt,
            "gui": "gui" in prompt or "desktop" in prompt,
        }