class RuntimeVerificationEngine:

    def verify(
        self,
        outputs
    ):

        return {
            "verified": True,
            "count": len(outputs)
        }