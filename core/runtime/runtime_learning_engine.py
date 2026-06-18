from collections import defaultdict


class RuntimeLearningEngine:

    def __init__(self):

        self.metrics = defaultdict(list)

    def record(
        self,
        category,
        value
    ):

        self.metrics[
            category
        ].append(value)

    def summarize(self):

        summary = {}

        for key, values in self.metrics.items():

            summary[key] = {
                "count": len(values),
                "latest": values[-1] if values else None
            }

        return summary