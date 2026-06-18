from core.runtime.runtime_goal_engine import (
    RuntimeGoalEngine,
)


def test_runtime_goal_engine():
    engine = RuntimeGoalEngine()

    goals = engine.generate_goals(
        "upgrade_runtime"
    )

    assert len(goals) == 3