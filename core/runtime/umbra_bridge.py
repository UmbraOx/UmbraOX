from core.runtime.umbra_ast_analyzer import UmbraASTAnalyzer
from core.runtime.umbra_llm_patch_engine import UmbraLLMPatchEngine
from pathlib import Path


class UmbraBridge:
    """
    Single entry point for WorkerAI ↔ Umbra evolution system
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.analyzer = UmbraASTAnalyzer()
        self.patcher = UmbraLLMPatchEngine(base_path=base_path)

    # ---------------------------
    # FULL AUDIT PIPELINE
    # ---------------------------
    def run_full_audit(self):
        scan = self.analyzer.scan_project(self.base_path)

        return {
            "summary": {
                "files_scanned": len(scan),
                "total_functions": sum(f["function_count"] for f in scan),
                "total_classes": sum(c["class_count"] for c in scan),
            },
            "modules": scan
        }

    # ---------------------------
    # PATCH WORKFLOW
    # ---------------------------
    def propose_fix(self, file_path: str, analysis: str):
        proposal = self.patcher.generate_patch(file_path, analysis)
        return {
            "diff": self.patcher.diff(proposal),
            "proposal": proposal
        }

    def apply_fix(self, proposal, backup_dir="C:\\Umbra\\backups"):
        self.patcher.apply_patch(proposal, backup_dir)