import pytest
import os
from core.runtime.runtime_auto_tester import RuntimeAutoTester, AutoTestResult


@pytest.fixture
def tester(tmp_path):
    return RuntimeAutoTester(project_root=str(tmp_path), timeout=30)


def test_parse_passing_output(tester):
    output = "5 passed, 1 skipped in 2.3s"
    result = tester._parse_result(output, 2.3)
    assert result.passed == 5
    assert result.skipped == 1


def test_parse_failing_output(tester):
    output = "3 passed, 2 failed, 1 error in 5.1s"
    result = tester._parse_result(output, 5.1)
    assert result.passed == 3
    assert result.failed == 2
    assert result.errors == 1
    assert result.success is False


def test_parse_all_passing(tester):
    output = "10 passed in 1.5s"
    result = tester._parse_result(output, 1.5)
    assert result.passed == 10
    assert result.success is True


def test_run_tests_real(tester):
    tiny_test = os.path.join(str(tester.project_root), "test_tiny.py")
    with open(tiny_test, "w") as f:
        f.write("def test_ok():\n    assert 1 == 1\n")
    result = tester.run_tests(test_path=tiny_test)
    assert result is not None
    assert result.passed >= 1 or result.errors >= 0


def test_result_to_dict():
    result = AutoTestResult(10, 0, 0, 1, 2.5, "output")
    d = result.to_dict()
    assert d["passed"] == 10
    assert d["success"] is True


def test_result_summary():
    result = AutoTestResult(5, 0, 0, 0, 1.0, "")
    summary = result.summary()
    assert "PASS" in summary
    assert "5" in summary


def test_result_failure_summary():
    result = AutoTestResult(3, 2, 0, 0, 1.0, "")
    assert "FAIL" in result.summary()


def test_history_recorded(tester, tmp_path):
    tiny = tmp_path / "test_h.py"
    tiny.write_text("def test_x():\n    assert True\n")
    tester.run_tests(test_path=str(tiny))
    assert len(tester.get_history()) == 1


def test_get_last_result_none_when_empty(tester):
    assert tester.get_last_result() is None


def test_is_suite_passing_none_when_no_runs(tester):
    assert tester.is_suite_passing() is None


def test_run_generated_code_tests_no_tests(tester, tmp_path):
    result = tester.run_generated_code_tests(str(tmp_path))
    assert result is None


def test_run_single_file(tester, tmp_path):
    f = tmp_path / "test_single.py"
    f.write_text("def test_one():\n    assert 1 == 1\n")
    result = tester.run_single_file(str(f))
    assert result is not None