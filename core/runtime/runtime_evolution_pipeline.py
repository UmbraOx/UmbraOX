from core.runtime.runtime_patch_contract import PatchContractValidator
from core.runtime.runtime_evolution_governor import EvolutionGovernor


class RuntimeEvolutionPipeline:
    """
    END-TO-END SELF-MODIFICATION PIPELINE

    scan → generate → validate → diff → approve → apply → rollback safety
    """

    def __init__(self, patch_engine, governor: EvolutionGovernor):
        self.patch_engine = patch_engine
        self.contract = PatchContractValidator()
        self.governor = governor

        self.approved_cache = {}
        self.failed_patches = []

    # -------------------------
    # GENERATE PATCH
    # -------------------------
    def generate(self, file_path: str, analysis: str):
        raw = self.patch_engine._call_llm(
            self._build_prompt(file_path, analysis)
        )

        contract = self.contract.verify(raw)

        return {
            "file": file_path,
            "code": contract["code"],
            "valid": contract["syntax_valid"],
            "error": contract.get("error")
        }

    # -------------------------
    # BUILD PROMPT
    # -------------------------
    def _build_prompt(self, file_path: str, analysis: str):
        return f"""
You are Umbra Evolution Engine.

Return code ONLY between markers:
===BEGIN FILE===
...full file...
===END FILE===

Rules:
- Preserve functionality
- Fix issues only if needed
- No markdown

File: {file_path}
Analysis: {analysis}
"""

    # -------------------------
    # APPLY WITH GOVERNOR + SAFETY
    # -------------------------
    def apply(self, file_path: str, code: str):
        if not self.governor.allow_patch(file_path):
            return {"status": "blocked_by_governor"}

        try:
            from pathlib import Path
            path = Path(file_path)

            backup = path.read_text(encoding="utf-8", errors="ignore")

            # write new version
            path.write_text(code, encoding="utf-8")

            # verify rollback safety
            if not self.contract.validate_syntax(code)["valid"]:
                path.write_text(backup, encoding="utf-8")
                return {"status": "rollback_syntax_failure"}

            return {"status": "applied"}

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }