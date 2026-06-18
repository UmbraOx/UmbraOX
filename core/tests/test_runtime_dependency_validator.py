from core.runtime.runtime_dependency_validator import (
    RuntimeDependencyValidator,
)


def test_runtime_dependency_validator():
    validator = RuntimeDependencyValidator()

    validator.add_dependency("pytest")
    validator.add_dependency("networkx")

    result = validator.validate(
        ["pytest"]
    )

    assert result["valid"] is False
    assert "networkx" in result["missing"]