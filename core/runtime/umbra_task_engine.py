# C:\Umbra\core\runtime\umbra_task_engine.py
# Umbra Task Engine v2.0 — Full Task Lifecycle Manager
# FIXED: run_task now accepts BOTH goal string AND task_id
# BossAgent calls run_task(goal) — this now handles both cases

import uuid
import time
import logging

log = logging.getLogger("umbra.task_engine")


class UmbraTask:
    def __init__(self, task_id: str, goal: str, steps: list):
        self.id      = task_id
        self.goal    = goal
        self.steps   = list(steps)
        self._cursor = 0
        self.status  = "pending"
        self.result  = None
        self.error   = None
        self.context = {}
        self.created = time.time()

    def next_step(self):
        if self._cursor < len(self.steps):
            s = self.steps[self._cursor]
            self._cursor += 1
            return s
        return None

    def to_dict(self):
        return {
            "id":      self.id,
            "goal":    self.goal,
            "steps":   self.steps,
            "status":  self.status,
            "result":  self.result,
            "error":   self.error,
            "created": self.created,
        }


class _StubPlanner:
    def decompose(self, goal: str) -> list:
        # Returns list of step dicts
        words = goal.split()
        if len(words) <= 6:
            return [{"step": goal, "type": "direct"}]
        # Break into up to 3 phases
        chunk = max(1, len(words) // 3)
        return [
            {"step": " ".join(words[i:i+chunk]), "type": "direct"}
            for i in range(0, len(words), chunk)
        ]


class _StubExecutor:
    def execute_step(self, step: dict, context: dict) -> dict:
        return {"status": "ok", "step": step.get("step", ""), "output": None}


class UmbraTaskEngine:
    """
    Full Task Lifecycle Manager.

    Usage:
        engine = UmbraTaskEngine(llm=llm_provider)
        task   = engine.create_task("Build a game called DemiWorld")
        result = engine.run_task(task.id)        # by id
        result = engine.run_task("some goal")    # by goal string — also works
    """

    def __init__(self, llm=None):
        self.llm   = llm
        self.tasks = {}  # task_id -> UmbraTask

        # Try real planner/executor, fall back to stubs
        try:
            from core.runtime.umbra_task_planner import UmbraTaskPlanner
            self.planner = UmbraTaskPlanner(llm_engine=llm)
        except Exception:
            self.planner = _StubPlanner()

        try:
            from core.runtime.umbra_task_executor import UmbraTaskExecutor
            self.executor = UmbraTaskExecutor()
        except Exception:
            self.executor = _StubExecutor()

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────────────────────────────────

    def create_task(self, goal: str) -> UmbraTask:
        task_id = str(uuid.uuid4())
        try:
            steps = self.planner.decompose(goal)
        except Exception:
            steps = [{"step": goal, "type": "direct"}]
        task = UmbraTask(task_id=task_id, goal=goal, steps=steps)
        self.tasks[task_id] = task
        log.debug("Created task %s: %s", task_id[:8], goal[:60])
        return task

    # ─────────────────────────────────────────────────────────────────────────
    # RUN — accepts task_id OR goal string
    # ─────────────────────────────────────────────────────────────────────────

    def run_task(self, task_id_or_goal: str) -> dict:
        """
        Run a task by ID or by goal string.
        If task_id_or_goal is not a known task ID, it is treated as a goal
        and a new task is created automatically.
        """
        # Resolve task
        if task_id_or_goal in self.tasks:
            task = self.tasks[task_id_or_goal]
        else:
            # Treat as goal — create on the fly
            task = self.create_task(task_id_or_goal)

        task.status = "running"
        try:
            while True:
                step = task.next_step()
                if not step:
                    task.status = "completed"
                    break
                result = self.executor.execute_step(step, task.context)
                task.result = result
                if result.get("status") == "error":
                    task.status = "failed"
                    task.error  = result.get("error", "unknown")
                    break
                # Merge step output into context for next step
                if isinstance(result.get("output"), dict):
                    task.context.update(result["output"])
        except Exception as e:
            task.status = "failed"
            task.error  = str(e)
            log.error("Task %s failed: %s", task.id[:8], e)

        return {
            "task_id": task.id,
            "goal":    task.goal,
            "status":  task.status,
            "result":  task.result,
            "error":   task.error,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────────────────────────

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)

    def list_tasks(self) -> list:
        return [t.to_dict() for t in self.tasks.values()]

    def clear_completed(self):
        to_del = [k for k, v in self.tasks.items() if v.status in ("completed", "failed")]
        for k in to_del:
            del self.tasks[k]
        return len(to_del)