from core.runtime.runtime_runtime_evolver import (
    RuntimeRuntimeEvolver,
)


def test_runtime_runtime_evolver():
    evolver = RuntimeRuntimeEvolver()

    state = {
        "version": 1,
    }

    result = evolver.evolve(state)

    assert result["version"] == 2
    assert result["evolved"] is True