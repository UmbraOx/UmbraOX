class RuntimeExecutionController:

    def execute(self, pipeline):
        completed = []

        for stage in pipeline:
            completed.append({
                "stage": stage["stage"],
                "status": "completed"
            })

        return completed