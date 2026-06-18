class SystemicExpansionEngine:

    def expand(self, growth_report):
        expansions = []

        for index in range(growth_report["new_workers"]):
            expansions.append(
                f"worker_agent_{index + 1}"
            )

        return {
            "expansions": expansions,
            "status": "planned"
        }