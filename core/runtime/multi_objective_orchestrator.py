class MultiObjectiveOrchestrator:

    def orchestrate(self, tasks):
        waves = []

        for index, task in enumerate(tasks):
            waves.append({
                "wave": index + 1,
                "task": task,
                "status": "queued"
            })

        return {
            "waves": waves,
            "count": len(waves)
        }