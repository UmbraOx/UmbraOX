import uuid
from core.runtime.umbra_task import UmbraTask
from core.runtime.umbra_task_planner import UmbraTaskPlanner
from core.runtime.umbra_task_executor import UmbraTaskExecutor


class UmbraTaskEngine:
    """
    FULL TASK LIFECYCLE MANAGER

    goal → plan → execute → complete
    """

    def __init__(self, llm=None):
        self.planner = UmbraTaskPlanner(llm_engine=llm)
        self.executor = UmbraTaskExecutor()

        self.tasks = {}

    # -----------------------
    # CREATE TASK
    # -----------------------
    def create_task(self, goal: str):
        task_id = str(uuid.uuid4())

        steps = self.planner.decompose(goal)

        task = UmbraTask(
            id=task_id,
            goal=goal,
            steps=steps
        )

        self.tasks[task_id] = task

        return task

    # -----------------------
    # RUN TASK
    # -----------------------
    def run_task(self, task_id: str):
        task = self.tasks.get(task_id)

        if not task:
            return {"error": "task_not_found"}

        while True:
            step = task.next_step()

            if not step:
                task.status = "completed"
                break

            result = self.executor.execute_step(step, task.context)

            task.result = result

            if result.get("status") == "error":
                task.status = "failed"
                task.error = result.get("error")
                break

        return {
            "task_id": task.id,
            "status": task.status,
            "result": task.result
        }