class RuntimeScalingEngine:

    def expand(self, amount=2):

        return [
            f"worker_expand_{i+1}"
            for i in range(amount)
        ]