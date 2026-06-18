class UmbraHotReloadEngine:

    def reload(
        self,
        module
    ):
        return {
            "module": module,
            "reloaded": True
        }