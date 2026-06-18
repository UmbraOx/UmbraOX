class RuntimePromptPipeline:

    def process(
        self,
        prompt
    ):
        return {
            "prompt": prompt,
            "normalized": prompt.lower().strip()
        }