class LiveGenerationMonitor:

    def display(
        self,
        outputs
    ):

        for output in outputs:

            print(
                "[GENERATED]",
                output
            )