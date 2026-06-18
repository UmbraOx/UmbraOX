from core.runtime.umbra_bridge import UmbraBridge
from core.agents.priority_scorer import PriorityScorer
from core.agents.task_queue import EvolutionQueue
from core.runtime.umbra_sandbox import UmbraSandbox
from core.runtime.umbra_evolution_journal import UmbraEvolutionJournal
from core.runtime.umbra_task_engine import UmbraTaskEngine


class BossAgent:
    """
    UMBRA ORCHESTRATION BRAIN

    Responsibilities:
    - system audit
    - prioritization
    - task queue management
    - patch proposals
    - task execution via task engine
    """

    def __init__(self, base_path: str, auto_mode: bool = False):

        self.base_path = base_path

        self.bridge = UmbraBridge(base_path)
        self.scorer = PriorityScorer()
        self.queue = EvolutionQueue()

        self.sandbox = UmbraSandbox()
        self.journal = UmbraEvolutionJournal()

        self.auto_mode = auto_mode

        # --------------------------
        # TASK ENGINE (CRITICAL)
        # --------------------------
        self.task_engine = UmbraTaskEngine(llm=None)

    # ---------------------------
    # SYSTEM AUDIT CYCLE
    # ---------------------------
    def run_cycle(self):

        audit = self.bridge.run_full_audit()
        scored = self.scorer.score(audit["modules"])

        for item in scored:
            self.queue.add(item)

        self.journal.log({
            "event": "cycle_run",
            "modules_scanned": len(audit["modules"]),
            "queue_size": self.queue.size()
        })

        return {
            "audit": audit,
            "queue_size": self.queue.size()
        }

    # ---------------------------
    # TASK EXECUTION (LEGACY + MODERN)
    # ---------------------------
    def execute_next(self):

        task = self.queue.pop()

        if not task:
            return {"status": "idle"}

        proposal = self.bridge.propose_fix(
            task["file"],
            task["reason"]
        )

        diff = proposal["diff"]
        patch = proposal["proposal"]

        sandbox_result = None

        if self.auto_mode:
            sandbox_result = self.sandbox.test_run(task["file"])

        self.journal.log({
            "event": "proposal_generated",
            "file": task["file"],
            "priority": task["priority"],
            "sandbox_ok": sandbox_result["success"] if sandbox_result else None
        })

        return {
            "diff": diff,
            "proposal": patch,
            "sandbox": sandbox_result,
            "task": task
        }

    # ---------------------------
    # DIRECT TASK API
    # ---------------------------
    def run_task(self, goal: str):
        return self.task_engine.run_task(goal)