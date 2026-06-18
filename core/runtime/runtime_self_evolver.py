from pathlib import Path
import ast
import traceback

from core.runtime.runtime_self_repair_engine import RuntimeSelfRepairEngine
from core.runtime.runtime_self_evolution_engine import RuntimeSelfEvolutionEngine
from core.runtime.umbra_llm_patch_engine import UmbraLLMPatchEngine
from core.agents.boss_agent import BossAgent


class RuntimeSelfEvolver:
    """
    UNIFIED EVOLUTION ORCHESTRATOR (Umbra Core Gate)

    Responsibilities:
    - Single entry point for all self-improvement
    - Coordinates scanning, scoring, patching, and applying
    - Enforces safety gates before any mutation
    """

    def __init__(self, root_dir: str, auto_apply: bool = False):
        self.root_dir = Path(root_dir)
        self.auto_apply = auto_apply

        self.repair_engine = RuntimeSelfRepairEngine(root_dir)
        self.evolution_engine = RuntimeSelfEvolutionEngine(root_dir)
        self.patch_engine = UmbraLLMPatchEngine(base_path=root_dir)
        self.boss = BossAgent(root_dir, auto_mode=auto_apply)

        self.backup_dir = self.root_dir / ".umbra_backups"
        self.backup_dir.mkdir(exist_ok=True, parents=True)

        self.last_report = None

    # ---------------------------
    # MAIN ENTRY POINT
    # ---------------------------
    def run_cycle(self):
        """
        Full evolution cycle:
        1. Scan system
        2. Prioritize issues
        3. Generate patches
        4. Validate
        5. Apply (optional)
        """

        audit = self.boss.bridge.run_full_audit()
        scored = self.boss.scorer.score(audit["modules"])

        results = []

        for item in scored:
            file_path = item["file"]

            try:
                proposal = self.patch_engine.generate_patch(
                    file_path=file_path,
                    analysis=item.get("reason", "no analysis provided")
                )

                diff = self.patch_engine.diff(proposal)

                valid = self._validate_patch(proposal.modified)

                results.append({
                    "file": file_path,
                    "priority": item.get("priority"),
                    "diff": diff,
                    "valid": valid,
                    "applied": False
                })

                if valid and self.auto_apply:
                    self.patch_engine.apply_patch(proposal, str(self.backup_dir))
                    results[-1]["applied"] = True

            except Exception as e:
                results.append({
                    "file": file_path,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "applied": False
                })

        self.last_report = {
            "modules_scanned": len(audit["modules"]),
            "results": results
        }

        return self.last_report

    # ---------------------------
    # VALIDATION GATE (CRITICAL)
    # ---------------------------
    def _validate_patch(self, code: str) -> bool:
        """
        Ensures patch is syntactically safe before writing.
        """

        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    # ---------------------------
    # REPORTING
    # ---------------------------
    def export_report(self, path: str = None):
        if not self.last_report:
            return None

        out_path = Path(path) if path else self.root_dir / "umbra_evolution_report.json"
        out_path.write_text(str(self.last_report), encoding="utf-8")
        return str(out_path)