from core.runtime.runtime_goal_orchestrator import RuntimeGoalOrchestrator


def test_runtime_goal_orchestrator():
    orchestrator = RuntimeGoalOrchestrator()

    result = orchestrator.register_goal("expand runtime")

    assert result["status"] == "registered"