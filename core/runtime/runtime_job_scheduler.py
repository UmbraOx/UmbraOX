class RuntimeJobScheduler:

    def __init__(self):

        self.jobs = []

    def schedule(
        self,
        job
    ):

        self.jobs.append(
            {
                "job": job,
                "status": "scheduled"
            }
        )

    def get_jobs(self):

        return self.jobs