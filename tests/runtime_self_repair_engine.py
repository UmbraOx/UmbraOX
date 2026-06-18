from core.runtime.runtime_self_repair_engine import (
    RuntimeSelfRepairEngine,
)


def test_runtime_self_repair_engine():
    engine = RuntimeSelfRepairEngine()

    result = engine.repair(
        "syntax_error"
    )

    assert result["success"] is True