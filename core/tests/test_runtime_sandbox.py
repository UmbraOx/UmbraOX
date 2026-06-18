from core.runtime.runtime_sandbox import (
    RuntimeSandbox
)


def test_runtime_sandbox():

    sandbox = RuntimeSandbox()

    result = sandbox.execute(
        "execute",
        lambda: "safe"
    )

    assert result["success"] is True

    blocked = sandbox.execute(
        "network_access",
        lambda: "unsafe"
    )

    assert blocked["success"] is False