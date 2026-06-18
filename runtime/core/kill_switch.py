# core/runtime/kill_switch.py

class KillSwitch:
    def __init__(self):
        self.triggered = False

    def activate(self):
        print("[KILL SWITCH ACTIVATED]")
        self.triggered = True

    def reset(self):
        print("[KILL SWITCH RESET]")
        self.triggered = False

    def is_active(self):
        return self.triggered