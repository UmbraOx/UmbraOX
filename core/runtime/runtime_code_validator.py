from core.runtime.runtime_sandbox import (
    RuntimeSandbox
)

from core.runtime.runtime_ast_inspector import (
    RuntimeASTInspector
)


class RuntimeCodeValidator:

    def __init__(self):

        self.sandbox = RuntimeSandbox()

        self.inspector = (
            RuntimeASTInspector()
        )

    def validate(
        self,
        content
    ):

        sandbox_safe = (
            self.sandbox.safe(
                content
            )
        )

        syntax_valid = (
            self.inspector.inspect(
                content
            )
        )

        return {
            "safe": sandbox_safe,
            "valid": syntax_valid,
            "approved": (
                sandbox_safe and syntax_valid
            )
        }