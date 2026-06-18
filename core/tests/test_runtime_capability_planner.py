from core.runtime.runtime_capability_planner import RuntimeCapabilityPlanner


def test_runtime_capability_planner():

    planner = (
        RuntimeCapabilityPlanner()
    )

    plan = planner.build_plan(
        "execution",
        "execute runtime task"
    )

    assert plan["steps"]
    assert plan["objective"]