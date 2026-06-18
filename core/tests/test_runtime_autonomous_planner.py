from core.runtime.runtime_autonomous_planner import RuntimeAutonomousPlanner


def test_runtime_autonomous_planner():
    planner = RuntimeAutonomousPlanner()

    plan = planner.generate_plan("Build Runtime")

    assert plan["status"] == "planned"