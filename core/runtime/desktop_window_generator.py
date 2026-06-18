class DesktopWindowGenerator:

    def create(
        self,
        window_name
    ):

        return {
            "title": window_name,
            "resizable": True,
            "theme": "umbra_dark"
        }