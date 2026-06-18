from core.runtime.runtime_security_layer import RuntimeSecurityLayer
from core.runtime.runtime_build_engine import RuntimeBuildEngine


class RuntimeExecutionGateway:

    def __init__(self):
        self.security = RuntimeSecurityLayer()
        self.builder = RuntimeBuildEngine()

    def execute(self, action):
        if not self.security.validate(action):
            return {
                "status": "blocked"
            }

        return self.builder.build(action)