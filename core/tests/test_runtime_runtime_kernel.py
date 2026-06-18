from core.runtime.runtime_runtime_kernel import RuntimeKernel


def test_runtime_runtime_kernel():

    kernel = RuntimeKernel()

    result = kernel.boot()

    assert result["status"] == "booted"