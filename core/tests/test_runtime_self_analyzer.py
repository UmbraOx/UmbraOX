import pytest
import os
from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer, ModuleAnalysis


@pytest.fixture
def analyzer(tmp_path):
    runtime_dir = tmp_path / "runtime"
    tests_dir = tmp_path / "tests"
    runtime_dir.mkdir()
    tests_dir.mkdir()
    return RuntimeSelfAnalyzer(
        runtime_dir=str(runtime_dir),
        tests_dir=str(tests_dir),
    )


def test_analyze_valid_file(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_example.py"
    f.write_text("class MyClass:\n    def my_method(self):\n        pass\n")
    result = analyzer.analyze_file(str(f))
    assert result.syntax_valid is True
    assert result.line_count == 3


def test_analyze_invalid_syntax(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_bad.py"
    f.write_text("def broken(\n  pass")
    result = analyzer.analyze_file(str(f))
    assert result.syntax_valid is False
    assert result.syntax_error is not None


def test_analyze_missing_file(analyzer):
    result = analyzer.analyze_file("/nonexistent/file.py")
    assert result.syntax_valid is False


def test_detects_classes(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_cls.py"
    f.write_text("class Alpha:\n    pass\nclass Beta:\n    pass\n")
    result = analyzer.analyze_file(str(f))
    class_names = [c["name"] for c in result.classes]
    assert "Alpha" in class_names
    assert "Beta" in class_names


def test_detects_has_tests(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_tested.py"
    f.write_text("class TestedClass:\n    pass\n")
    test_f = tmp_path / "tests" / "test_runtime_tested.py"
    test_f.write_text("def test_it(): pass\n")
    result = analyzer.analyze_file(str(f))
    assert result.has_tests is True


def test_detects_no_tests(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_untested.py"
    f.write_text("class UntestedClass:\n    pass\n")
    result = analyzer.analyze_file(str(f))
    assert result.has_tests is False


def test_analyze_all_runtime_modules(analyzer, tmp_path):
    for i in range(3):
        f = tmp_path / "runtime" / f"runtime_mod{i}.py"
        f.write_text(f"class Mod{i}:\n    pass\n")
    results = analyzer.analyze_all_runtime_modules()
    assert len(results) == 3


def test_find_modules_without_tests(analyzer, tmp_path):
    f1 = tmp_path / "runtime" / "runtime_a.py"
    f1.write_text("class A:\n    pass\n")
    f2 = tmp_path / "runtime" / "runtime_b.py"
    f2.write_text("class B:\n    pass\n")
    test_f = tmp_path / "tests" / "test_runtime_a.py"
    test_f.write_text("def test_a(): pass\n")
    without_tests = analyzer.find_modules_without_tests()
    names = [a.module_name for a in without_tests]
    assert "runtime_b" in names
    assert "runtime_a" not in names


def test_get_module_summary(analyzer, tmp_path):
    f = tmp_path / "runtime" / "runtime_s.py"
    f.write_text("class S:\n    pass\n")
    summary = analyzer.get_module_summary()
    assert "total_modules" in summary
    assert summary["total_modules"] >= 1


def test_module_analysis_to_dict():
    m = ModuleAnalysis("/path/to/file.py", "runtime_example")
    d = m.to_dict()
    assert "file_path" in d
    assert "module_name" in d
    assert d["syntax_valid"] is True