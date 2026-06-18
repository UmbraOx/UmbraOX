import os
from typing import Dict, Any


class RuntimeSelfAnalyzer:
    """
    Stable analyzer with fixed contract.
    """

    def __init__(self, root_path: str = "C:\\Umbra"):
        self.root_path = root_path

    # REQUIRED BY TESTS
    def get_module_summary(self) -> Dict[str, Any]:
        """
        Returns stable summary schema expected by improvement loop.
        """

        total_modules = 0
        modules_with_tests = 0
        syntax_errors = 0
        total_lines = 0
        total_classes = 0

        suggestions = []

        for root, _, files in os.walk(self.root_path):
            for f in files:
                if f.endswith(".py"):
                    total_modules += 1
                    path = os.path.join(root, f)

                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()

                        total_lines += len(content.splitlines())

                        if "class " in content:
                            total_classes += content.count("class ")

                        if "test_" in f or "tests" in path:
                            modules_with_tests += 1

                        # heuristic suggestion
                        if len(content) < 50:
                            suggestions.append({
                                "module": f,
                                "reason": "likely_stub",
                                "priority": "low"
                            })

                    except Exception:
                        syntax_errors += 1

        return {
            "total_modules": total_modules,
            "modules_with_tests": modules_with_tests,
            "modules_without_tests": total_modules - modules_with_tests,
            "syntax_errors": syntax_errors,
            "total_lines": total_lines,
            "total_classes": total_classes,
            "suggestions": suggestions,
        }