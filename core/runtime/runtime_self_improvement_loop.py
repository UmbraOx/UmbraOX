from typing import Any, Dict, List, Optional
from datetime import datetime


class ImprovementPlan:
    """
    Stable object-first plan container.
    """

    def __init__(self, targets: List[Dict[str, Any]]):
        self.targets = targets
        self.generated_at = datetime.utcnow().isoformat()
        self.executed = False
        self.results: List[Any] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "targets": self.targets,
            "generated_at": self.generated_at,
            "executed": self.executed,
            "results": self.results,
        }


class RuntimeSelfImprovementLoop:
    """
    Stable improvement loop with strict object contracts.
    """

    def __init__(self, analyzer, pipeline):
        self.analyzer = analyzer
        self.pipeline = pipeline
        self.last_plan: Optional[ImprovementPlan] = None

    # --- REQUIRED BY TESTS ---
    def analyze_and_plan(self) -> ImprovementPlan:
        """
        Generates improvement plan from analyzer output.
        """
        summary = self.analyzer.get_module_summary()

        targets = []

        # Normalize whatever analyzer returns
        for item in summary.get("suggestions", []):
            targets.append({
                "module": item.get("module"),
                "reason": item.get("reason", "heuristic"),
                "priority": item.get("priority", "medium"),
            })

        # fallback if analyzer gives nothing
        if not targets:
            targets = [{
                "module": "system_self_check",
                "reason": "default_scan",
                "priority": "low",
            }]

        self.last_plan = ImprovementPlan(targets)
        return self.last_plan

    # backward compatibility
    def run(self) -> ImprovementPlan:
        return self.analyze_and_plan()

    def execute(self) -> Dict[str, Any]:
        """
        Stub execution layer (safe mode).
        """
        if not self.last_plan:
            self.analyze_and_plan()

        self.last_plan.executed = True
        self.last_plan.results.append({
            "status": "safe_stub_execution",
            "timestamp": datetime.utcnow().isoformat()
        })

        return self.last_plan.to_dict()