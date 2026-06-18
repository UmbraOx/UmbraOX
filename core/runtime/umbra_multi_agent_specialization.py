from enum import Enum


class AgentRole(Enum):
    PLANNER = "planner"
    EXECUTOR = "executor"
    REPAIR = "repair"
    AUDITOR = "auditor"
    EVOLUTION = "evolution"


class UmbraMultiAgentSpecialization:
    """
    Converts generic agents into role-based system actors.
    This is what stabilizes your multi-agent chaos layer.
    """

    def __init__(self):
        self.role_map = {}

    def assign_role(self, agent_id: str, role: AgentRole):
        self.role_map[agent_id] = role

    def get_role(self, agent_id: str):
        return self.role_map.get(agent_id, AgentRole.EXECUTOR)

    def route_task(self, agent_id: str, task: dict):
        role = self.get_role(agent_id)

        if role == AgentRole.PLANNER:
            return {"action": "decompose", "task": task}

        if role == AgentRole.REPAIR:
            return {"action": "patch_fix", "task": task}

        if role == AgentRole.AUDITOR:
            return {"action": "analyze", "task": task}

        if role == AgentRole.EVOLUTION:
            return {"action": "mutate_system", "task": task}

        return {"action": "execute", "task": task}