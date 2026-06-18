from core.runtime.umbra_runtime_shell import (
    UmbraRuntimeShell
)


class UmbraCommandCenter:

    def __init__(self):
        self.shell = (
            UmbraRuntimeShell()
        )

    def process(
        self,
        command
    ):
        return self.shell.execute(
            command
        )