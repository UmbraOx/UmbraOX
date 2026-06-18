from core.runtime.implementation_planner import (
    ImplementationPlanner
)

from core.runtime.patch_blueprint import (
    PatchBlueprint
)

from core.runtime.execution_simulator import (
    ExecutionSimulator
)

from core.runtime.rollback_manager import (
    RollbackManager
)

from core.runtime.patch_generator import (
    PatchGenerator
)

from core.runtime.deployment_manager import (
    DeploymentManager
)


class ApprovalExecutionEngine:

    def __init__(self):

        self.planner = (
            ImplementationPlanner()
        )

        self.blueprint = (
            PatchBlueprint()
        )

        self.simulator = (
            ExecutionSimulator()
        )

        self.rollback = (
            RollbackManager()
        )

        self.generator = (
            PatchGenerator()
        )

        self.deployer = (
            DeploymentManager()
        )

    def prepare(self, proposal):

        plan = self.planner.build_plan(
            proposal
        )

        blueprint = self.blueprint.create(
            plan
        )

        checkpoint = (
            self.rollback.create_checkpoint(
                proposal.get("target", "")
            )
        )

        simulation = (
            self.simulator.simulate(
                plan,
                blueprint
            )
        )

        bundle = self.generator.generate(
            proposal,
            plan
        )

        return {
            "proposal": proposal,
            "plan": plan,
            "blueprint": blueprint,
            "simulation": simulation,
            "checkpoint": checkpoint,
            "bundle": bundle,
        }

    def deploy(self, prepared):

        bundle = prepared["bundle"]

        deployment = (
            self.deployer.execute(
                bundle
            )
        )

        return deployment