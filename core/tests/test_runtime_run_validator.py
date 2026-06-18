import pytest
import os
from core.runtime.runtime_run_validator import RuntimeRunValidator, ValidationResult
from core.runtime.runtime_autonomous_pipeline import PipelineRun


@pytest.fixture
def validator():
    return RuntimeRunValidator(timeout=5)


def make_run_with_files(tmp_path, files):
    run = PipelineRun("run_test", "test prompt")
    run.status = "completed"
    run.written_files = []
    for filename, content in files.items():
        full = tmp_path / filename
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
        run.written_files.append({"file": str(full), "lines": len(content.splitlines())})
    return run


def test_validate_run_passes_valid_python(validator, tmp_path):
    code = "def hello():\n    '''Hello function.'''\n    return 'hello'\n\nif __name__ == '__main__':\n    print(hello())\n"
    run = make_run_with_files(tmp_path, {"script.py": code})
    result = validator.validate_run(run)
    assert result.passed is True


def test_validate_run_fails_syntax_error(validator, tmp_path):
    code = "def broken(\n    pass"
    run = make_run_with_files(tmp_path, {"bad.py": code})
    result = validator.validate_run(run)
    assert result.passed is False
    assert any("Syntax error" in i or "CRITICAL" in i for i in result.issues)


def test_validate_run_empty_files_fails(validator):
    run = PipelineRun("run_empty", "test")
    run.status = "completed"
    run.written_files = []
    result = validator.validate_run(run)
    assert result.passed is False


def test_validate_run_score_with_docstring(validator, tmp_path):
    code = '"""Module docstring."""\n\ndef func():\n    """Func docstring."""\n    try:\n        return 42\n    except Exception:\n        pass\n'
    run = make_run_with_files(tmp_path, {"good.py": code})
    result = validator.validate_run(run)
    assert result.score > 90


def test_validate_file_valid(validator, tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x = 1\ny = 2\nprint(x + y)\n")
    result = validator.validate_file(str(f))
    assert result.passed is True


def test_validate_file_missing(validator):
    result = validator.validate_file("/nonexistent/path.py")
    assert result.passed is False


def test_validation_history_recorded(validator, tmp_path):
    code = "x = 1\ny = 2\n"
    run = make_run_with_files(tmp_path, {"s.py": code})
    validator.validate_run(run)
    assert len(validator.get_history()) == 1


def test_get_last_result_none_when_empty(validator):
    assert validator.get_last_result() is None


def test_validation_result_to_dict():
    r = ValidationResult(True, ["warning"], 85)
    d = r.to_dict()
    assert d["passed"] is True
    assert d["score"] == 85
    assert "warning" in d["issues"]


def test_stub_file_penalized(validator, tmp_path):
    code = "def my_function():\n    pass\n"
    run = make_run_with_files(tmp_path, {"stub.py": code})
    result = validator.validate_run(run)
    assert result.score < 100