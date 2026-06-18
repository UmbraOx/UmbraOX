import time
from typing import Dict, Any

from core.runtime.umbra_llm_patch_engine import UmbraLLMPatchEngine


class UmbraGenerationEngine:
    """
    Central execution engine for ALL Umbra generation tasks.

    This is the single entry point for:
    - image prompts
    - game generation requests
    - text outputs
    - asset-producing tasks
    """

    def __init__(self, asset_store, ollama_model="llama3.1"):

        self.asset_store = asset_store
        self.patch_engine = UmbraLLMPatchEngine(ollama_model=ollama_model)

        self.last_result = None

    # -------------------------
    # MAIN ENTRY POINT
    # -------------------------

    def generate(self, request: Dict[str, Any]):

        task_type = request.get("type", "unknown")
        prompt = request.get("prompt", "")

        analysis = self._analyze_request(task_type, prompt)

        raw_output = self._execute_generation(task_type, prompt, analysis)

        asset = self._store_asset(task_type, raw_output)

        self.last_result = asset

        return {
            "status": "success",
            "task_type": task_type,
            "asset_id": asset.asset_id,
            "file_path": asset.file_path,
            "timestamp": time.time()
        }

    # -------------------------
    # ANALYSIS LAYER
    # -------------------------

    def _analyze_request(self, task_type: str, prompt: str) -> str:

        return f"""
Task Type: {task_type}
Prompt: {prompt}

Analyze requirements, constraints, and required output structure.
Determine best generation strategy.
"""

    # -------------------------
    # EXECUTION LAYER
    # -------------------------

    def _execute_generation(self, task_type: str, prompt: str, analysis: str):

        # In real system this would route to:
        # - SDXL (images)
        # - Ollama (text/code)
        # - TTS engine (audio)
        # - game builder pipeline (Unity/UE export)

        llm_prompt = f"""
You are Umbra Generation Engine.

TASK TYPE: {task_type}

PROMPT:
{prompt}

ANALYSIS:
{analysis}

Return structured output appropriate for this task.
"""

        return self.patch_engine._call_llm(llm_prompt)

    # -------------------------
    # STORAGE LAYER
    # -------------------------

    def _store_asset(self, task_type: str, output: str):

        from core.runtime.umbra_asset import UmbraAsset

        asset = UmbraAsset(
            asset_type=task_type,
            data=output,
            metadata={
                "source": "umbra_generation_engine"
            }
        )

        return self.asset_store.save(asset)