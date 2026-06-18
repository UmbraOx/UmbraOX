class ExecutionWaveEngine:

    def generate(
        self,
        phases
    ):

        waves = []

        for index, phase in enumerate(
            phases,
            start=1
        ):

            waves.append({
                "wave": index,
                "objective": phase
            })

        return waves