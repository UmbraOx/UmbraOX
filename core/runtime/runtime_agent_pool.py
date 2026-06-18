import threading
from datetime import datetime


class AgentTask:

    def __init__(self, agent_id, task_id, objective):
        self.agent_id = agent_id
        self.task_id = task_id
        self.objective = objective
        self.status = "pending"
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "objective": self.objective,
            "status": self.status,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class RuntimeAgentPool:
    """
    Pool of parallel agents for concurrent task execution.
    Each agent runs in its own thread with its own orchestrator context.
    Supports up to max_agents concurrent agents.
    """

    def __init__(self, max_agents=3):
        self.max_agents = max_agents
        self._lock = threading.Lock()
        self._active_agents = {}
        self._completed_tasks = []
        self._agent_counter = 0

    def submit(self, task_id, objective, executor_fn):
        with self._lock:
            if len(self._active_agents) >= self.max_agents:
                return None, "pool_full"
            self._agent_counter += 1
            agent_id = f"agent_{self._agent_counter:03d}"

        agent_task = AgentTask(agent_id, task_id, objective)
        thread = threading.Thread(
            target=self._run_agent,
            args=(agent_task, executor_fn),
            daemon=True,
        )

        with self._lock:
            self._active_agents[agent_id] = agent_task

        thread.start()
        return agent_id, None

    def _run_agent(self, agent_task, executor_fn):
        agent_task.status = "running"
        agent_task.started_at = datetime.now().isoformat()
        try:
            result = executor_fn(agent_task.objective)
            agent_task.result = result
            agent_task.status = "completed"
        except Exception as e:
            agent_task.error = str(e)
            agent_task.status = "failed"
        finally:
            agent_task.completed_at = datetime.now().isoformat()
            with self._lock:
                self._active_agents.pop(agent_task.agent_id, None)
                self._completed_tasks.append(agent_task.to_dict())

    def get_active_count(self):
        with self._lock:
            return len(self._active_agents)

    def get_active_agents(self):
        with self._lock:
            return [t.to_dict() for t in self._active_agents.values()]

    def get_completed_tasks(self):
        with self._lock:
            return list(self._completed_tasks)

    def wait_all(self, timeout=30):
        import time
        start = time.time()
        while self.get_active_count() > 0:
            if time.time() - start > timeout:
                return False
            time.sleep(0.1)
        return True

    def is_full(self):
        return self.get_active_count() >= self.max_agents

    def capacity(self):
        return self.max_agents - self.get_active_count()

    def reset_completed(self):
        with self._lock:
            self._completed_tasks.clear()