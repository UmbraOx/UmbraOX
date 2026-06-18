from core.runtime.runtime_recursive_executor import RuntimeRecursiveExecutor


def test_runtime_recursive_executor():
    executor = RuntimeRecursiveExecutor()

    result = executor.execute_recursive(["a", "b"])

    assert len(result) == 2