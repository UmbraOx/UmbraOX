class RuntimeTaskState:

    def create(
        self,
        objective,
        worker
    ):

        return {
            "objective": objective,
            "worker": worker,
            "status": "queued"
        }

    def complete(
        self,
        task
    ):

        task["status"] = "completed"

        return task