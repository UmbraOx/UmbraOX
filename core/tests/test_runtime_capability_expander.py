from core.runtime.runtime_capability_expander import RuntimeCapabilityExpander


def test_runtime_capability_expander():
    expander = RuntimeCapabilityExpander()

    expander.expand_capabilities(["vision", "voice"])

    assert "vision" in expander.get_capabilities()