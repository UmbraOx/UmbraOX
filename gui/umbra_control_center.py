import tkinter as tk
from tkinter import ttk


class UmbraControlCenter(tk.Tk):

    def __init__(self, spine, asset_store):

        super().__init__()

        self.spine = spine
        self.asset_store = asset_store

        self.title("Umbra Control Center")
        self.geometry("1200x700")

        self.configure(bg="#111111")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        # -----------------------
        # QUEUE TAB
        # -----------------------
        self.queue_tab = tk.Frame(self.tabs, bg="#111111")
        self.tabs.add(self.queue_tab, text="Queue")

        self.queue_list = tk.Listbox(self.queue_tab, width=80)
        self.queue_list.pack(fill="both", expand=True)

        # -----------------------
        # ASSETS TAB
        # -----------------------
        self.asset_tab = tk.Frame(self.tabs, bg="#111111")
        self.tabs.add(self.asset_tab, text="Assets")

        self.asset_list = tk.Listbox(self.asset_tab, width=80)
        self.asset_list.pack(side="left", fill="both", expand=True)

        self.preview_box = tk.Text(self.asset_tab, bg="#1a1a1a", fg="white")
        self.preview_box.pack(side="right", fill="both", expand=True)

        # -----------------------
        # CONTROL PANEL
        # -----------------------
        self.refresh_button = tk.Button(
            self.queue_tab,
            text="Refresh Queue",
            command=self.refresh_queue
        )
        self.refresh_button.pack()

        self.refresh_assets()

    # -----------------------
    # QUEUE DISPLAY
    # -----------------------

    def refresh_queue(self):

        queue = self.spine.boss_agent.queue.list_tasks()

        self.queue_list.delete(0, tk.END)

        for i, task in enumerate(queue):

            self.queue_list.insert(
                tk.END,
                f"{i}: [{task.task_type}] {task.prompt}"
            )

    # -----------------------
    # ASSET DISPLAY
    # -----------------------

    def refresh_assets(self):

        assets = self.asset_store.list_assets()

        self.asset_list.delete(0, tk.END)

        for a in assets:

            self.asset_list.insert(
                tk.END,
                f"{a['type']} | {a['asset_id']}"
            )

    # -----------------------
    # PREVIEW SELECTED ASSET
    # -----------------------

    def preview_selected(self, event):

        selection = self.asset_list.curselection()
        if not selection:
            return

        index = selection[0]
        text = self.asset_list.get(index)

        parts = text.split("|")
        if len(parts) < 2:
            return

        asset_type = parts[0].strip()
        asset_id = parts[1].strip()

        asset = self.asset_store.load(asset_type, asset_id)

        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, str(asset))