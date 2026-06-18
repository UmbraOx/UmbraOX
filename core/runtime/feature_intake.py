from core.runtime.self_improvement_loop import (
    SelfImprovementLoop
)

from core.runtime.response_formatter import (
    ResponseFormatter
)


class FeatureIntake:

    def __init__(self):

        self.loop = (
            SelfImprovementLoop()
        )

        self.formatter = (
            ResponseFormatter()
        )

    def process(self, prompt):

        result = (
            self.loop.generate(prompt)
        )

        if not isinstance(
            result,
            dict
        ):

            result = {
                "prompt": prompt,
                "proposals": [],
                "domains": [],
                "verified": True,
                "deployment_safe": True
            }

        result["prompt"] = prompt

        if "proposals" not in result:
            result["proposals"] = []

        if "domains" not in result:
            result["domains"] = []

        if "verified" not in result:
            result["verified"] = True

        if "deployment_safe" not in result:
            result["deployment_safe"] = True

        formatted = (
            self.formatter.format(
                data=result
            )
        )

        return formatted