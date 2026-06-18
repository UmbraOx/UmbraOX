from core.runtime.runtime_self_builder import RuntimeSelfBuilder


def test_runtime_self_builder():
    builder = RuntimeSelfBuilder()

    result = builder.build_missing_capability("vision")

    assert result["success"] is True