from core.runtime.runtime_workspace_builder import (
    RuntimeWorkspaceBuilder
)

from core.runtime.application_scaffolder import (
    ApplicationScaffolder
)


class DesktopApplicationBuilder:

    def __init__(self):

        self.workspace = (
            RuntimeWorkspaceBuilder()
        )

        self.scaffolder = (
            ApplicationScaffolder()
        )

    def build(
        self,
        name
    ):

        workspace = (
            self.workspace.create_workspace(
                name
            )
        )

        scaffold = (
            self.scaffolder.scaffold(
                name
            )
        )

        return {
            "workspace": workspace,
            "scaffold": scaffold
        }