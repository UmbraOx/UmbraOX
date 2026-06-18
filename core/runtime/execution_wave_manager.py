class ExecutionWaveManager:

    def create_wave(
        self,
        tasks
    ):

        return {
            "wave_size": len(tasks),
            "status": "created"
        }