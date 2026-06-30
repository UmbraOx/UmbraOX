import pytest
import os
from core.runtime.runtime_project_builder import RuntimeProjectBuilder, ProjectBlueprint


def make_builder():
    return RuntimeProjectBuilder()


def test_build_script_returns_blueprint():
    builder = make_builder()
    bp = builder.build("my_script", project_type="script", description="test script")
    assert isinstance(bp, ProjectBlueprint)
    assert bp.name == "my_script"


def test_build_cli_has_main():
    builder = make_builder()
    bp = builder.build("my_cli", project_type="cli", description="cli tool")
    assert "main.py" in bp.files


def test_build_api_has_app():
    builder = make_builder()
    bp = builder.build("my_api", project_type="api", description="rest api")
    assert "app.py" in bp.files


def test_build_library_has_init():
    builder = make_builder()
    bp = builder.build("my_lib", project_type="library", description="python lib")
    file_keys = list(bp.files.keys())
    assert any("__init__.py" in k for k in file_keys)


def test_build_script_has_readme():
    builder = make_builder()
    bp = builder.build("my_script", project_type="script")
    assert "README.md" in bp.files


def test_build_cli_has_tests():
    builder = make_builder()
    bp = builder.build("test_cli", project_type="cli")
    assert any("test" in k for k in bp.files)


def test_build_creates_valid_python(tmp_path):
    import ast
    builder = make_builder()
    bp = builder.build("valid_proj", project_type="script")
    for path, content in bp.files.items():
        if path.endswith(".py"):
            try:
                ast.parse(content)
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {path}: {e}")


def test_build_history_recorded():
    builder = make_builder()
    builder.build("proj_a", project_type="script")
    builder.build("proj_b", project_type="cli")
    assert len(builder.get_build_history()) == 2


def test_blueprint_to_dict():
    builder = make_builder()
    bp = builder.build("dict_test", project_type="api")
    d = bp.to_dict()
    assert "name" in d
    assert "project_type" in d
    assert "files" in d


def test_supported_types():
    builder = make_builder()
    types = builder.get_supported_types()
    assert "cli" in types
    assert "api" in types
    assert "library" in types


def test_build_writes_to_disk(tmp_path):
    from core.runtime.runtime_code_writer import RuntimeCodeWriter
    writer = RuntimeCodeWriter(base_dir=str(tmp_path))
    builder = RuntimeProjectBuilder(code_writer=writer)
    bp = builder.build("disk_proj", project_type="script", output_dir=str(tmp_path))
    assert os.path.exists(os.path.join(str(tmp_path), "script.py"))


def test_project_entry_point_set():
    builder = make_builder()
    bp = builder.build("ep_test", project_type="cli")
    assert bp.entry_point == "main.py"