class AgentRoleManager:

    def assign_roles(self, domains):

        mapping = {
            "runtime": "runtime_engineer",
            "ui": "ui_architect",
            "agents": "agent_designer",
            "deployment": "deployment_specialist",
            "planning": "planner"
        }

        roles = []

        for domain in domains:
            roles.append(
                mapping.get(
                    domain,
                    "generalist"
                )
            )

        return roles