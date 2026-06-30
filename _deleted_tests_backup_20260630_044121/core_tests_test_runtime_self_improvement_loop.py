import pytest
from unittest.mock import MagicMock
from core.runtime.runtime_self_improvement_loop import RuntimeSelfImprovementLoop, ImprovementPlan
from core.runtime.runtime_autonomous_pipeline import PipelineRun


def make_mock_analyzer(targets=None):
    analyzer = MagicMock()
    if targets is None:
        targets = [
            {"module": "runtime_example", "reason": "missing_test", "priority": "medium"},
            {"module": "runtime_stub", "reason": "likely_stub", "priority": "high"},
        ]
    analyzer.get_improvement_targets.return_value = targets
    return analyzer


def make_mock_pipeline(status="completed"):
    pipeline = MagicMock()
    run = PipelineRun("run_0001", "test prompt")
    run.status = status
    run.written_files = [{"file": "code/test.py", "lines": 10}]
    run.results = []
    pipeline.run.return_value = run
    return pipeline


def test_analyze_and_plan_returns_plan():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    plan = loop.analyze_and_plan()
    assert isinstance(plan, ImprovementPlan)
    assert len(plan.targets) > 0


def test_plan_prioritizes_high_priority():
    targets = [
        {"module": "mod_a", "reason": "missing_test", "priority": "medium"},
        {"module": "mod_b", "reason": "likely_stub", "priority": "high"},
    ]
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(targets), make_mock_pipeline())
    plan = loop.analyze_and_plan()
    assert plan.targets[0]["module"] == "mod_b"


def test_execute_plan_runs_pipeline():
    pipeline = make_mock_pipeline()
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), pipeline)
    plan = loop.analyze_and_plan()
    loop.execute_plan(plan)
    assert pipeline.run.called


def test_execute_plan_marks_executed():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    plan = loop.analyze_and_plan()
    loop.execute_plan(plan)
    assert plan.executed is True


def test_execute_plan_records_results():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    plan = loop.analyze_and_plan()
    loop.execute_plan(plan)
    assert len(plan.results) > 0
    assert "module" in plan.results[0]
    assert "status" in plan.results[0]


def test_run_cycle_returns_plan():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    plan = loop.run_cycle()
    assert plan is not None
    assert plan.executed is True


def test_run_cycle_no_targets_returns_none():
    # Pass explicit empty list to override defaults
    empty_analyzer = MagicMock()
    empty_analyzer.get_improvement_targets.return_value = []
    loop = RuntimeSelfImprovementLoop(empty_analyzer, make_mock_pipeline())
    result = loop.run_cycle()
    assert result is None


def test_improvement_history_recorded():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    loop.run_cycle()
    loop.run_cycle()
    assert len(loop.get_history()) == 2


def test_get_last_plan():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    loop.run_cycle()
    last = loop.get_last_plan()
    assert last is not None
    assert "targets" in last


def test_build_objective_missing_test():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    obj = loop._build_objective("runtime_example", "missing_test")
    assert "test" in obj.lower()
    assert "runtime_example" in obj


def test_build_objective_stub():
    loop = RuntimeSelfImprovementLoop(make_mock_analyzer(), make_mock_pipeline())
    obj = loop._build_objective("runtime_stub", "likely_stub")
    assert "implement" in obj.lower()


def test_max_targets_limit():
    targets = [
        {"module": f"mod_{i}", "reason": "missing_test", "priority": "medium"}
        for i in range(10)
    ]
    loop = RuntimeSelfImprovementLoop(
        make_mock_analyzer(targets), make_mock_pipeline(), max_targets_per_run=3
    )
    plan = loop.analyze_and_plan()
    assert len(plan.targets) == 3


def test_improvement_plan_to_dict():
    plan = ImprovementPlan([{"module": "m", "reason": "r", "priority": "high"}])
    d = plan.to_dict()
    assert "targets" in d
    assert "executed" in d
    assert d["executed"] is False