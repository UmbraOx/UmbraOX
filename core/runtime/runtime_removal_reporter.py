class RuntimeRemovalReporter:
    def __init__(self, registry):
        self.registry = registry

    def get_deletable_files(self):
        return self.registry.list_removable()

    def preview_delete(self):
        files = self.registry.list_removable()
        return {
            "count": len(files),
            "files": files
        }