import pytest
from core.runtime.runtime_execution_graph import RuntimeExecutionGraph, ExecutionNode


def make_graph():
    return RuntimeExecutionGraph()


def test_add_node():
    g = make_graph()
    node = g.add_node("task_a")
    assert node.task_id == "task_a"
    assert node.state == ExecutionNode.STATE_PENDING


def test_add_duplicate_node_returns_existing():
    g = make_graph()
    n1 = g.add_node("task_a")
    n2 = g.add_node("task_a")
    assert n1.node_id == n2.node_id


def test_add_edge_and_dependency():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    g.add_edge("task_a", "task_b")
    b_node = g.get_nodes_by_state(ExecutionNode.STATE_PENDING)
    assert len(b_node) == 2


def test_add_edge_missing_node_raises():
    g = make_graph()
    g.add_node("task_a")
    with pytest.raises(ValueError):
        g.add_edge("task_a", "task_missing")


def test_get_ready_nodes_no_deps():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    ready = g.get_ready_nodes()
    assert len(ready) == 2


def test_get_ready_nodes_with_deps():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    g.add_edge("task_a", "task_b")
    ready = g.get_ready_nodes()
    ready_ids = [n.task_id for n in ready]
    assert "task_a" in ready_ids
    assert "task_b" not in ready_ids


def test_complete_unlocks_dependent():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    g.add_edge("task_a", "task_b")
    g.mark_node_running("task_a")
    g.mark_node_completed("task_a", result="done")
    ready = g.get_ready_nodes()
    assert any(n.task_id == "task_b" for n in ready)


def test_failure_propagates_to_dependent():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    g.add_edge("task_a", "task_b")
    g.mark_node_running("task_a")
    g.mark_node_failed("task_a", error="crash", propagate=True)
    b = g.get_nodes_by_state(ExecutionNode.STATE_SKIPPED)
    assert any(n.task_id == "task_b" for n in b)


def test_retry_increments_count():
    g = make_graph()
    g.add_node("task_a")
    g.mark_node_running("task_a")
    g.mark_node_failed("task_a", propagate=False)
    success = g.retry_node("task_a")
    assert success is True
    node = g.get_nodes_by_state(ExecutionNode.STATE_PENDING)
    assert node[0].retry_count == 1


def test_retry_exhausted():
    g = make_graph()
    g.add_node("task_a")
    for _ in range(3):
        g.mark_node_running("task_a")
        g.mark_node_failed("task_a", propagate=False)
        g.retry_node("task_a")
    g.mark_node_running("task_a")
    g.mark_node_failed("task_a", propagate=False)
    assert g.retry_node("task_a") is False


def test_is_complete_when_all_done():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    g.mark_node_running("task_a")
    g.mark_node_completed("task_a")
    g.mark_node_running("task_b")
    g.mark_node_completed("task_b")
    assert g.is_complete() is True


def test_summary():
    g = make_graph()
    g.add_node("task_a")
    g.add_node("task_b")
    s = g.summary()
    assert s["total"] == 2
    assert s["complete"] is False


def test_export_and_restore():
    g = make_graph()
    g.add_node("task_a", {"priority": "high"})
    g.add_node("task_b")
    g.add_edge("task_a", "task_b")
    g.mark_node_running("task_a")
    g.mark_node_completed("task_a", result="output_a")
    exported = g.export()

    g2 = make_graph()
    g2.restore(exported)
    assert g2.get_nodes_by_state(ExecutionNode.STATE_COMPLETED)[0].task_id == "task_a"


def test_no_cycle_simple():
    g = make_graph()
    g.add_node("a")
    g.add_node("b")
    g.add_edge("a", "b")
    assert g.has_cycle() is False