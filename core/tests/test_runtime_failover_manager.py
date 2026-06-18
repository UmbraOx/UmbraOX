from core.runtime.runtime_failover_manager import RuntimeFailoverManager


def test_runtime_failover_manager():

    manager = RuntimeFailoverManager()

    result = manager.failover(
        "primary_agent"
    )

    assert result["status"] == "failover_started"