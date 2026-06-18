class LiveExecutionMonitor:

    def display(
        self,
        results
    ):

        for result in results:

            print(
                "[LIVE]",
                result["worker"],
                "->",
                result["objective"],
                "::",
                result["status"]
            )