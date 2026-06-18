from core.runtime.runtime_learning_engine import RuntimeLearningEngine


class RuntimeRecursiveImprovement:

    def __init__(self):

        self.learning = (
            RuntimeLearningEngine()
        )

    def improve(
        self,
        runtime_state
    ):

        issues = runtime_state.get(
            "issues",
            []
        )

        for issue in issues:

            self.learning.record(
                "issues",
                issue
            )

        return {
            "success": True,
            "issues_processed": len(issues),
            "learning": (
                self.learning.summarize()
            )
        }