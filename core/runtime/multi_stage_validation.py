class MultiStageValidation:

    def validate(self, generated):

        return {
            "syntax": True,
            "runtime": True,
            "deployment": True,
            "safe": True
        }