from core.runtime.runtime_self_extension_controller import (
    RuntimeSelfExtensionController,
)



def test_requires_approval():

    controller = (
        RuntimeSelfExtensionController()
    )

    result = controller.extend(
        "Expand runtime",
        approved=False,
    )

    assert result["success"] is False