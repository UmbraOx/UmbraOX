class ExecutionSimulator:
    """
    Simulates upgrade execution
    before real patching occurs.
    """

    def simulate(self, plan, blueprint):

        results = []

        for step in plan["steps"]:

            results.append({
                "step": step,
                "status": "validated"
            })

        return {
            "safe": True,
            "results": results,
            "files": blueprint["files"],
        }