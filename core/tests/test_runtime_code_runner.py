import pytest
import os
from core.runtime.runtime_code_runner import RuntimeCodeRunner, RunResult


@pytest.fixture
def runner(tmp_path):
    return RuntimeCodeRunner(timeout=10, working_dir=str(tmp_path))


def test_run_string_hello_world(runner):
    result = runner.run_string("print('hello_umbra')")
    assert result.success is True
    assert "hello_umbra" in result.stdout


def test_run_string_captures_stderr(runner):
    result = runner.run_string("import sys; sys.stderr.write('err_out')")
    assert "err_out" in result.stderr


def test_run_string_syntax_error(runner):
    result = runner.run_string("def broken(\n  pass")
    assert result.success is False


def test_run_string_timeout(runner):
    runner.timeout = 1
    result = runner.run_string("import time; time.sleep(10)")
    assert result.success is False
    assert "TIMEOUT" in result.stderr


def test_run_file(runner, tmp_path):
    script = tmp_path / "test_script.py"
    script.write_text("print('file_ran')\n")
    result = runner.run_file(str(script))
    assert result.success is True
    assert "file_ran" in result.stdout


def test_run_file_missing(runner):
    result = runner.run_file("/nonexistent/path/script.py")
    assert result.success is False
    assert "not found" in result.stderr


def test_run_history_recorded(runner):
    runner.run_string("x = 1")
    runner.run_string("y = 2")
    assert len(runner.get_history()) == 2


def test_get_last_result(runner):
    runner.run_string("print('first')")
    runner.run_string("print('second')")
    last = runner.get_last_result()
    assert "second" in last["stdout"]


def test_clear_history(runner):
    runner.run_string("x = 1")
    runner.clear_history()
    assert runner.get_history() == []


def test_run_result_to_dict():
    r = RunResult(True, "output", "", 0, 0.01, "test.py")
    d = r.to_dict()
    assert d["success"] is True
    assert d["stdout"] == "output"


def test_run_string_with_computation(runner):
    result = runner.run_string("result = 2 + 2; print(f'result={result}')")
    assert result.success is True
    assert "result=4" in result.stdout


def test_run_workspace_file(runner, tmp_path):
    code_dir = tmp_path / "code"
    code_dir.mkdir()
    script = code_dir / "my_script.py"
    script.write_text("print('workspace_ok')\n")
    result = runner.run_workspace_file(str(tmp_path), "code/my_script.py")
    assert result.success is True
    assert "workspace_ok" in result.stdout