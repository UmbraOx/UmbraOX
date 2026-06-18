class RuntimeWorkflowEngine:
    def execute_workflow(self, workflow):
        return {
            "workflow": workflow,
            "status": "completed",
        }