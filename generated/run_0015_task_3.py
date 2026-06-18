import tkinter as tk
from tkinter import messagebox

def toggle_theme():
    """Toggle between light and dark themes."""
    global current_theme
    if current_theme == "dark":
        set_light_theme()
    else:
        set_dark_theme()

def set_dark_theme():
    """Set the theme to dark."""
    root.config(bg="#2c3e50")
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(fg="white", bg="#2c3e50")
        elif isinstance(widget, tk.Button):
            widget.config(bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white")
        elif isinstance(widget, tk.Entry):
            widget.config(bg="#ecf0f1", fg="#333333")

def set_light_theme():
    """Set the theme to light."""
    root.config(bg="white")
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(fg="black", bg="white")
        elif isinstance(widget, tk.Button):
            widget.config(bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white")
        elif isinstance(widget, tk.Entry):
            widget.config(bg="white", fg="black")

def on_closing():
    """Handle the window closing event."""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Initialize the main application window
root = tk.Tk()
root.title("Dark Theme Single-Page App")
root.geometry("400x300")

# Set initial theme to dark
current_theme = "dark"
set_dark_theme()

# Create UI elements
title_label = tk.Label(root, text="Welcome to the Dark Theme App", font=("Arial", 16))
title_label.pack(pady=20)

description_label = tk.Label(root, text="This is a simple single-page app with a dark theme.", wraplength=350)
description_label.pack(pady=10)

entry_field = tk.Entry(root, width=40)
entry_field.pack(pady=10)

toggle_button = tk.Button(root, text="Toggle Theme", command=toggle_theme)
toggle_button.pack(pady=20)

# Handle window closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()
