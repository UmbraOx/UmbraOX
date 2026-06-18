from datetime import UTC
from datetime import datetime


class RuntimeCodeGenerator:

    def generate_stub(
        self,
        class_name,
        methods=None
    ):

        methods = methods or []

        lines = [
            f"class {class_name}:",
            "",
            "    def __init__(self):",
            "        pass",
            ""
        ]

        for method in methods:

            lines.extend(
                [
                    f"    def {method}(self):",
                    "        return True",
                    ""
                ]
            )

        return {
            "class_name": class_name,
            "code": "\n".join(lines),
            "created": (
                datetime.now(UTC).isoformat()
            )
        }