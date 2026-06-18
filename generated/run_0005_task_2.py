import tkinter as tk

def create_transparent_window(title="Transparent Window", width=300, height=200, x=100, y=100):
    """
    Creates an always-on-top transparent window using tkinter.

    Parameters:
    title (str): The title of the window.
    width (int): The width of the window in pixels.
    height (int): The height of the window in pixels.
    x (int): The x-coordinate for the top-left corner of the window.
    y (int): The y-coordinate for the top-left corner of the window.

    Returns:
    tk.Tk: The tkinter root window object.
    """
    try:
        # Create the main window
        root = tk.Tk()
        root.title(title)

        # Set the window size and position
        root.geometry(f"{width}x{height}+{x}+{y}")

        # Make the window transparent
        root.attributes('-alpha', 0.7)  # 0.0 is fully transparent, 1.0 is fully opaque

        # Keep the window always on top
        root.attributes('-topmost', True)

        # Start the main event loop
        root.mainloop()

        return root
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    create_transparent_window(width=400, height=300, x=150, y=200)
