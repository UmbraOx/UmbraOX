class RuntimeExecutionValidator:

    def validate(
        self,
        result
    ):

        if result is None:

            return {
                "success": False,
                "error": "null_result"
            }

        if isinstance(
            result,
            dict
        ):

            return {
                "success": True
            }

        return {
            "success": False,
            "error": "invalid_result_type"
        }