from core.runtime.generated_project_builder import (
    GeneratedProjectBuilder
)

from core.runtime.desktop_application_builder import (
    DesktopApplicationBuilder
)

from core.runtime.agent_runtime_builder import (
    AgentRuntimeBuilder
)


class AutonomousFeatureBuilder:

    def __init__(self):

        self.project_builder = (
            GeneratedProjectBuilder()
        )

        self.desktop_builder = (
            DesktopApplicationBuilder()
        )

        self.agent_builder = (
            AgentRuntimeBuilder()
        )

    def execute(
        self,
        prompt,
        generated
    ):

        written = (
            self.project_builder.build(
                generated
            )
        )

        outputs = {
            "written_files": written
        }

        lower = prompt.lower()

        if "desktop" in lower:

            outputs["desktop"] = (
                self.desktop_builder.build(
                    "umbra_desktop"
                )
            )

        if "agent" in lower:

            outputs["agent_runtime"] = (
                self.agent_builder.build_agent_runtime(
                    "assistant_worker"
                )
            )

        return outputs