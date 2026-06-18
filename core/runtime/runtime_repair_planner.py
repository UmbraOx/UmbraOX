class RuntimeRepairPlanner:
    def create_plan(self, issue):
        return [
            f"analyze::{issue}",
            f"repair::{issue}",
            f"validate::{issue}",
        ]