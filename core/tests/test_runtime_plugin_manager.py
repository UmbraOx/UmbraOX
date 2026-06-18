from core.runtime.runtime_plugin import RuntimePlugin
from core.runtime.runtime_plugin_manager import RuntimePluginManager


def test_runtime_plugin_manager():

    manager = (
        RuntimePluginManager()
    )

    plugin = (
        RuntimePlugin(
            "test_plugin"
        )
    )

    result = manager.load(
        plugin
    )

    assert result["success"] is True
    assert "test_plugin" in manager.get_plugins()