import pytest
import os
from core.runtime.runtime_validation_engine import RuntimeValidationEngine, ValidationResult


def make_engine():
    return RuntimeValidationEngine()


def test_valid_python_syntax():
    engine = make_engine()
    result = engine.validate_python_syntax("x = 1 + 2\nprint(x)")
    assert result.passed is True
    assert result.errors == []


def test_invalid_python_syntax():
    engine = make_engine()
    result = engine.validate_python_syntax("def broken(\n  pass")
    assert result.passed is False
    assert len(result.errors) > 0


def test_empty_code_warns():
    engine = make_engine()
    result = engine.validate_python_syntax("   ")
    assert len(result.warnings) > 0


def test_file_exists_pass(tmp_path):
    engine = make_engine()
    f = tmp_path / "test.py"
    f.write_text("x = 1")
    result = engine.validate_file_exists(str(f))
    assert result.passed is True


def test_file_exists_fail():
    engine = make_engine()
    result = engine.validate_file_exists("/nonexistent/path/file.py")
    assert result.passed is False
    assert len(result.errors) > 0


def test_output_schema_pass():
    engine = make_engine()
    result = engine.validate_output_schema(
        {"status": "ok", "result": 42}, ["status", "result"]
    )
    assert result.passed is True


def test_output_schema_missing_key():
    engine = make_engine()
    result = engine.validate_output_schema({"status": "ok"}, ["status", "result"])
    assert result.passed is False
    assert any("result" in e for e in result.errors)


def test_output_schema_not_dict():
    engine = make_engine()
    result = engine.validate_output_schema("not a dict", ["key"])
    assert result.passed is False


def test_string_not_empty_pass():
    engine = make_engine()
    assert engine.validate_string_not_empty("hello").passed is True


def test_string_not_empty_fail():
    engine = make_engine()
    assert engine.validate_string_not_empty("   ").passed is False
    assert engine.validate_string_not_empty("").passed is False


def test_validate_python_file(tmp_path):
    engine = make_engine()
    f = tmp_path / "good.py"
    f.write_text("def hello():\n    return 42\n")
    result = engine.validate_python_file(str(f))
    assert result.passed is True


def test_validate_python_file_missing():
    engine = make_engine()
    result = engine.validate_python_file("/does/not/exist.py")
    assert result.passed is False


def test_custom_rule_pass():
    engine = make_engine()
    engine.register_custom_rule("len_check", lambda v: (len(v) > 3, "too short"))
    result = engine.validate_custom("len_check", "hello")
    assert result.passed is True


def test_custom_rule_fail():
    engine = make_engine()
    engine.register_custom_rule("len_check", lambda v: (len(v) > 3, "too short"))
    result = engine.validate_custom("len_check", "hi")
    assert result.passed is False
    assert "too short" in result.errors[0]


def test_history_records():
    engine = make_engine()
    engine.validate_python_syntax("x = 1")
    engine.validate_string_not_empty("test")
    assert len(engine.get_history()) == 2


def test_failed_validations_filter():
    engine = make_engine()
    engine.validate_python_syntax("x = 1")
    engine.validate_python_syntax("def bad(\n")
    failed = engine.get_failed_validations()
    assert len(failed) == 1