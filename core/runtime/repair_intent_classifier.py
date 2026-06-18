class RepairIntentClassifier:

    def classify(self, analysis):
        if analysis.functions or analysis.classes:
            return "keep_or_improve"

        if analysis.imports:
            return "review"

        if "__init__.py" in analysis.path:
            return "protect"

        return "candidate_stub"