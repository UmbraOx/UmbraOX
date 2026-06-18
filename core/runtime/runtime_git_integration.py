import os
from datetime import datetime


class RuntimeGitIntegration:
    """
    Automatically commits Umbra-generated code to git.
    Wraps RuntimeGitManager with pipeline-aware commit logic.
    """

    def __init__(self, git_manager, repo_path=None, auto_commit=False):
        self.git = git_manager
        self.repo_path = repo_path or os.getcwd()
        self.auto_commit = auto_commit
        self.commit_history = []

    def setup_repo(self):
        if not self.git.is_repo(self.repo_path):
            result = self.git.init(self.repo_path)
            return result.success
        return True

    def commit_pipeline_run(self, pipeline_run):
        if not pipeline_run.written_files:
            return None
        if not self.git.is_repo(self.repo_path):
            return None

        self.git.set_repo_path(self.repo_path)
        add_result = self.git.add(".")
        if not add_result.success:
            return None

        msg = (
            f"umbra: run {pipeline_run.run_id} -- "
            f"{len(pipeline_run.written_files)} file(s) -- "
            f"{pipeline_run.prompt[:50]}"
        )
        commit_result = self.git.commit(msg)
        if commit_result.success:
            self.commit_history.append({
                "run_id": pipeline_run.run_id,
                "message": msg,
                "timestamp": datetime.now().isoformat(),
                "files": len(pipeline_run.written_files),
            })
        return commit_result

    def auto_commit_if_enabled(self, pipeline_run):
        if self.auto_commit:
            return self.commit_pipeline_run(pipeline_run)
        return None

    def get_commit_history(self):
        return list(self.commit_history)

    def get_repo_status(self):
        if not self.git.is_repo(self.repo_path):
            return {"is_repo": False}
        self.git.set_repo_path(self.repo_path)
        status = self.git.status()
        log = self.git.log(limit=5)
        return {
            "is_repo": True,
            "status": status.output if status.success else "",
            "recent_commits": log.output if log.success else "",
            "umbra_commits": len(self.commit_history),
        }