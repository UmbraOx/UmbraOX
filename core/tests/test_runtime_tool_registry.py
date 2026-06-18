from core.runtime.runtime_tool_registry import RuntimeToolRegistry


def test_runtime_tool_registry():

    registry = RuntimeToolRegistry()

    registry.register(
        "tool",
        lambda: True
    )

    assert registry.get_tool("tool") is not None