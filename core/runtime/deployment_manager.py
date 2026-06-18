import uuid

from core.runtime.patch_deployer import (
    PatchDeployer
)

from core.runtime.deployment_registry import (
    DeploymentRegistry
)


class DeploymentManager:

    def __init__(self):

        self.deployer = PatchDeployer()

        self.registry = DeploymentRegistry()

    def execute(self, bundle):

        deployed = self.deployer.deploy(
            bundle
        )

        deployment = {
            "id": str(uuid.uuid4())[:8],
            "files": deployed,
            "count": len(deployed),
        }

        self.registry.register(
            deployment
        )

        return deployment