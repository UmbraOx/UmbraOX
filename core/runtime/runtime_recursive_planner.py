class RuntimeRecursivePlanner:
    def expand_goal(self, goal, depth=3):
        tasks = []

        for i in range(depth):
            tasks.append(
                f"{goal} :: phase_{i + 1}"
            )

        return tasks