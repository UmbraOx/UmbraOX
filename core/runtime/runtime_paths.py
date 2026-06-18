from pathlib import Path


class RuntimePaths:

    ROOT = Path(".")

    GENERATED = ROOT / "generated"

    MEMORY = ROOT / "memory"

    LOGS = ROOT / "logs"

    @classmethod
    def ensure(cls):

        cls.GENERATED.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.MEMORY.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.LOGS.mkdir(
            parents=True,
            exist_ok=True
        )