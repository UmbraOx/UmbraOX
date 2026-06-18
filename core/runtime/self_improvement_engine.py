# core/runtime/self_improvement_engine.py

import uuid
from core.runtime.code_indexer import CodeIndexer
from core.runtime.upgrade_memory import UpgradeMemory


class SelfImprovementEngine:

    def __init__(self):

        self.indexer = CodeIndexer()

        self.memory = UpgradeMemory()

    # -------------------------------------------------
    # RUN ANALYSIS
    # -------------------------------------------------

    def analyze(self):

        index = self.indexer.index_project()

        proposals = []

        # -----------------------------
        # RULE: TODO DETECTION
        # -----------------------------

        for path, data in index.items():

            for todo in data["todos"]:

                proposal = {
                    "id": str(uuid.uuid4())[:8],
                    "goal": "Resolve TODO item",
                    "file": path,
                    "reason": todo,
                    "type": "maintenance"
                }

                if not self.memory.is_rejected(proposal["goal"]):

                    proposals.append(proposal)

        # -----------------------------
        # RULE: IMPORT COMPLEXITY
        # -----------------------------

        total_imports = sum(
            len(d["imports"]) for d in index.values()
        )

        if total_imports > 150:

            proposal = {
                "id": str(uuid.uuid4())[:8],
                "goal": "Reduce import complexity",
                "file": "project-wide",
                "reason": f"{total_imports} imports detected",
                "type": "architecture"
            }

            if not self.memory.is_rejected(proposal["goal"]):

                proposals.append(proposal)

        print(f"[SELF_IMPROVEMENT] proposals: {len(proposals)}")

        return proposals