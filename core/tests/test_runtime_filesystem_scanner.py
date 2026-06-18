from core.runtime.runtime_filesystem_scanner import (
    RuntimeFilesystemScanner,
)


def test_runtime_filesystem_scanner():
    scanner = RuntimeFilesystemScanner()

    result = scanner.scan("core")

    assert "files" in result
    assert "directories" in result