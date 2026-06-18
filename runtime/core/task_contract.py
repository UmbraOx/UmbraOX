class TaskContract:

    @staticmethod
    def create(goal, task_type="general", agent="coder"):

        return {
            "goal": goal,
            "type": task_type,
            "agent": agent,
            "status": "pending",
            "retries": 0,
            "max_retries": 3,
            "result": None,
            "error": None
        }

    @staticmethod
    def mark_running(task):
        task["status"] = "running"
        return task

    @staticmethod
    def mark_done(task, result):
        task["status"] = "done"
        task["result"] = result
        return task

    @staticmethod
    def mark_failed(task, error):
        task["status"] = "failed"
        task["error"] = error
        return task