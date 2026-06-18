class ObjectiveExecutionRouter:

    def route(self, task):
        domain = task.get("domain")

        routes = {
            "ui": "core/gui",
            "agents": "core/agents",
            "runtime": "core/runtime",
            "planning": "core/runtime/planning",
            "deployment": "core/runtime/deployment",
            "voice": "core/runtime/speech",
            "memory": "core/runtime/memory",
        }

        return routes.get(domain, "core/runtime")