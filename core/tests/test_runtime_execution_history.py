from core.runtime.runtime_execution_history import RuntimeExecutionHistory


def test_runtime_execution_history():

    history = (
        RuntimeExecutionHistory()
    )

    history.record(
        "build runtime",
        True
    )

    assert len(history.get_history()) == 1