from core.runtime.runtime_autonomous_loop import RuntimeAutonomousLoop


def test_runtime_autonomous_loop():

    loop = (
        RuntimeAutonomousLoop()
    )

    result = loop.cycle(
        [
            "memory pressure"
        ],
        [
            {
                "safe": True,
                "efficient": True,
                "autonomous": True
            }
        ]
    )

    assert result["decision"] is not None