from core.runtime.runtime_workflow_engine import (
    RuntimeWorkflowEngine,
)


def test_runtime_workflow_engine():
    engine = RuntimeWorkflowEngine()

    result = engine.execute_workflow(
        "deployment"
    )

    assert result["status"] == "completed"