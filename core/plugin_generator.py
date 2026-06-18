import os


class PluginGenerator:

    def __init__(self):

        self.plugin_dir = "core/plugins"

        os.makedirs(self.plugin_dir, exist_ok=True)

    def create_plugin(self, name, description=""):

        safe_name = name.lower().replace(" ", "_")

        plugin_path = os.path.join(
            self.plugin_dir,
            f"{safe_name}.py"
        )

        if os.path.exists(plugin_path):

            print(f"[PLUGIN_GENERATOR] Plugin already exists: {safe_name}")

            return plugin_path

        template = f'''class Plugin:

    def __init__(self):

        self.name = "{safe_name}"
        self.description = "{description}"

    def run(self, *args, **kwargs):

        print("[PLUGIN] Running plugin: {safe_name}")
'''

        with open(plugin_path, "w", encoding="utf-8") as f:
            f.write(template)

        print(f"[PLUGIN_GENERATOR] Created plugin: {plugin_path}")

        return plugin_path