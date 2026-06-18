from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline


def test_runtime_execution_pipeline():
    pipeline = RuntimeExecutionPipeline()

    result = pipeline.run(["task1", "task2"])

    assert len(result) == 2