class RecursiveRuntimeBuilder:

    def expand(self, topology):
        expansions = []

        workers = topology.get("workers", {})

        for worker_type in workers.get("types", []):
            expansions.append({
                "agent": worker_type,
                "status": "expandable"
            })

        return expansions