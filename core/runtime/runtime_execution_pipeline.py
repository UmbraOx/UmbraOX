from datetime import datetime


class PipelineRun:
    def __init__(self, tasks):
        self.tasks = tasks
        self.status = "completed"
        self.written_files = []
        self.started_at = datetime.now().isoformat()
        self.completed_at = datetime.now().isoformat()

    def __len__(self):
        return len(self.tasks)

    def __iter__(self):
        return iter(self.tasks)

    def to_dict(self):
        return {
            "tasks": self.tasks,
            "status": self.status,
            "written_files": self.written_files,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class RuntimeExecutionPipeline:
    def __init__(self):
        self.pipeline_history = []

    def run(self, tasks):
        # enforce correct input shape
        if isinstance(tasks, str):
            tasks = [{"task": tasks}]

        completed = []

        for task in tasks:
            completed.append({
                "task": task,
                "status": "completed"
            })

        run_obj = PipelineRun(completed)
        self.pipeline_history.append(run_obj)
        return run_obj