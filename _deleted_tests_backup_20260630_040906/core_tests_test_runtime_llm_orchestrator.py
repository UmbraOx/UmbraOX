import pytest
from unittest.mock import MagicMock
from core.runtime.runtime_llm_orchestrator import RuntimeLLMOrchestrator, OrchestrationResult
from core.runtime.runtime_execution_graph import RuntimeExecutionGraph
from core.runtime.runtime_task_state_machine import RuntimeTaskStateMachine
from core.runtime.runtime_context_builder import RuntimeContextBuilder
from core.runtime.runtime_llm_provider import LLMResponse


def make_mock_llm(content="LLM response", success=True):
    llm = MagicMock()
    resp = LLMResponse(content, "mock-model", "mock", 10)
    resp.success = success
    resp.error = None if success else "LLM error"
    llm.complete.return_value = resp
    llm.is_configured.return_value = True
    return llm


def make_orchestrator(llm=None, fail_llm=False):
    llm = llm or make_mock_llm(success=not fail_llm)
    if fail_llm:
        llm = make_mock_llm(success=False)
    graph = RuntimeExecutionGraph()
    sm = RuntimeTaskStateMachine()
    ctx = RuntimeContextBuilder()
    return RuntimeLLMOrchestrator(
        llm_provider=llm,
        context_builder=ctx,
        execution_graph=graph,
        task_state_machine=sm,
    )


def test_orchestrate_success():
    orch = make_orchestrator()
    result = orch.orchestrate("task_a", "build a hello world script")
    assert result.success is True
    assert result.task_id == "task_a"
    assert len(result.response_content) > 0


def test_orchestrate_registers_in_state_machine():
    orch = make_orchestrator()
    orch.orchestrate("task_b", "analyze the codebase")
    state = orch.state_machine.get_state("task_b")
    assert state == "completed"


def test_orchestrate_marks_graph_completed():
    orch = make_orchestrator()
    orch.orchestrate("task_c", "write unit tests")
    from core.runtime.runtime_execution_graph import ExecutionNode
    nodes = orch.graph.get_nodes_by_state(ExecutionNode.STATE_COMPLETED)
    assert any(n.task_id == "task_c" for n in nodes)


def test_orchestrate_llm_failure_marks_failed():
    orch = make_orchestrator(fail_llm=True)
    result = orch.orchestrate("task_fail", "do something")
    assert result.success is False
    assert "error" in result.metadata


def test_orchestrate_with_dependencies():
    orch = make_orchestrator()
    orch.orchestrate("dep_task", "first task")
    result = orch.orchestrate("main_task", "second task", dependencies=["dep_task"])
    assert result.success is True


def test_orchestrate_history_recorded():
    orch = make_orchestrator()
    orch.orchestrate("task_h1", "objective one")
    orch.orchestrate("task_h2", "objective two")
    assert len(orch.get_history()) == 2


def test_orchestrate_batch():
    orch = make_orchestrator()
    tasks = [
        {"task_id": "bt1", "objective": "task one"},
        {"task_id": "bt2", "objective": "task two", "dependencies": ["bt1"]},
    ]
    results = orch.orchestrate_batch(tasks)
    assert len(results) == 2
    assert all(r.success for r in results)


def test_graph_summary():
    orch = make_orchestrator()
    orch.orchestrate("gs_task", "summarize")
    s = orch.get_graph_summary()
    assert "total" in s
    assert s["total"] >= 1


def test_state_summary():
    orch = make_orchestrator()
    orch.orchestrate("ss_task", "state check")
    s = orch.get_state_summary()
    assert "total" in s


def test_orchestration_result_to_dict():
    result = OrchestrationResult(True, "t1", "response", "context", {"key": "val"})
    d = result.to_dict()
    assert d["success"] is True
    assert d["task_id"] == "t1"
    assert d["metadata"]["key"] == "val"


def test_recursion_guard_blocks_unsafe():
    from core.runtime.runtime_recursion_guard import RuntimeRecursionGuard
    # Use a guard that's already exhausted for this task
    guard = RuntimeRecursionGuard(max_calls_per_task=3, max_depth=100)
    # Pre-exhaust the call count for this task
    for _ in range(3):
        try:
            guard.enter("guarded_task", "pre")
            guard.exit("guarded_task")
        except Exception:
            pass
    orch = make_orchestrator()
    orch.recursion_guard = guard
    result = orch.orchestrate("guarded_task", "should be blocked")
    assert result.success is False