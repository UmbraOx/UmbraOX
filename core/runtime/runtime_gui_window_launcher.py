import os

class RuntimeGuiWindowLauncher:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            import tkinter as tk
        except ImportError:
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def launch_window(self, title: str, size: tuple = (400, 300)) -> None:
        if not self.is_available():
            print("Tkinter is not available. Cannot launch GUI window.")
            return

        root = tk.Tk()
        root.title(title)
        root.geometry(f"{size[0]}x{size[1]}")
        root.mainloop()