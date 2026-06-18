from __future__ import annotations

import ast
import os
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Set, Optional


# =========================================================
# DATA MODEL
# =========================================================

@dataclass
class FileNode:
    path: str
    imports: List[str]
    functions: List[str]
    classes: List[str]
    has_docstring: bool


@dataclass
class RepairAction:
    path: str
    intent: str  # improve | refactor | simulate_delete | ignore | protect
    reason: str
    risk: float
    priority: str


@dataclass
class RepairPlan:
    actions: List[RepairAction]
    summary: str


# =========================================================
# OBSERVATION LAYER (AST + GRAPH)
# =========================================================

class CodebaseObserver:

    def scan_file(self, file_path: Path) -> Optional[FileNode]:
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except Exception:
            return None

        imports = []
        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports += [n.name for n in node.names]

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return FileNode(
            path=str(file_path),
            imports=imports,
            functions=functions,
            classes=classes,
            has_docstring=ast.get_docstring(tree) is not None
        )


# =========================================================
# KNOWLEDGE GRAPH
# =========================================================

class DependencyGraph:

    def __init__(self):
        self.edges: Dict[str, Set[str]] = {}

    def add(self, node: FileNode):
        self.edges[node.path] = set(node.imports)

    def is_required(self, path: str) -> bool:
        for deps in self.edges.values():
            if path in deps:
                return True
        return False


# =========================================================
# REASONING LAYER
# =========================================================

class RepairReasoner:

    def evaluate(self, node: FileNode, graph: DependencyGraph) -> RepairAction:

        # NEVER DELETE CORE STRUCTURE FILES
        name = node.path.split("\\")[-1].lower()
        if name in {"__init__.py", "__main__.py", "setup.py"}:
            return RepairAction(
                path=node.path,
                intent="protect",
                reason="core_framework_file",
                risk=0.0,
                priority="high"
            )

        # STUB DETECTION (ONLY IF ISOLATED)
        is_stub = len(node.functions) == 0 and len(node.classes) == 0

        if is_stub and not graph.is_required(node.path):
            return RepairAction(
                path=node.path,
                intent="simulate_delete",
                reason="isolated_stub_no_dependencies",
                risk=0.7,
                priority="medium"
            )

        # IMPROVEMENT CASE
        if node.functions and not node.has_docstring:
            return RepairAction(
                path=node.path,
                intent="improve",
                reason="missing_documentation",
                risk=0.4,
                priority="low"
            )

        return RepairAction(
            path=node.path,
            intent="ignore",
            reason="stable",
            risk=0.1,
            priority="low"
        )


# =========================================================
# PLANNING LAYER
# =========================================================

class RepairPlanner:

    def build_plan(self, actions: List[RepairAction]) -> RepairPlan:

        summary = {
            "protect": 0,
            "improve": 0,
            "simulate_delete": 0,
            "ignore": 0
        }

        for a in actions:
            summary[a.intent] += 1

        return RepairPlan(
            actions=sorted(actions, key=lambda x: x.risk, reverse=True),
            summary=json.dumps(summary, indent=2)
        )


# =========================================================
# EXECUTION LAYER (SAFE + CONTROLLED)
# =========================================================

class SafeExecutor:

    def simulate(self, plan: RepairPlan) -> Dict:
        return {
            "SIMULATION_ONLY": True,
            "plan": [asdict(a) for a in plan.actions],
            "summary": plan.summary
        }

    def require_approval(self, preview: Dict) -> bool:
        print("\n=== UMBRA REPAIR PLAN PREVIEW ===")
        print(json.dumps(preview, indent=2))

        return input("\nApprove? (yes/no): ").strip().lower() == "yes"


# =========================================================
# ORCHESTRATOR (MAIN SYSTEM)
# =========================================================

class UmbraSelfRepairCore:

    def __init__(self, root: str):
        self.root = Path(root)
        self.observer = CodebaseObserver()
        self.graph = DependencyGraph()
        self.reasoner = RepairReasoner()
        self.planner = RepairPlanner()
        self.executor = SafeExecutor()

    def run_scan(self):

        nodes = []
        actions = []

        # OBSERVE
        for file in self.root.rglob("*.py"):
            node = self.observer.scan_file(file)
            if node:
                nodes.append(node)
                self.graph.add(node)

        # REASON
        for node in nodes:
            actions.append(self.reasoner.evaluate(node, self.graph))

        # PLAN
        plan = self.planner.build_plan(actions)

        # EXECUTE (SAFE)
        preview = self.executor.simulate(plan)

        if self.executor.require_approval(preview):
            print("\nExecution layer not yet enabled (safe mode default).")
            return preview

        print("No changes applied.")
        return preview