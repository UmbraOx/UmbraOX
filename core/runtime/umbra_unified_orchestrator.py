from core.runtime.umbra_goal_decomposer import (
    UmbraGoalDecomposer
)

from core.runtime.umbra_phase_planner import (
    UmbraPhasePlanner
)

from core.runtime.umbra_execution_governor import (
    UmbraExecutionGovernor
)

from core.runtime.umbra_runtime_workspace import (
    UmbraRuntimeWorkspace
)

from core.runtime.umbra_system_snapshot import (
    UmbraSystemSnapshot
)

from core.runtime.umbra_self_upgrade_engine import (
    UmbraSelfUpgradeEngine
)

from core.runtime.umbra_construction_pipeline import (
    UmbraConstructionPipeline
)


class UmbraUnifiedOrchestrator:

    def __init__(self):

        self.decomposer = (
            UmbraGoalDecomposer()
        )

        self.planner = (
            UmbraPhasePlanner()
        )

        self.governor = (
            UmbraExecutionGovernor()
        )

        self.workspace = (
            UmbraRuntimeWorkspace()
        )

        self.snapshot = (
            UmbraSystemSnapshot()
        )

        self.upgrades = (
            UmbraSelfUpgradeEngine()
        )

        self.pipeline = (
            UmbraConstructionPipeline()
        )

    def execute(
        self,
        objective
    ):

        approved = (
            self.governor.approve(
                objective
            )
        )

        if not approved:

            return {
                "success": False,
                "reason": "blocked"
            }

        workspace = (
            self.workspace.initialize()
        )

        goals = (
            self.decomposer.decompose(
                objective
            )
        )

        phases = (
            self.planner.build(
                goals
            )
        )

        construction = (
            self.pipeline.build(
                phases
            )
        )

        upgrades = (
            self.upgrades.upgrades(
                objective
            )
        )

        snapshot = (
            self.snapshot.create({
                "objective": objective,
                "phases": phases,
                "upgrades": upgrades
            })
        )

        return {
            "success": True,
            "objective": objective,
            "workspace": workspace,
            "goals": goals,
            "phases": phases,
            "construction": construction,
            "upgrades": upgrades,
            "snapshot": snapshot
        }