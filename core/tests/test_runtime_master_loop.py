from core.runtime.runtime_master_loop import RuntimeMasterLoop


def test_runtime_master_loop():
    loop = RuntimeMasterLoop()

    result = loop.run_cycle()

    assert result["success"] is True