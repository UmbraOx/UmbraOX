# core/runtime/autonomous_architect.py

from core.runtime.project_analyzer import (
    ProjectAnalyzer
)

from core.runtime.architecture_inspector import (
    ArchitectureInspector
)


class AutonomousArchitect:

    def __init__(self):

        self.analyzer = ProjectAnalyzer()

        self.inspector = ArchitectureInspector()

    # -------------------------------------------------
    # REVIEW
    # -------------------------------------------------

    def review_project(self):

        report = self.analyzer.analyze()

        suggestions = self.inspector.inspect(
            report
        )

        result = {
            "report": report,
            "suggestions": suggestions
        }

        print("[ARCHITECT] review complete")

        return result