import pytest
import os
from core.runtime.runtime_git_manager import RuntimeGitManager, GitResult


def test_git_result_to_dict():
    r = GitResult(True, "git status", "nothing to commit", "")
    d = r.to_dict()
    assert d["success"] is True
    assert d["command"] == "git status"


def test_init_creates_git_repo(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    result = mgr.init()
    assert result.success is True
    assert os.path.exists(os.path.join(str(tmp_path), ".git"))


def test_status_in_new_repo(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    result = mgr.status()
    assert result.success is True


def test_is_repo_false_in_empty_dir(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    assert mgr.is_repo() is False


def test_is_repo_true_after_init(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    assert mgr.is_repo() is True


def test_add_and_commit(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    # Configure git identity for the test
    mgr._run(["config", "user.email", "umbra@test.com"])
    mgr._run(["config", "user.name", "Umbra Test"])
    test_file = tmp_path / "test.py"
    test_file.write_text("x = 1\n")
    mgr.add(".")
    result = mgr.commit("initial commit")
    assert result.success is True


def test_log_after_commit(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    mgr._run(["config", "user.email", "umbra@test.com"])
    mgr._run(["config", "user.name", "Umbra Test"])
    (tmp_path / "f.py").write_text("x = 1\n")
    mgr.add(".")
    mgr.commit("test commit")
    result = mgr.log(count=5)
    assert result.success is True
    assert "test commit" in result.output


def test_diff_empty_on_clean_repo(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    mgr._run(["config", "user.email", "umbra@test.com"])
    mgr._run(["config", "user.name", "Umbra Test"])
    (tmp_path / "f.py").write_text("x = 1\n")
    mgr.add(".")
    mgr.commit("clean")
    result = mgr.diff()
    assert result.success is True
    assert result.output == ""


def test_operation_history_recorded(tmp_path):
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    mgr.init()
    mgr.status()
    assert len(mgr.get_history()) == 2


def test_set_repo_path(tmp_path):
    mgr = RuntimeGitManager()
    mgr.set_repo_path(str(tmp_path))
    assert mgr.repo_path == str(tmp_path)


def test_git_not_found_returns_error(tmp_path, monkeypatch):
    import subprocess
    original_run = subprocess.run
    def mock_run(*args, **kwargs):
        raise FileNotFoundError("git not found")
    monkeypatch.setattr(subprocess, "run", mock_run)
    mgr = RuntimeGitManager(repo_path=str(tmp_path))
    result = mgr.status()
    assert result.success is False
    assert "not found" in result.error