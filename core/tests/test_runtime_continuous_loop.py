from core.runtime.runtime_continuous_loop import RuntimeContinuousLoop


def test_runtime_continuous_loop():

    loop = RuntimeContinuousLoop()

    result = loop.cycle()

    assert result["status"] == "running"