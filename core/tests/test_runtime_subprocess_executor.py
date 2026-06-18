import pytest
from core.runtime.runtime_subprocess_executor import RuntimeSubprocessExecutor, SubprocessResult


def test_execute_simple_echo():
    exe = RuntimeSubprocessExecutor()
    result = exe.execute("echo hello_umbra")
    assert result.success is True
    assert "hello_umbra" in result.stdout


def test_execute_captures_stderr():
    exe = RuntimeSubprocessExecutor()
    result = exe.execute("python -c \"import sys; sys.stderr.write('err_out')\"")
    assert "err_out" in result.stderr


def test_execute_blocked_command():
    exe = RuntimeSubprocessExecutor()
    result = exe.execute("rm -rf /")
    assert result.success is False
    assert "BLOCKED" in result.stderr


def test_execute_timeout():
    exe = RuntimeSubprocessExecutor(timeout=1)
    result = exe.execute("python -c \"import time; time.sleep(10)\"")
    assert result.success is False
    assert "TIMEOUT" in result.stderr


def test_execute_invalid_command():
    exe = RuntimeSubprocessExecutor()
    result = exe.execute("totally_nonexistent_command_xyz_123")
    assert result.success is False


def test_history_records_execution():
    exe = RuntimeSubprocessExecutor()
    exe.execute("echo test")
    assert len(exe.get_history()) == 1


def test_get_last_result():
    exe = RuntimeSubprocessExecutor()
    exe.execute("echo first")
    exe.execute("echo second")
    last = exe.get_last_result()
    assert "second" in last["stdout"]


def test_clear_history():
    exe = RuntimeSubprocessExecutor()
    exe.execute("echo a")
    exe.clear_history()
    assert exe.get_history() == []


def test_allowlist_blocks_unlisted():
    exe = RuntimeSubprocessExecutor(allowed_commands=["echo"])
    result = exe.execute("python --version")
    assert result.success is False
    assert "BLOCKED" in result.stderr


def test_allowlist_permits_listed():
    exe = RuntimeSubprocessExecutor(allowed_commands=["echo"])
    result = exe.execute("echo allowed")
    assert result.success is True


def test_subprocess_result_to_dict():
    result = SubprocessResult("echo hi", 0, "hi\n", "", 0.01)
    d = result.to_dict()
    assert d["command"] == "echo hi"
    assert d["success"] is True


def test_execute_python_script(tmp_path):
    script = tmp_path / "test_script.py"
    script.write_text("print('umbra_ok')")
    exe = RuntimeSubprocessExecutor()
    result = exe.execute_python(str(script))
    assert "umbra_ok" in result.stdout


def test_execute_pytest_returns_result(tmp_path):
    tiny_test = tmp_path / "test_tiny.py"
    tiny_test.write_text("def test_ok():\n    assert 1 == 1\n")
    exe = RuntimeSubprocessExecutor(timeout=15)
    result = exe.execute_pytest(str(tmp_path))
    assert result.returncode is not None
    assert isinstance(result.stdout, str)