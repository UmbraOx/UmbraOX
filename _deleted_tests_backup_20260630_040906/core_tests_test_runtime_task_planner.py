from core.runtime.runtime_task_planner import RuntimeTaskPlanner


def test_runtime_task_planner():
    planner = RuntimeTaskPlanner()

    plan = planner.create_plan("build runtime")

    assert len(plan) > 0