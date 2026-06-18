class RecursiveExecutionWaveSystem:

    def execute(
        self,
        waves
    ):

        results = []

        for wave in waves:

            results.append({
                "wave": wave["wave"],
                "status": "completed"
            })

        return results