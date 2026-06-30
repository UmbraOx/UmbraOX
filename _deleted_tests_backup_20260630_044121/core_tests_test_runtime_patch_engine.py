from core.runtime.runtime_patch_engine import (
    RuntimePatchEngine,
)

from core.runtime.runtime_patch_applier import (
    RuntimePatchApplier,
)


def test_runtime_patch_engine():
    engine = RuntimePatchEngine()
    applier = RuntimePatchApplier()

    patch = engine.generate_patch(
        "test.py",
        "hello",
        "goodbye",
    )

    result = applier.apply_patch(
        "hello world",
        patch,
    )

    assert result == "goodbye world"