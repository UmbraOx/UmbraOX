from core.runtime.runtime_autonomous_brain import RuntimeAutonomousBrain


def test_runtime_autonomous_brain():
    brain = RuntimeAutonomousBrain()

    result = brain.execute_objective("build autonomous agents")

    assert result["status"] == "success"