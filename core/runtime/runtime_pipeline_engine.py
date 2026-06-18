class RuntimePipelineEngine:
    def run(self, stages):
        results = []

        for stage in stages:
            results.append({
                "stage": stage,
                "status": "completed",
            })

        return results