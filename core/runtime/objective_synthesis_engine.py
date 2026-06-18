class ObjectiveSynthesisEngine:

    def synthesize(self, prompt, tasks):
        return {
            "prompt": prompt,
            "summary": f"Umbra synthesized {len(tasks)} runtime objectives.",
            "tasks": tasks,
        }