import pytest
import os
from core.runtime.runtime_session_manager import RuntimeSessionManager, Session


@pytest.fixture
def manager(tmp_path):
    return RuntimeSessionManager(sessions_dir=str(tmp_path))


def test_create_session(manager):
    session = manager.create_session("test_session")
    assert session.session_id == "test_session"


def test_create_session_auto_id(manager):
    session = manager.create_session()
    assert session.session_id.startswith("session_")


def test_session_set_get(manager):
    session = manager.create_session("s1")
    session.set("key", "value")
    assert session.get("key") == "value"


def test_session_get_default(manager):
    session = manager.create_session("s2")
    assert session.get("missing", "default") == "default"


def test_save_and_load_session(manager, tmp_path):
    session = manager.create_session("persist_test")
    session.set("objective", "build an API")
    manager.save_session("persist_test")
    loaded = manager.load_session("persist_test")
    assert loaded is not None
    assert loaded.get("objective") == "build an API"


def test_load_nonexistent_returns_none(manager):
    result = manager.load_session("does_not_exist")
    assert result is None


def test_load_or_create_creates_new(manager):
    session = manager.load_or_create("brand_new")
    assert session is not None
    assert session.session_id == "brand_new"


def test_load_or_create_loads_existing(manager):
    session = manager.create_session("existing")
    session.set("data", "preserved")
    manager.save_session("existing")
    loaded = manager.load_or_create("existing")
    assert loaded.get("data") == "preserved"


def test_list_saved_sessions(manager):
    s1 = manager.create_session("alpha")
    s2 = manager.create_session("beta")
    manager.save_session("alpha")
    manager.save_session("beta")
    sessions = manager.list_saved_sessions()
    assert "alpha" in sessions
    assert "beta" in sessions


def test_delete_session(manager):
    manager.create_session("to_delete")
    manager.save_session("to_delete")
    result = manager.delete_session("to_delete")
    assert result is True
    assert manager.load_session("to_delete") is None


def test_record_run(manager):
    manager.create_session("run_session")
    manager.record_run("run_session", {
        "run_id": "run_0001",
        "status": "completed",
        "prompt": "build a tool",
    })
    history = manager.get_run_history("run_session")
    assert len(history) == 1
    assert history[0]["run_id"] == "run_0001"


def test_session_to_dict(manager):
    session = manager.create_session("dict_test")
    session.set("foo", "bar")
    d = session.to_dict()
    assert "session_id" in d
    assert d["foo"] == "bar"


def test_get_latest_session_id(manager):
    manager.create_session("z_latest")
    manager.save_session("z_latest")
    latest = manager.get_latest_session_id()
    assert latest is not None