from core.runtime.runtime_patch_pipeline import (
    RuntimePatchPipeline,
)


def test_runtime_patch_pipeline():
    pipeline = RuntimePatchPipeline()

    result = pipeline.process([
        "patch_1",
        "patch_2",
    ])

    assert result["success"] is True