from core.runtime.runtime_agent import (
    RuntimeAgent
)

from core.runtime.runtime_message_bus import (
    RuntimeMessageBus
)

from core.runtime.runtime_agent_registry import (
    RuntimeAgentRegistry
)

from core.runtime.runtime_agent_coordinator import (
    RuntimeAgentCoordinator
)


def test_runtime_agents():

    bus = RuntimeMessageBus()

    planner = RuntimeAgent(
        "planner_agent",
        bus
    )

    executor = RuntimeAgent(
        "executor_agent",
        bus
    )

    registry = (
        RuntimeAgentRegistry()
    )

    registry.register(
        planner
    )

    registry.register(
        executor
    )

    planner.send_message(
        "executor_agent",
        "task",
        {
            "objective": "execute"
        }
    )

    received = (
        executor.receive_messages()
    )

    assert len(received) == 1

    coordinator = (
        RuntimeAgentCoordinator(
            registry
        )
    )

    result = coordinator.delegate(
        "execution task"
    )

    assert result["success"] is True