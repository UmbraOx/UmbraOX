from core.runtime.runtime_autonomous_controller import RuntimeAutonomousController


def test_runtime_autonomous_controller():

    controller = RuntimeAutonomousController()

    result = controller.control(
        "build system"
    )

    assert result["status"] == "controlled"