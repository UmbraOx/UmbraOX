from core.runtime.runtime_capability_injector import RuntimeCapabilityInjector


def test_runtime_capability_injector():

    injector = (
        RuntimeCapabilityInjector()
    )

    injector.inject(
        "planner",
        object()
    )

    assert injector.get("planner") is not None