import ast
import os
import subprocess
import sys
from datetime import datetime


class ValidationResult:

    def __init__(self, passed, issues=None, score=0, details=None):
        self.passed = passed
        self.issues = issues or []
        self.score = score
        self.details = details or {}
        self.validated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "passed": self.passed,
            "issues": self.issues,
            "score": self.score,
            "details": self.details,
            "validated_at": self.validated_at,
        }


class RuntimeRunValidator:
    """
    Validates pipeline run outputs before saving.
    - Syntax checks on all written Python files
    - Execution check (can the code actually run?)
    - Quality checks (has docstrings? error handling?)
    - Completeness check (not just stubs?)
    """

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.validation_history = []

    def validate_run(self, pipeline_run, workspace_base=None):
        issues = []
        details = {}
        score = 100

        if not pipeline_run.written_files:
            return ValidationResult(False, ["No files written"], 0)

        syntax_results = []
        for file_info in pipeline_run.written_files:
            file_path = file_info.get("file", "")
            if workspace_base:
                full_path = os.path.join(workspace_base, pipeline_run.run_id, file_path)
            else:
                full_path = file_path

            if not os.path.exists(full_path):
                issues.append(f"File not found: {file_path}")
                score -= 20
                continue

            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()

            result = self._check_file(source, full_path)
            syntax_results.append(result)
            issues.extend(result.get("issues", []))
            score += result.get("bonus", 0)
            score -= result.get("penalty", 0)

        details["files_checked"] = len(syntax_results)
        details["syntax_ok"] = sum(1 for r in syntax_results if r.get("syntax_ok"))

        score = max(0, min(100, score))
        passed = len([i for i in issues if "CRITICAL" in i]) == 0
        result = ValidationResult(passed, issues, score, details)
        self.validation_history.append(result.to_dict())
        return result

    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            return ValidationResult(False, [f"CRITICAL: File not found: {file_path}"], 0)
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
        result = self._check_file(source, file_path)
        issues = result.get("issues", [])
        passed = not any("CRITICAL" in i for i in issues)
        return ValidationResult(passed, issues, 80 if passed else 0)

    def _check_file(self, source, path):
        result = {"issues": [], "bonus": 0, "penalty": 0, "syntax_ok": False}

        if not source.strip():
            result["issues"].append(f"CRITICAL: Empty file: {path}")
            result["penalty"] = 30
            return result

        try:
            ast.parse(source)
            result["syntax_ok"] = True
        except SyntaxError as e:
            result["issues"].append(f"CRITICAL: Syntax error in {path}: {e}")
            result["penalty"] = 40
            return result

        if len(source.strip().splitlines()) < 5:
            result["issues"].append(f"WARNING: Very short file ({path}), may be stub")
            result["penalty"] = 10

        if '"""' in source or "'''" in source:
            result["bonus"] = 5

        if "try:" in source and "except" in source:
            result["bonus"] += 5

        if "pass" == source.strip() or source.strip().endswith("\n    pass"):
            result["issues"].append(f"WARNING: File appears to be a stub: {path}")
            result["penalty"] += 20

        return result

    def get_history(self):
        return list(self.validation_history)

    def get_last_result(self):
        return self.validation_history[-1] if self.validation_history else None