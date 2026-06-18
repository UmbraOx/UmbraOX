class RuntimeExecutionMonitor:
    """
    Simple execution tracker.
    """

    def track(self, results):
        if not isinstance(results, list):
            results = [results]

        completed = sum(1 for r in results if r.get("status") == "completed")

        return {
            "completed": completed,
            "total": len(results),
            "success": completed == len(results),
        }