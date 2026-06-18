import pytest
from core.runtime.runtime_prompt_templates import RuntimePromptTemplates, detect_template, get_prompt


def test_detect_template_test():
    assert detect_template("write pytest tests for my module") == "python_test"


def test_detect_template_api():
    assert detect_template("build a REST API with Flask") == "python_api"


def test_detect_template_data():
    assert detect_template("analyze CSV file with pandas") == "data_analysis"


def test_detect_template_class():
    assert detect_template("write a Python class for user management") == "python_class"


def test_detect_template_automation():
    assert detect_template("automate file renaming in a directory") == "automation"


def test_detect_template_script():
    assert detect_template("write a Python script to process logs") == "python_script"


def test_detect_template_default():
    result = detect_template("do something unclear")
    assert result == "default"


def test_get_prompt_contains_objective():
    prompt = get_prompt("build a web scraper", "python_script")
    assert "build a web scraper" in prompt


def test_get_prompt_auto_detects():
    prompt = get_prompt("write pytest tests for RuntimeQueue")
    assert "pytest" in prompt.lower() or "test" in prompt.lower()


def test_runtime_prompt_templates_list():
    pt = RuntimePromptTemplates()
    templates = pt.list_templates()
    assert "python_script" in templates
    assert "python_test" in templates
    assert "default" in templates


def test_runtime_prompt_templates_get_prompt():
    pt = RuntimePromptTemplates()
    prompt = pt.get_prompt("build a CSV parser", "data_analysis")
    assert "CSV parser" in prompt


def test_runtime_prompt_templates_add_custom():
    pt = RuntimePromptTemplates()
    pt.add_template("custom", "Custom template: {objective}")
    assert "custom" in pt.list_templates()
    prompt = pt.get_prompt("my task", "custom")
    assert "my task" in prompt


def test_usage_tracking():
    pt = RuntimePromptTemplates()
    pt.get_prompt("task 1", "default")
    pt.get_prompt("task 2", "default")
    stats = pt.get_usage_stats()
    assert stats.get("default", 0) == 2


def test_detect_template_method():
    pt = RuntimePromptTemplates()
    assert pt.detect_template("write a test suite") == "python_test"


def test_all_templates_have_objective_placeholder():
    pt = RuntimePromptTemplates()
    for name, template in pt.templates.items():
        assert "{objective}" in template, f"Template '{name}' missing {{objective}}"