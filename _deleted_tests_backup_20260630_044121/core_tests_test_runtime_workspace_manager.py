import pytest
import os
import tempfile
from core.runtime.runtime_workspace_manager import RuntimeWorkspaceManager


@pytest.fixture
def manager(tmp_path):
    return RuntimeWorkspaceManager(base_dir=str(tmp_path))


def test_create_workspace(manager):
    ws = manager.create_workspace("ws_test")
    assert ws.workspace_id == "ws_test"
    assert os.path.exists(ws.base_path)


def test_create_duplicate_returns_same(manager):
    ws1 = manager.create_workspace("ws_a")
    ws2 = manager.create_workspace("ws_a")
    assert ws1.workspace_id == ws2.workspace_id


def test_write_and_read_file(manager):
    ws = manager.create_workspace("ws_rw")
    ws.write_file("hello.txt", "hello umbra")
    content = ws.read_file("hello.txt")
    assert content == "hello umbra"


def test_file_exists(manager):
    ws = manager.create_workspace("ws_ex")
    assert not ws.file_exists("missing.txt")
    ws.write_file("present.txt", "data")
    assert ws.file_exists("present.txt")


def test_list_files(manager):
    ws = manager.create_workspace("ws_list")
    ws.write_file("a.py", "# a")
    ws.write_file("b.py", "# b")
    files = ws.list_files()
    assert len(files) == 2


def test_delete_file(manager):
    ws = manager.create_workspace("ws_del")
    ws.write_file("del_me.txt", "bye")
    result = ws.delete_file("del_me.txt")
    assert result is True
    assert not ws.file_exists("del_me.txt")


def test_destroy_workspace(manager):
    ws = manager.create_workspace("ws_destroy")
    path = ws.base_path
    manager.destroy_workspace("ws_destroy")
    assert not os.path.exists(path)
    assert not manager.workspace_exists("ws_destroy")


def test_snapshot_and_restore(manager):
    ws = manager.create_workspace("ws_snap")
    ws.write_file("original.txt", "before snapshot")
    snap_path = manager.snapshot_workspace("ws_snap", "snap1")
    ws.write_file("original.txt", "after mutation")
    manager.restore_snapshot("ws_snap", snap_path)
    content = ws.read_file("original.txt")
    assert content == "before snapshot"


def test_list_workspaces(manager):
    manager.create_workspace("ws_x")
    manager.create_workspace("ws_y")
    assert set(manager.list_workspaces()) == {"ws_x", "ws_y"}


def test_workspace_exists(manager):
    assert not manager.workspace_exists("missing")
    manager.create_workspace("present")
    assert manager.workspace_exists("present")


def test_workspace_to_dict(manager):
    ws = manager.create_workspace("ws_dict")
    ws.write_file("f.py", "x=1")
    d = ws.to_dict()
    assert d["workspace_id"] == "ws_dict"
    assert d["file_count"] == 1