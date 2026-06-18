class ProjectManifestGenerator:

    def generate(
        self,
        name,
        modules
    ):

        return {
            "project": name,
            "modules": modules
        }