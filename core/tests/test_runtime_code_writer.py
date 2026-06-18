import pytest
import os
from core.runtime.runtime_code_writer import RuntimeCodeWriter, WriteResult


@pytest.fixture
def writer(tmp_path):
    return RuntimeCodeWriter(base_dir=str(tmp_path), backup_dir=str(tmp_path / ".backups"))


def test_write_creates_file(writer, tmp_path):
    result = writer.write("hello.py", "x = 1\n")
    assert result.success is True
    assert os.path.exists(os.path.join(str(tmp_path), "hello.py"))


def test_write_content_correct(writer, tmp_path):
    writer.write("test.py", "print('umbra')\n")
    content = writer.read("test.py")
    assert content == "print('umbra')\n"


def test_write_invalid_syntax_blocked(writer):
    result = writer.write("bad.py", "def broken(\n  pass")
    assert result.success is False
    assert "Syntax" in result.message


def test_write_non_python_skips_validation(writer):
    result = writer.write("readme.md", "# not python\ndef broken(")
    assert result.success is True


def test_write_creates_backup_on_overwrite(writer, tmp_path):
    writer.write("file.py", "x = 1\n")
    result = writer.write("file.py", "x = 2\n")
    assert result.success is True
    assert result.backup_path is not None
    assert os.path.exists(result.backup_path)


def test_write_overwrite_false_blocks(writer):
    writer.write("once.py", "x = 1\n")
    result = writer.write("once.py", "x = 2\n", overwrite=False)
    assert result.success is False
    assert "overwrite" in result.message


def test_write_many(writer, tmp_path):
    files = {
        "module_a.py": "A = 1\n",
        "module_b.py": "B = 2\n",
    }
    results = writer.write_many(files)
    assert len(results) == 2
    assert all(r.success for r in results)


def test_exists(writer):
    assert writer.exists("nothing.py") is False
    writer.write("something.py", "x = 1\n")
    assert writer.exists("something.py") is True


def test_delete(writer):
    writer.write("del_me.py", "x = 1\n")
    result = writer.delete("del_me.py")
    assert result is True
    assert not writer.exists("del_me.py")


def test_list_python_files(writer):
    writer.write("a.py", "x = 1\n")
    writer.write("b.py", "y = 2\n")
    writer.write("notes.txt", "not python")
    files = writer.list_python_files()
    py_files = [f for f in files if f.endswith(".py")]
    assert len(py_files) == 2


def test_write_history_recorded(writer):
    writer.write("a.py", "x = 1\n")
    writer.write("b.py", "y = 2\n")
    assert len(writer.get_write_history()) == 2


def test_failed_writes_filter(writer):
    writer.write("good.py", "x = 1\n")
    writer.write("bad.py", "def broken(\n")
    failed = writer.get_failed_writes()
    assert len(failed) == 1


def test_restore_backup(writer, tmp_path):
    writer.write("restore_me.py", "x = 'original'\n")
    writer.write("restore_me.py", "x = 'modified'\n")
    success = writer.restore_backup("restore_me.py")
    assert success is True
    content = writer.read("restore_me.py")
    assert "original" in content


def test_write_result_to_dict():
    r = WriteResult(True, "/some/path.py", "ok", "/backup/path.py")
    d = r.to_dict()
    assert d["success"] is True
    assert d["path"] == "/some/path.py"


def test_write_absolute(writer, tmp_path):
    abs_path = os.path.join(str(tmp_path), "absolute.py")
    result = writer.write_absolute(abs_path, "z = 99\n")
    assert result.success is True
    assert os.path.exists(abs_path)