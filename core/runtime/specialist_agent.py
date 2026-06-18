from core.runtime.worker_agent import (
    WorkerAgent
)


class SpecialistAgent(
    WorkerAgent
):

    def __init__(
        self,
        name,
        specialty
    ):

        super().__init__(name)

        self.specialty = specialty

    def execute(
        self,
        task
    ):

        result = super().execute(task)

        result["specialty"] = (
            self.specialty
        )

        return result