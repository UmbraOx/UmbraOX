from core.runtime.construction_planner import (
    ConstructionPlanner
)

from core.runtime.runtime_blueprint_system import (
    RuntimeBlueprintSystem
)


class AutonomousPlanningEngine:

    def __init__(self):

        self.planner = ConstructionPlanner()

        self.blueprints = RuntimeBlueprintSystem()

    def build(self, proposal):

        plan = self.planner.create_plan(
            proposal
        )

        blueprint = self.blueprints.generate(
            proposal
        )

        return {
            "proposal": proposal,
            "plan": plan,
            "blueprint": blueprint
        }