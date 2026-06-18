# core/runtime/kill_switch.py

class KillSwitch:
    """
    Global emergency stop for all execution layers.
    """

    def __init__(self):
        self.active = False

    def trigger(self):
        self.active = True
        print("[KILL_SWITCH] ACTIVATED")

    def reset(self):
        self.active = False
        print("[KILL_SWITCH] RESET")


kill_switch = KillSwitch()