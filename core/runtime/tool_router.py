# core/runtime/tool_router.py


class ToolRouter:
    def __init__(self, registry=None):
        self.registry = registry

    def route(self, user_input):

        text = user_input.lower()

        # -----------------------------------------
        # CREATE FILE
        # -----------------------------------------
        if "create a file named" in text:

            return {
                "tool": "fs.create_file",
                "args": {
                    "raw": user_input
                }
            }

        # -----------------------------------------
        # CREATE FOLDER
        # -----------------------------------------
        if "create a folder named" in text:

            return {
                "tool": "fs.create_folder",
                "args": {
                    "raw": user_input
                }
            }

        # -----------------------------------------
        # FALLBACK
        # -----------------------------------------
        return {
            "tool": "noop",
            "args": {
                "raw": user_input
            }
        }