import os
import importlib.util


class RuntimePluginLoader:

    def __init__(self):
        self.plugin_dir = "plugins"

        os.makedirs(
            self.plugin_dir,
            exist_ok=True
        )

    def load_plugins(self):
        loaded = []

        for file in os.listdir(
            self.plugin_dir
        ):
            if not file.endswith(".py"):
                continue

            path = os.path.join(
                self.plugin_dir,
                file
            )

            spec = (
                importlib.util
                .spec_from_file_location(
                    file[:-3],
                    path
                )
            )

            module = (
                importlib.util
                .module_from_spec(spec)
            )

            spec.loader.exec_module(module)

            loaded.append(
                file[:-3]
            )

        return loaded