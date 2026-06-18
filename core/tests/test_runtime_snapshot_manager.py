import pytest
import os
from core.runtime.runtime_snapshot_manager import RuntimeSnapshotManager


@pytest.fixture
def manager(tmp_path):
    return RuntimeSnapshotManager(snapshot_dir=str(tmp_path))


def test_create_snapshot(manager, tmp_path):
    path = manager.create_snapshot({"key": "value"})
    assert os.path.exists(path)


def test_snapshot_content(manager):
    path = manager.create_snapshot({"x": 42})
    data = manager.restore_snapshot(path)
    assert data["runtime_state"]["x"] == 42


def test_snapshot_with_label(manager):
    path = manager.create_snapshot({"y": 1}, label="mytest")
    assert "mytest" in os.path.basename(path)


def test_list_snapshots(manager):
    manager.create_snapshot({"a": 1})
    manager.create_snapshot({"b": 2})
    snaps = manager.list_snapshots()
    assert len(snaps) == 2


def test_get_latest(manager):
    manager.create_snapshot({"first": True})
    manager.create_snapshot({"second": True})
    latest = manager.get_latest()
    assert latest is not None


def test_delete_snapshot(manager):
    path = manager.create_snapshot({"del": True})
    fname = os.path.basename(path)
    result = manager.delete_snapshot(fname)
    assert result is True
    assert not os.path.exists(path)


def test_delete_nonexistent(manager):
    result = manager.delete_snapshot("nonexistent.json")
    assert result is False


def test_no_deprecation_warning():
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        from core.runtime.runtime_snapshot_manager import RuntimeSnapshotManager
        sm = RuntimeSnapshotManager()
        sm.create_snapshot({"test": True})
        deprecation_warns = [x for x in w if "utcnow" in str(x.message).lower()]
        assert len(deprecation_warns) == 0


def test_multiple_snapshots_unique_names(manager):
    paths = [manager.create_snapshot({"i": i}) for i in range(5)]
    assert len(set(paths)) == 5


def test_snapshot_counter_increments(manager):
    p1 = manager.create_snapshot({"a": 1})
    p2 = manager.create_snapshot({"b": 2})
    assert p1 != p2