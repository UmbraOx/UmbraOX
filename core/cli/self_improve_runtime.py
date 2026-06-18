from __future__ import annotations

from pprint import pprint

from core.runtime.runtime_self_improvement_engine import (
    RuntimeSelfImprovementEngine
)


def main():

    print()
    print(
        "[UMBRA SELF-IMPROVEMENT ENGINE ONLINE]"
    )
    print()

    engine = (
        RuntimeSelfImprovementEngine()
    )

    result = engine.improve()

    print()
    print("[SELF IMPROVEMENT RESULTS]")
    print()

    pprint(result)


if __name__ == "__main__":
    main()