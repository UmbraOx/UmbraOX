from core.runtime.feature_intake import (
    FeatureIntake
)

from core.runtime.runtime_loop import (
    RuntimeLoop
)

from core.runtime.autonomy_loop import (
    start_autonomy_loop
)


class BossAgent:

    def __init__(self):

        self.feature_intake = (
            FeatureIntake()
        )

        self.runtime_loop = (
            RuntimeLoop()
        )

        self.runtime_loop.start()

        start_autonomy_loop()

    def run(self, prompt):

        try:

            response = (
                self.feature_intake.process(
                    prompt
                )
            )

            print(response)

        except Exception as e:

            print(
                f"[BOSS ERROR] {e}"
            )