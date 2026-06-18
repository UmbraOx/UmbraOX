import shutil
import os


class UmbraIntelligentRollback:
    """
    Handles rollback decisions based on risk scoring.
    """

    def __init__(self):
        self.history = []

    def evaluate(self, regression_score: float, test_result: dict) -> dict:

        risk_score = regression_score

        if not test_result.get("success", False):
            risk_score += 0.4

        decision = "rollback" if risk_score > 0.5 else "accept"

        return {
            "risk_score": round(risk_score, 3),
            "decision": decision
        }

    def rollback_file(self, backup_path: str, target_path: str):

        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, target_path)

        return {
            "status": "rolled_back",
            "from": backup_path,
            "to": target_path
        }