class SynthesisValidator:

    def validate(
        self,
        outputs
    ):

        validated = []

        for item in outputs:

            if (
                "path" in item and
                "code" in item
            ):

                validated.append(item)

        return validated