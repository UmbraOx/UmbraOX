import json
from datetime import datetime
from pathlib import Path


class UmbraSystemSnapshot:

    def create(
        self,
        state
    ):

        Path(
            "workspace/snapshots"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )

        path = (
            f"workspace/snapshots/"
            f"snapshot_{timestamp}.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                state,
                file,
                indent=4
            )

        return path