class RecursiveObjectivePlanner:

    def build_plan(self, interpreted):
        tasks = []

        for domain in interpreted["domains"]:
            tasks.append({
                "domain": domain,
                "objective": f"Build subsystem for {domain}",
                "status": "planned"
            })

        return {
            "tasks": tasks,
            "count": len(tasks),
            "status": "ready"
        }