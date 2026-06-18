import tkinter as tk
from tkinter import scrolledtext

class RuntimeFullGuiChatWindow:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            import tkinter as tk
            from tkinter import scrolledtext
        except ImportError:
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"error": "RuntimeFullGuiChatWindow is not available"}

        root = tk.Tk()
        root.title("Umbra AI Chat")

        chat_window = scrolledtext.ScrolledText(root, width=40, height=15)
        chat_window.grid(column=0, row=0)

        def send_message():
            user_input = input_entry.get()
            if user_input:
                chat_window.insert(tk.END, f"User: {user_input}\n")
                chat_window.insert(tk.END, f"AI: {prompt}\n")
                input_entry.delete(0, tk.END)

        input_entry = tk.Entry(root, width=40)
        input_entry.grid(column=0, row=1)
        input_entry.bind("<Return>", lambda event: send_message())

        send_button = tk.Button(root, text="Send", command=send_message)
        send_button.grid(column=1, row=1)

        root.mainloop()

        return {"status": "GUI chat window closed"}