from core.runtime.runtime_execution_context import (
    RuntimeExecutionContext
)

from core.runtime.runtime_execution_validator import (
    RuntimeExecutionValidator
)


class RuntimeExecutionManager:

    def __init__(self):

        self.validator = (
            RuntimeExecutionValidator()
        )

    def execute(
        self,
        objective,
        executor
    ):

        context = (
            RuntimeExecutionContext(
                objective
            )
        )

        context.update_status(
            "running"
        )

        context.log(
            "Execution started"
        )

        try:

            result = executor(
                objective
            )

            validation = (
                self.validator.validate(
                    result
                )
            )

            if validation["success"]:

                context.update_status(
                    "completed"
                )

            else:

                context.update_status(
                    "failed_validation"
                )

            context.log(
                str(validation)
            )

            return {
                "success": (
                    validation["success"]
                ),
                "result": result,
                "validation": validation,
                "context": (
                    context.export()
                )
            }

        except Exception as e:

            context.update_status(
                "crashed"
            )

            context.log(
                str(e)
            )

            return {
                "success": False,
                "error": str(e),
                "context": (
                    context.export()
                )
            }