from core.runtime.runtime_tool_executor import RuntimeToolExecutor


def test_runtime_tool_executor():

    executor = RuntimeToolExecutor()

    result = executor.execute(
        lambda x: x + 1,
        1
    )

    assert result == 2