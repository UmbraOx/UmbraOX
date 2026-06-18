class RuntimeLiveScheduler:

    def schedule(self, objectives):

        return [
            {
                "wave": i + 1,
                "objective": objective
            }

            for i, objective in enumerate(objectives)
        ]