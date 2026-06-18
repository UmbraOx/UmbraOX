from core.runtime.runtime_memory_bridge import RuntimeMemoryBridge


def test_runtime_memory_bridge():
    bridge = RuntimeMemoryBridge()

    bridge.store("goal", "expand")

    assert bridge.retrieve("goal") == "expand"