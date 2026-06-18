from __future__ import annotations

import ast
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
import hashlib
import json
import copy


# -----------------------------
# DATA STRUCTURES
# -----------------------------

@dataclass
class FileAnalysis:
    path: str
    imports: List[str]
    classes: List[str]
    functions: List[str]
    has_docstring: bool
    complexity_score: int
    is_stub: bool
    risk_score: float


@dataclass
class RepairCandidate:
    path: str
    reason: str
    priority: str
    risk: float
    action: str  # "improve", "refactor", "delete_simulate", "ignore"


# -----------------------------
# AST ANALYZER
# -----------------------------

class ASTAnalyzer:
    def analyze(self, file_path: Path) -> Optional[FileAnalysis]:
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except Exception:
            return None

        imports = []
        functions = []
        classes = []
        has_docstring = ast.get_docstring(tree) is not None

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

        complexity = len(functions) + len(classes) + len(imports)

        is_stub = (
            len(functions) == 0 and
            len(classes) == 0 and
            len(imports) == 0
        )

        risk = self._compute_risk(file_path, is_stub, complexity)

        return FileAnalysis(
            path=str(file_path),
            imports=imports,
            classes=classes,
            functions=functions,
            has_docstring=has_docstring,
            complexity_score=complexity,
            is_stub=is_stub,
            risk_score=risk
        )

    def _compute_risk(self, path: Path, is_stub: bool, complexity: int) -> float:
        base = 0.1

        if "test" in path.name:
            base += 0.1
        if "__init__" in path.name:
            base -= 0.2  # IMPORTANT: never treat init as low-value by default
        if is_stub:
            base += 0.4
        if complexity > 10:
            base -= 0.2

        return max(0.0, min(1.0, base))


# -----------------------------
# PACKAGE GRAPH
# -----------------------------

class PackageGraph:
    def __init__(self):
        self.graph: Dict[str, Set[str]] = {}

    def add_file(self, analysis: FileAnalysis):
        self.graph[analysis.path] = set(analysis.imports)

    def is_critical(self, path: str) -> bool:
        # Anything imported by others is critical
        for deps in self.graph.values():
            if path in deps:
                return True
        return False


# -----------------------------
# REPAIR ENGINE V2
# -----------------------------

class RuntimeSelfRepairEngineV2:
    """
    SAFE MODE FIRST:
    - Never deletes files directly
    - Only simulates changes
    - Requires explicit approval for actions
    """

    def __init__(self, root: str):
        self.root = Path(root)
        self.analyzer = ASTAnalyzer()
        self.graph = PackageGraph()
        self.analysis_cache: Dict[str, FileAnalysis] = {}

    # -------------------------
    # SCAN
    # -------------------------

    def scan(self) -> List[FileAnalysis]:
        results = []

        for path in self.root.rglob("*.py"):
            analysis = self.analyzer.analyze(path)
            if analysis:
                self.analysis_cache[str(path)] = analysis
                self.graph.add_file(analysis)
                results.append(analysis)

        return results

    # -------------------------
    # PRIORITIZATION
    # -------------------------

    def rank_candidates(self, analyses: List[FileAnalysis]) -> List[RepairCandidate]:
        candidates = []

        for a in analyses:
            reason = []
            action = "ignore"

            if a.is_stub and not self.graph.is_critical(a.path):
                reason.append("isolated_stub")
                action = "delete_simulate"

            if not a.has_docstring and len(a.functions) > 0:
                reason.append("missing_docs")
                action = "improve"

            if a.risk_score > 0.7:
                reason.append("high_risk_change")

            priority = "low"
            if a.risk_score > 0.6:
                priority = "high"
            elif a.risk_score > 0.3:
                priority = "medium"

            candidates.append(
                RepairCandidate(
                    path=a.path,
                    reason=";".join(reason),
                    priority=priority,
                    risk=a.risk_score,
                    action=action
                )
            )

        return sorted(candidates, key=lambda x: x.risk, reverse=True)

    # -------------------------
    # SIMULATION MODE
    # -------------------------

    def simulate_changes(self, candidates: List[RepairCandidate]) -> Dict:
        plan = {
            "deletions": [],
            "improvements": [],
            "ignored": []
        }

        for c in candidates:
            if c.action == "delete_simulate":
                plan["deletions"].append(asdict(c))
            elif c.action == "improve":
                plan["improvements"].append(asdict(c))
            else:
                plan["ignored"].append(asdict(c))

        return plan

    # -------------------------
    # APPROVAL GATE
    # -------------------------

    def require_approval(self, plan: Dict) -> bool:
        print("\n=== UMBRA SELF REPAIR PLAN ===")
        print(json.dumps(plan, indent=2))

        resp = input("\nApprove changes? (yes/no): ").strip().lower()
        return resp == "yes"

    # -------------------------
    # EXECUTION (SAFE PLACEHOLDER)
    # -------------------------

    def execute(self, plan: Dict):
        print("\n[SAFE MODE] No files are being modified yet.")
        print("This system only simulates until explicitly enabled.")
        return plan

    # -------------------------
    # FULL RUN
    # -------------------------

    def run(self):
        analyses = self.scan()
        candidates = self.rank_candidates(analyses)
        plan = self.simulate_changes(candidates)

        if self.require_approval(plan):
            return self.execute(plan)

        print("No changes applied.")
        return plan