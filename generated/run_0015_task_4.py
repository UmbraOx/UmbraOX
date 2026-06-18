"""
This module implements the dark theme styles for a UI application.
It ensures consistency across all UI components and pages.
"""

import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root):
    """
    Apply dark theme styles to the given Tkinter root window and its child widgets.

    :param root: The main Tkinter window or frame to apply the theme to.
    """
    try:
        # Set the background color for the root window
        root.configure(bg="#2c3e50")

        # Configure style for ttk widgets
        style = ttk.Style(root)
        style.theme_use("clam")  # Use a theme that supports custom styles

        # Define dark theme colors
        bg_color = "#2c3e50"
        fg_color = "#ecf0f1"
        button_bg = "#34495e"
        button_fg = "#ecf0f1"

        # Configure ttk.Button style
        style.configure("TButton", background=button_bg, foreground=button_fg,
                         relief=tk.RAISED, borderwidth=2)

        # Configure ttk.Label style
        style.configure("TLabel", background=bg_color, foreground=fg_color)

        # Configure ttk.Entry style
        style.configure("TEntry", fieldbackground="#34495e", foreground="#ecf0f1",
                         insertbackground="#ecf0f1")

        # Configure ttk.Checkbutton style
        style.configure("TCheckbutton", background=bg_color, foreground=fg_color)

        # Configure ttk.Radiobutton style
        style.configure("TRadiobutton", background=bg_color, foreground=fg_color)

        # Apply styles to existing widgets
        for child in root.winfo_children():
            if isinstance(child, tk.Frame):
                apply_dark_theme(child)
            elif isinstance(child, ttk.Button):
                child.config(style="TButton")
            elif isinstance(child, ttk.Label):
                child.config(style="TLabel")
            elif isinstance(child, ttk.Entry):
                child.config(style="TEntry")
            elif isinstance(child, ttk.Checkbutton):
                child.config(style="TCheckbutton")
            elif isinstance(child, ttk.Radiobutton):
                child.config(style="TRadiobutton")

    except Exception as e:
        print(f"An error occurred while applying dark theme: {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")

    # Create some sample widgets
    label = ttk.Label(root, text="Dark Theme Label")
    label.pack(pady=10)

    button = ttk.Button(root, text="Click Me")
    button.pack(pady=10)

    entry = ttk.Entry(root)
    entry.pack(pady=10)

    checkbutton = ttk.Checkbutton(root, text="Check me")
    checkbutton.pack(pady=10)

    radiobutton = ttk.Radiobutton(root, text="Radio Option", value=1)
    radiobutton.pack(pady=10)

    # Apply dark theme
    apply_dark_theme(root)

    root.mainloop()
