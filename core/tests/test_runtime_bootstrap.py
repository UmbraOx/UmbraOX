from core.runtime.runtime_bootstrap import RuntimeBootstrap


def test_runtime_bootstrap():
    bootstrap = RuntimeBootstrap()

    result = bootstrap.bootstrap_runtime()

    assert result["runtime_initialized"] is True