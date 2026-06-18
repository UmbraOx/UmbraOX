from core.runtime.runtime_validation_engine import (
    RuntimeValidationEngine
)


class UmbraValidationPipeline:

    def __init__(self):
        self.validator = (
            RuntimeValidationEngine()
        )

    def validate(
        self,
        generated
    ):
        return self.validator.validate_generated(
            generated
        )