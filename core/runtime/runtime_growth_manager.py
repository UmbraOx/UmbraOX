class RuntimeGrowthManager:

    def evaluate(self, interpreted):
        domains = interpreted.get("domains", [])

        return {
            "new_workers": len(domains),
            "new_services": len(domains) * 2,
            "recommended_scaling": len(domains) > 3
        }