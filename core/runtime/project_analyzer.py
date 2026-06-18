# core/runtime/project_analyzer.py

from core.runtime.code_indexer import CodeIndexer


class ProjectAnalyzer:

    def __init__(self):

        self.indexer = CodeIndexer()

    # -------------------------------------------------
    # ANALYZE
    # -------------------------------------------------

    def analyze(self):

        index = self.indexer.index_project()

        report = {
            "total_files": len(index),
            "total_imports": 0,
            "total_todos": 0,
            "files_with_todos": []
        }

        for path, data in index.items():

            report["total_imports"] += len(
                data["imports"]
            )

            report["total_todos"] += len(
                data["todos"]
            )

            if data["todos"]:

                report["files_with_todos"].append(
                    path
                )

        print("[ANALYZER] analysis complete")

        return report