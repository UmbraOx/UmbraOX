from core.runtime.runtime_goal_decomposer import RuntimeGoalDecomposer


def test_runtime_goal_decomposer():
    decomposer = RuntimeGoalDecomposer()

    tasks = decomposer.decompose_goal("Build API")

    assert len(tasks) > 0