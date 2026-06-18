class ExecutionSupervisor:

    def monitor(self, tasks):

        states = {}

        for task in tasks:

            states[
                task.task_id
            ] = task.status

        return states