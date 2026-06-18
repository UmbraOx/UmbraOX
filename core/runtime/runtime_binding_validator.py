class RuntimeBindingValidator:
    """
    Ensures runtime method calls are valid before execution.
    """

    def validate_method(self, obj, method_name: str):
        if not hasattr(obj, method_name):
            return False, f"Missing method: {method_name}"

        method = getattr(obj, method_name)

        if not callable(method):
            return False, f"{method_name} is not callable"

        return True, None