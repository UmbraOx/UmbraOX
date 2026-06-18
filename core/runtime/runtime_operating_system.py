from core.runtime.runtime_system_manager import (
    RuntimeSystemManager
)

from core.runtime.runtime_command_center import (
    RuntimeCommandCenter
)

from core.runtime.runtime_autonomous_cognition import (
    RuntimeAutonomousCognition
)

from core.runtime.runtime_sandbox import (
    RuntimeSandbox
)

from core.runtime.runtime_failure_manager import (
    RuntimeFailureManager
)


class RuntimeOperatingSystem:

    def __init__(self):

        self.manager = (
            RuntimeSystemManager()
        )

        self.command = (
            RuntimeCommandCenter()
        )

        self.cognition = (
            RuntimeAutonomousCognition()
        )

        self.sandbox = (
            RuntimeSandbox()
        )

        self.failures = (
            RuntimeFailureManager()
        )

    def boot(self):

        return self.command.initialize()

    def execute(self, objective):

        validation = (
            self.sandbox.validate(
                objective
            )
        )

        if not validation["safe"]:

            return {
                "blocked": True,
                "reason":
                validation["reason"]
            }

        try:

            cognition = (
                self.cognition.process(
                    objective
                )
            )

            execution = (
                self.manager.execute(
                    objective
                )
            )

            return {
                "cognition": cognition,
                "execution": execution
            }

        except Exception as e:

            return self.failures.record(e)