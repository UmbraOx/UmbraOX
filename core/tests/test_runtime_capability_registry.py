from core.runtime.runtime_capability_registry import (
    RuntimeCapabilityRegistry,
)


def test_runtime_capability_registry():
    registry = RuntimeCapabilityRegistry()

    registry.register(
        "builder",
        "code_generation",
    )

    assert registry.get("builder") == "code_generation"