import json
import difflib
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class PatchProposal:
    file_path: str
    original: str
    modified: str
    reason: str
    risk_level: str = "low"


class UmbraLLMPatchEngine:
    """
    LLM-driven patch generator + diff system (Ollama-backed)
    """

    def __init__(self, ollama_model: str = "llama3.1", base_path: str = "C:\\Umbra"):
        self.model = ollama_model
        self.base_path = Path(base_path)
        self.history = []

    # ---------------------------
    # LLM CALL (OLLAMA)
    # ---------------------------
    def _call_llm(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120
            )
            return result.stdout.decode("utf-8", errors="ignore")
        except Exception as e:
            return f"ERROR_LLM_CALL: {str(e)}"

    # ---------------------------
    # PATCH GENERATION
    # ---------------------------
    def generate_patch(self, file_path: str, analysis: str) -> PatchProposal:
        target = Path(file_path)

        if not target.exists():
            raise FileNotFoundError(file_path)

        original = target.read_text(encoding="utf-8", errors="ignore")

        prompt = f"""
You are Umbra OS self-improvement engine.

Task:
Improve this file based on analysis.

Rules:
- Do NOT change external behavior unless necessary
- Keep compatibility
- Fix bugs, add safety, improve structure
- Return ONLY updated full file

File:
{file_path}

Analysis:
{analysis}

Code:
{original}
"""

        modified = self._call_llm(prompt)

        return PatchProposal(
            file_path=file_path,
            original=original,
            modified=modified,
            reason=analysis
        )

    # ---------------------------
    # DIFF VIEW
    # ---------------------------
    def diff(self, proposal: PatchProposal) -> str:
        return "\n".join(
            difflib.unified_diff(
                proposal.original.splitlines(),
                proposal.modified.splitlines(),
                fromfile="original",
                tofile="modified",
                lineterm=""
            )
        )

    # ---------------------------
    # APPLY PATCH (SAFE)
    # ---------------------------
    def apply_patch(self, proposal: PatchProposal, backup_dir: str):
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        file_path = Path(proposal.file_path)
        backup_file = backup_path / file_path.name

        # backup
        backup_file.write_text(proposal.original, encoding="utf-8")

        # apply
        file_path.write_text(proposal.modified, encoding="utf-8")

        self.history.append({
            "file": proposal.file_path,
            "backup": str(backup_file),
            "reason": proposal.reason
        })

    # ---------------------------
    # SIMULATION MODE
    # ---------------------------
    def simulate(self, proposal: PatchProposal) -> Dict:
        return {
            "file": proposal.file_path,
            "diff": self.diff(proposal),
            "risk": proposal.risk_level,
            "status": "SIMULATION_ONLY"
        }