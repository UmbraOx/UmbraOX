from core.runtime.code_synthesizer import (
    CodeSynthesizer
)

from core.runtime.patch_bundle import (
    PatchBundle
)


class PatchGenerator:

    def __init__(self):

        self.synth = CodeSynthesizer()

        self.bundle = PatchBundle()

    def generate(
        self,
        proposal,
        plan
    ):

        files = self.synth.synthesize(
            plan
        )

        bundle = self.bundle.build(
            proposal,
            plan,
            files
        )

        return bundle