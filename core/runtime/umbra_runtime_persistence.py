import json


class UmbraRuntimePersistence:

    def save(
        self,
        state
    ):
        with open(
            "umbra_state.json",
            "w"
        ) as f:
            json.dump(
                state,
                f,
                indent=4
            )

        return True