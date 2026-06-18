class DeploymentRegistry:
    """
    Tracks deployments performed by Umbra.
    """

    def __init__(self):

        self.deployments = []

    def register(self, deployment):

        self.deployments.append(
            deployment
        )

        print(
            f"[DEPLOYMENT] registered: "
            f"{deployment['id']}"
        )

    def all(self):

        return self.deployments