class RuntimePromptIngestor:

    def __init__(self):

        self.history = []

    def ingest(
        self,
        prompt
    ):

        self.history.append(prompt)

        return {
            "status": "ingested",
            "prompt": prompt
        }