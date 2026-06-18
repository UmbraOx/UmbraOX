from core.runtime.runtime_module_generator import (
    RuntimeModuleGenerator
)

from core.runtime.service_code_builder import (
    ServiceCodeBuilder
)

from core.runtime.agent_code_generator import (
    AgentCodeGenerator
)

from core.runtime.gui_code_generator import (
    GuiCodeGenerator
)


class ConstructionSynthesizer:

    def __init__(self):

        self.runtime_builder = (
            RuntimeModuleGenerator()
        )

        self.service_builder = (
            ServiceCodeBuilder()
        )

        self.agent_builder = (
            AgentCodeGenerator()
        )

        self.gui_builder = (
            GuiCodeGenerator()
        )

    def synthesize(
        self,
        prompt
    ):

        outputs = []

        lower = prompt.lower()

        if "voice" in lower:

            outputs.append(
                self.runtime_builder.build(
                    "speech_runtime"
                )
            )

            outputs.append(
                self.service_builder.build_service(
                    "audio_pipeline"
                )
            )

        if "agent" in lower:

            outputs.append(
                self.agent_builder.generate(
                    "assistant_worker"
                )
            )

        if "gui" in lower or "dashboard" in lower:

            outputs.append(
                self.gui_builder.generate_window(
                    "control_center"
                )
            )

        return outputs