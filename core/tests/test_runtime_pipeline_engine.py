from core.runtime.runtime_pipeline_engine import (
    RuntimePipelineEngine,
)


def test_runtime_pipeline_engine():
    engine = RuntimePipelineEngine()

    result = engine.run([
        "plan",
        "build",
        "validate",
    ])

    assert len(result) == 3