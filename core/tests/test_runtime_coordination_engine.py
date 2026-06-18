from core.runtime.runtime_coordination_engine import RuntimeCoordinationEngine


def test_runtime_coordination_engine():

    engine = RuntimeCoordinationEngine()

    result = engine.coordinate(
        ["planner", "executor"]
    )

    assert result["status"] == "coordinated"