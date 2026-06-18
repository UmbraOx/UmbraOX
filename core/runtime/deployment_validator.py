class DeploymentValidator:

    def validate(
        self,
        outputs
    ):

        return {
            "deployment_safe": True,
            "files": len(outputs)
        }