class UmbraResourceGovernor:
    """
    Controls Umbra execution intensity safely.
    NO hardware changes. ONLY scheduling + pacing.
    """

    def __init__(self):
        self.mode = "normal"

    def set_mode(self, mode: str):
        self.mode = mode

    def apply_policy(self, spine):
        """
        Adjusts runtime intensity safely.
        """

        if self.mode == "gaming":
            spine.interval = 12
            spine.max_cycles_per_tick = 1

        elif self.mode == "streaming":
            spine.interval = 15
            spine.max_cycles_per_tick = 1

        elif self.mode == "idle":
            spine.interval = 3
            spine.max_cycles_per_tick = 3

        else:
            spine.interval = 6
            spine.max_cycles_per_tick = 2

        return {
            "mode": self.mode,
            "interval": spine.interval,
            "max_cycles_per_tick": getattr(spine, "max_cycles_per_tick", None)
        }