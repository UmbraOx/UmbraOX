from datetime import datetime
from collections import defaultdict


class PipelineMetrics:
    def __init__(self):
        self.total_runs = 0
        self.successful_runs = 0
        self.failed_runs = 0
        self.total_tasks_executed = 0
        self.total_files_written = 0
        self.run_durations = []
        self.errors = defaultdict(int)
        self.started_at = datetime.now().isoformat()

    def record_run(self, run):
        self.total_runs += 1

        if run.get("status") == "completed":
            self.successful_runs += 1
        else:
            self.failed_runs += 1

    def success_rate(self):
        if self.total_runs == 0:
            return 0.0
        return round(self.successful_runs / self.total_runs * 100, 2)

    def to_dict(self):
        return {
            "total_runs": self.total_runs,
            "successful_runs": self.successful_runs,
            "failed_runs": self.failed_runs,
            "success_rate": self.success_rate(),
            "started_at": self.started_at
        }


class RuntimePipelineMonitor:
    def __init__(self):
        self.metrics = PipelineMetrics()
        self.history = []

    def record(self, run):
        self.metrics.record_run(run)
        self.history.append(run)

    def summary(self):
        return self.metrics.to_dict()