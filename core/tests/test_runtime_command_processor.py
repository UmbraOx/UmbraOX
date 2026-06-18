from core.runtime.runtime_command_processor import RuntimeCommandProcessor


def test_runtime_command_processor():
    processor = RuntimeCommandProcessor()

    result = processor.process("build autonomous system")

    assert result["status"] == "accepted"