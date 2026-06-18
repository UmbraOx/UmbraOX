from core.tool_router import ToolRouter


def bootstrap_tools(router: ToolRouter):
    """
    Registers default system tools into Umbra.
    This is where Umbra gains capabilities.
    """

    # --- FILE SYSTEM TOOL ---
    class FileSystemTool:

        def run(self, data):

            action = data.get("action")

            if action == "create_file":
                path = data["path"]
                content = data.get("content", "")

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

                return {"status": "created_file", "path": path}

            if action == "create_folder":
                import os
                os.makedirs(data["path"], exist_ok=True)

                return {"status": "created_folder", "path": data["path"]}

            return {"error": "unknown_action"}


    router.register_tool("filesystem", FileSystemTool())