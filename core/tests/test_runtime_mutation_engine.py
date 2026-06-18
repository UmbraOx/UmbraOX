from core.runtime.runtime_mutation_engine import (
    RuntimeMutationEngine,
)


def test_runtime_mutation_engine():
    engine = RuntimeMutationEngine()

    result = engine.mutate(
        "print('hello')"
    )

    assert "mutation_applied" in result