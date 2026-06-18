# core/plugins/fs_plugin.py

import os


class FSPlugin:
    def create_file(self, args):
        raw = args.get("raw", "")

        # Parse:
        # create a file named test.py with print("ok")

        path = "output.txt"
        content = ""

        if "create a file named" in raw:
            after = raw.split("create a file named", 1)[1].strip()

            if " with " in after:
                path, content = after.split(" with ", 1)
                path = path.strip()
                content = content.strip()
            else:
                path = after.strip()

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[FS] file created: {path}")

        return {
            "status": "created_file",
            "path": path
        }

    def create_folder(self, args):
        raw = args.get("raw", "")

        path = "new_folder"

        if "create a folder named" in raw:
            path = raw.split("create a folder named", 1)[1].strip()

        os.makedirs(path, exist_ok=True)

        print(f"[FS] folder created: {path}")

        return {
            "status": "created_folder",
            "path": path
        }


# ---------------------------------------------------
# COMPATIBILITY LAYER
# BossAgent still expects load_plugins()
# ---------------------------------------------------

def load_plugins(registry=None):
    """
    Compatibility bridge for older BossAgent code.
    Safe no-op registration layer.
    """

    print("[PLUGIN] Loaded: fs_plugin")

    return FSPlugin()