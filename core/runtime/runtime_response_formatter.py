class RuntimeResponseFormatter:
    def format(self, execution_result):
        return {
            "status": execution_result.get("status", "unknown"),
            "completed_tasks": len(execution_result.get("execution", [])),
            "goals": execution_result.get("plan", []),
        }