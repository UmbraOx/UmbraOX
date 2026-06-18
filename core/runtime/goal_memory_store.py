from core.runtime.persistent_execution_memory import (
    PersistentExecutionMemory
)


class GoalMemoryStore:

    def __init__(self):

        self.memory = (
            PersistentExecutionMemory()
        )

    def save_goal(
        self,
        goal
    ):

        self.memory.record({
            "type": "goal",
            "goal": goal
        })