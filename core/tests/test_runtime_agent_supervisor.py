from core.runtime.runtime_agent_supervisor import RuntimeAgentSupervisor


def test_runtime_agent_supervisor():

    supervisor = RuntimeAgentSupervisor()

    result = supervisor.supervise(
        ["agent1", "agent2"]
    )

    assert result["status"] == "supervising"
    assert len(result["agents"]) == 2