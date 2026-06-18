import os

class SystemIntrospector:
    """
    Reads Umbra's own structure safely (read-only).
    """

    def scan_core(self, root="core"):
        structure = {}

        for folder, _, files in os.walk(root):
            structure[folder] = files

        return structure

    def read_file(self, path):
        try:
            with open(path, "r") as f:
                return f.read()
        except:
            return None


system_introspector = SystemIntrospector()