# core/runtime/architecture_inspector.py


class ArchitectureInspector:

    def inspect(self, report):

        suggestions = []

        # -----------------------------------------
        # TODO DETECTION
        # -----------------------------------------

        if report["total_todos"] > 0:

            suggestions.append(
                "Project contains TODO items."
            )

        # -----------------------------------------
        # FILE COUNT
        # -----------------------------------------

        if report["total_files"] < 10:

            suggestions.append(
                "Project architecture is still small."
            )

        # -----------------------------------------
        # IMPORT COMPLEXITY
        # -----------------------------------------

        if report["total_imports"] > 100:

            suggestions.append(
                "Project imports becoming complex."
            )

        print(
            f"[ARCHITECTURE] "
            f"{len(suggestions)} suggestions"
        )

        return suggestions