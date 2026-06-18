class RuntimeReasoningEngine:

    def __init__(self):

        self.history = []

    def reason(
        self,
        context
    ):

        self.history.append(context)

        return {
            "status": "reasoned",
            "context": context
        }