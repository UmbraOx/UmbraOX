class CodeQualityEngine:

    def validate(
        self,
        source
    ):

        return {
            "valid": True,
            "lines": len(
                source.splitlines()
            )
        }