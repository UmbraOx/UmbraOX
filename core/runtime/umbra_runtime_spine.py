# C:\Umbra\core\runtime\umbra_runtime_spine.py
# Umbra Runtime Spine v2.0 — Central Wiring Layer
# Connects: BossAgent -> TaskEngine -> GenerationEngine -> AssetStore
# Fixed: removed bridge.analyze() call that didn't exist, unified API

import os
import sys
import json
import time
import logging

log = logging.getLogger("umbra.spine")

# ─── Safe imports ────────────────────────────────────────────────────────────
try:
    from core.runtime.umbra_generation_engine import UmbraGenerationEngine
    _gen_ok = True
except ImportError:
    _gen_ok = False

try:
    from core.runtime.umbra_asset_store import UmbraAssetStore
    _asset_ok = True
except ImportError:
    _asset_ok = False

try:
    from core.agents.boss_agent import BossAgent
    _boss_ok = True
except ImportError:
    _boss_ok = False

try:
    from core.runtime.umbra_task_engine import UmbraTaskEngine
    _task_ok = True
except ImportError:
    _task_ok = False


# ─── Stub fallbacks so Umbra still starts if a sub-module is missing ─────────
class _StubAssetStore:
    def save(self, asset): return asset
    def list(self): return []
    def get(self, aid): return None

class _StubGenerationEngine:
    def generate(self, req):
        return {"status": "stub", "task_type": req.get("type", "?"), "asset_id": None, "file_path": None}

class _StubBossAgent:
    def run_cycle(self): return {"status": "idle"}
    def execute_next(self): return None
    def plan(self, goal): return [{"step": goal, "type": "direct"}]

class _StubTaskEngine:
    def create_task(self, goal): return type("T", (), {"id": "stub", "goal": goal, "status": "pending"})()
    def run_task(self, task_id): return {"task_id": task_id, "status": "completed", "result": {}}


class UmbraRuntimeSpine:
    """
    CENTRAL SYSTEM WIRING LAYER — the authoritative entry point for all
    Umbra task execution.

    Flow:
        run_task(task_dict)
            -> BossAgent.plan(goal)           # decompose into steps
            -> GenerationEngine.generate(req) # execute each step
            -> AssetStore.save(asset)         # persist results
            -> return result dict

    tick() is called by the runtime loop; it pops the next queued task
    and processes it.
    """

    def __init__(self, base_path: str = "C:\\Umbra"):
        self.base_path = base_path
        self._task_queue = []          # list of task dicts waiting to run
        self._history    = []          # completed task results
        self._running    = False

        # ── Asset store ─────────────────────────────────────────────────────
        if _asset_ok:
            try:
                self.asset_store = UmbraAssetStore()
            except Exception as e:
                log.warning("AssetStore init failed (%s) — using stub", e)
                self.asset_store = _StubAssetStore()
        else:
            self.asset_store = _StubAssetStore()

        # ── Generation engine ────────────────────────────────────────────────
        if _gen_ok:
            try:
                self.generation_engine = UmbraGenerationEngine(self.asset_store)
            except Exception as e:
                log.warning("GenerationEngine init failed (%s) — using stub", e)
                self.generation_engine = _StubGenerationEngine()
        else:
            self.generation_engine = _StubGenerationEngine()

        # ── Boss agent ───────────────────────────────────────────────────────
        if _boss_ok:
            try:
                self.boss_agent = BossAgent(base_path)
            except Exception as e:
                log.warning("BossAgent init failed (%s) — using stub", e)
                self.boss_agent = _StubBossAgent()
        else:
            self.boss_agent = _StubBossAgent()

        # ── Task engine ──────────────────────────────────────────────────────
        if _task_ok:
            try:
                self.task_engine = UmbraTaskEngine()
            except Exception as e:
                log.warning("TaskEngine init failed (%s) — using stub", e)
                self.task_engine = _StubTaskEngine()
        else:
            self.task_engine = _StubTaskEngine()

        log.info("UmbraRuntimeSpine initialised at %s", base_path)

    # ─────────────────────────────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────────────────────────────

    def run_task(self, task: dict) -> dict:
        """
        Execute a task dict synchronously and return a result dict.

        task format:
            {
                "type":   "game" | "image" | "code" | "text" | "sprite" | ...,
                "prompt": "natural language description",
                "name":   "optional project/asset name",
            }
        """
        if not isinstance(task, dict):
            return {"status": "error", "error": "task must be a dict"}

        task_type = task.get("type", "code")
        prompt    = task.get("prompt", "")
        name      = task.get("name", "untitled")

        if not prompt:
            return {"status": "error", "error": "task has no prompt"}

        # 1. Plan: decompose goal into steps
        try:
            steps = self.boss_agent.plan(prompt)
        except Exception as e:
            log.warning("BossAgent.plan failed: %s — using direct passthrough", e)
            steps = [{"step": prompt, "type": task_type}]

        # 2. Execute each step through GenerationEngine
        results = []
        for step in steps:
            step_req = {
                "type":   step.get("type", task_type),
                "prompt": step.get("step", prompt),
                "name":   name,
            }
            try:
                r = self.generation_engine.generate(step_req)
                results.append(r)
            except Exception as e:
                log.error("GenerationEngine.generate failed: %s", e)
                results.append({"status": "error", "error": str(e)})

        # 3. Compile final result
        success_results = [r for r in results if r.get("status") == "success"]
        final = {
            "status":    "success" if success_results else "partial",
            "task_type": task_type,
            "prompt":    prompt,
            "steps_run": len(steps),
            "results":   results,
            "file_path": success_results[-1].get("file_path") if success_results else None,
            "asset_id":  success_results[-1].get("asset_id")  if success_results else None,
            "timestamp": time.time(),
        }
        self._history.append(final)
        return final

    def queue_task(self, task: dict):
        """Add a task to the async queue; processed on next tick()."""
        self._task_queue.append(task)

    def tick(self) -> dict:
        """
        Called once per runtime loop cycle.
        Processes one queued task (if any), otherwise runs BossAgent cycle.
        """
        # Process one queued task
        if self._task_queue:
            task = self._task_queue.pop(0)
            return self.run_task(task)

        # Run boss agent background cycle
        try:
            cycle = self.boss_agent.run_cycle()
            next_task = self.boss_agent.execute_next()
            if next_task and isinstance(next_task, dict) and next_task.get("status") != "idle":
                return self.run_task(next_task)
        except Exception:
            pass

        return {"status": "idle", "queue_depth": len(self._task_queue)}

    # ─────────────────────────────────────────────────────────────────────────
    # DIAGNOSTICS
    # ─────────────────────────────────────────────────────────────────────────

    def get_history(self) -> list:
        return list(self._history)

    def get_queue_depth(self) -> int:
        return len(self._task_queue)

    def status(self) -> dict:
        return {
            "base_path":    self.base_path,
            "queue_depth":  len(self._task_queue),
            "history_len":  len(self._history),
            "gen_engine":   type(self.generation_engine).__name__,
            "boss_agent":   type(self.boss_agent).__name__,
            "task_engine":  type(self.task_engine).__name__,
            "asset_store":  type(self.asset_store).__name__,
        }