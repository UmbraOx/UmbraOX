from datetime import datetime


class RuntimeScheduler:
    """
    Simple scheduling layer for Umbra tasks.
    """

    def __init__(self):
        self.jobs = []

    def add_job(self, name, func, interval_seconds):
        self.jobs.append(
            {
                "name": name,
                "func": func,
                "interval": interval_seconds,
                "last_run": None,
            }
        )

    def tick(self):
        now = datetime.now()

        for job in self.jobs:
            last = job["last_run"]

            if last is None:
                job["func"]()
                job["last_run"] = now