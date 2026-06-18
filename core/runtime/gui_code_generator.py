class GuiCodeGenerator:

    def generate_window(
        self,
        name
    ):

        code = f"""
WINDOW = {{
    "title": "{name}",
    "width": 1280,
    "height": 720
}}
"""

        return {
            "path": f"core/gui/{name}.py",
            "code": code.strip()
        }