from uuid import uuid4
from datetime import datetime, UTC


class RuntimeExecutionContext:

    def __init__(
        self,
        objective
    ):

        self.id = str(
            uuid4()
        )

        self.objective = (
            objective
        )

        self.created = (
            datetime.now(UTC)
            .isoformat()
        )

        self.status = (
            "initialized"
        )

        self.logs = []

    def update_status(
        self,
        status
    ):

        self.status = status

    def log(
        self,
        message
    ):

        self.logs.append(
            message
        )

    def export(self):

        return {
            "id": self.id,
            "objective": (
                self.objective
            ),
            "created": (
                self.created
            ),
            "status": (
                self.status
            ),
            "logs": self.logs
        }