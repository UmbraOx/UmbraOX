from core.runtime.runtime_agent_factory import (
    RuntimeAgentFactory,
)


def test_runtime_agent_factory():
    factory = RuntimeAgentFactory()

    agent = factory.create_agent(
        "Builder",
        "code_generation",
    )

    assert agent["active"] is True