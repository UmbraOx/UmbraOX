from core.runtime.umbra_self_test_engine import UmbraSelfTestEngine
from core.runtime.umbra_regression_detector import UmbraRegressionDetector
from core.runtime.umbra_intelligent_rollback import UmbraIntelligentRollback


class UmbraProductionEvolutionPipeline:
    """
    SAFE SELF-IMPROVEMENT LOOP

    Flow:
    proposal → test → regression score → decision → apply/rollback
    """

    def __init__(self, patch_engine, logger=None):

        self.patch_engine = patch_engine
        self.logger = logger

        self.tester = UmbraSelfTestEngine()
        self.regression = UmbraRegressionDetector()
        self.rollback = UmbraIntelligentRollback()

    def process(self, proposal):

        # 1. snapshot original
        original = proposal.original
        modified = proposal.modified

        # 2. regression score
        regression_score = self.regression.score_regression(original, modified)

        # 3. run tests
        test_result = self.tester.run_tests()

        # 4. intelligent decision
        decision = self.rollback.evaluate(regression_score, test_result)

        if self.logger:
            self.logger.log_event({
                "event": "evolution_evaluation",
                "risk": decision["risk_score"],
                "decision": decision["decision"]
            })

        # 5. apply or rollback
        if decision["decision"] == "accept":
            self.patch_engine.apply_patch(
                proposal,
                backup_dir="C:\\Umbra\\backups"
            )

            return {
                "status": "applied",
                "risk": decision
            }

        else:
            return {
                "status": "rejected",
                "risk": decision
            }