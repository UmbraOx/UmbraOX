import pytest
import os
from unittest.mock import MagicMock
from core.runtime.runtime_git_integration import RuntimeGitIntegration
from core.runtime.runtime_autonomous_pipeline import PipelineRun


def make_mock_git(is_repo=True, commit_success=True):
    git = MagicMock()
    git.is_repo.return_value = is_repo
    mock_result = MagicMock()
    mock_result.success = commit_success
    mock_result.output = "ok"
    git.init.return_value = mock_result
    git.add.return_value = mock_result
    git.commit.return_value = mock_result
    git.status.return_value = mock_result
    git.log.return_value = mock_result
    return git


def make_run(files=2):
    run = PipelineRun("run_0001", "build something")
    run.status = "completed"
    run.written_files = [{"file": f"code/f{i}.py", "lines": 10} for i in range(files)]
    return run


def test_commit_pipeline_run_success():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    run = make_run()
    result = integration.commit_pipeline_run(run)
    assert result is not None
    assert result.success is True


def test_commit_records_history():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    run = make_run()
    integration.commit_pipeline_run(run)
    history = integration.get_commit_history()
    assert len(history) == 1
    assert history[0]["run_id"] == "run_0001"


def test_no_commit_when_no_files():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    run = make_run(files=0)
    result = integration.commit_pipeline_run(run)
    assert result is None


def test_no_commit_when_not_repo():
    git = make_mock_git(is_repo=False)
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    run = make_run()
    result = integration.commit_pipeline_run(run)
    assert result is None


def test_auto_commit_when_enabled():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path", auto_commit=True)
    run = make_run()
    result = integration.auto_commit_if_enabled(run)
    assert result is not None


def test_auto_commit_skips_when_disabled():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path", auto_commit=False)
    run = make_run()
    result = integration.auto_commit_if_enabled(run)
    assert result is None


def test_get_repo_status_when_repo():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    status = integration.get_repo_status()
    assert status["is_repo"] is True
    assert "umbra_commits" in status


def test_get_repo_status_when_not_repo():
    git = make_mock_git(is_repo=False)
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    status = integration.get_repo_status()
    assert status["is_repo"] is False


def test_setup_repo_when_not_repo():
    git = make_mock_git(is_repo=False)
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    result = integration.setup_repo()
    assert git.init.called


def test_commit_message_contains_run_id():
    git = make_mock_git()
    integration = RuntimeGitIntegration(git, repo_path="/fake/path")
    run = make_run()
    integration.commit_pipeline_run(run)
    call_args = git.commit.call_args[0][0]
    assert "run_0001" in call_args