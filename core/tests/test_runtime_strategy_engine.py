from core.runtime.runtime_strategy_engine import RuntimeStrategyEngine


def test_runtime_strategy_engine():

    engine = RuntimeStrategyEngine()

    result = engine.build_strategy(
        "Create autonomous runtime"
    )

    assert result["status"] == "strategy_created"