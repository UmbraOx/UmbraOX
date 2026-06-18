import tkinter as tk
import keyboard

class OverlayWindow:
    """
    A class to create and manage an overlay window.
    The overlay window can be shown or hidden using a specified hotkey.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay Window")
        self.root.geometry("300x200")
        self.root.attributes('-topmost', True)
        self.root.withdraw()  # Start with the window hidden
        self.root.overrideredirect(True)  # Remove window decorations

    def show(self):
        """Show the overlay window."""
        self.root.deiconify()

    def hide(self):
        """Hide the overlay window."""
        self.root.withdraw()

def toggle_overlay():
    """Toggle the visibility of the overlay window using a hotkey."""
    if overlay_window.root.winfo_viewable():
        overlay_window.hide()
    else:
        overlay_window.show()

if __name__ == "__main__":
    # Create an instance of the OverlayWindow
    overlay_window = OverlayWindow()

    try:
        # Register the hotkey to toggle the overlay window
        keyboard.add_hotkey('ctrl+alt+h', toggle_overlay)
        print("Overlay window is ready. Press Ctrl+Alt+H to show/hide it.")
        
        # Start the Tkinter event loop
        overlay_window.root.mainloop()
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        # Unregister the hotkey when the program exits
        keyboard.remove_hotkey('ctrl+alt+h')
