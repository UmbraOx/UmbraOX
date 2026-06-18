from core.runtime.runtime_learning_engine import RuntimeLearningEngine
from core.runtime.runtime_decision_engine import RuntimeDecisionEngine


class RuntimeAutonomousLoop:

    def __init__(self):

        self.learning = (
            RuntimeLearningEngine()
        )

        self.decisions = (
            RuntimeDecisionEngine()
        )

    def cycle(
        self,
        observations,
        options
    ):

        for observation in observations:

            self.learning.record(
                "observations",
                observation
            )

        decision = (
            self.decisions.choose(
                options
            )
        )

        return {
            "decision": decision,
            "learning": (
                self.learning.summarize()
            )
        }