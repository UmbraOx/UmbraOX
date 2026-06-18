class RuntimeSandbox:

    def __init__(self):

        self.allowed_operations = [
            "read",
            "write",
            "execute"
        ]

    def validate_operation(
        self,
        operation
    ):

        return (
            operation
            in self.allowed_operations
        )

    def execute(
        self,
        operation,
        callback
    ):

        if not self.validate_operation(
            operation
        ):

            return {
                "success": False,
                "error": "operation_blocked"
            }

        result = callback()

        return {
            "success": True,
            "result": result
        }