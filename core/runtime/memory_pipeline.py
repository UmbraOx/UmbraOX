import json
from pathlib import Path


class MemoryPipeline:

    FILE = Path(
        "memory/runtime_memory.json"
    )

    def write(self, context):

        self.FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = []

        if self.FILE.exists():

            try:
                data = json.loads(
                    self.FILE.read_text(
                        encoding="utf-8"
                    )
                )

            except:
                data = []

        data.append(context)

        self.FILE.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return True