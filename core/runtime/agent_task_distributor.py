class AgentTaskDistributor:

    def distribute(self, graph):

        assignments = []

        for task in graph.get("tasks", []):

            role = self._assign_role(
                task
            )

            assignments.append({
                "task": task,
                "agent_role": role
            })

        return assignments

    def _assign_role(self, task):

        title = task.get(
            "title",
            ""
        ).lower()

        if "plan" in title:
            return "architect_agent"

        if "runtime" in title:
            return "coder_agent"

        if "validate" in title:
            return "reviewer_agent"

        return "worker_agent"