class PatchBundle:
    """
    Represents a generated upgrade package.
    """

    def build(
        self,
        proposal,
        plan,
        generated_files
    ):

        return {
            "proposal": proposal,
            "plan": plan,
            "files": generated_files,
            "file_count": len(generated_files),
            "execution_ready": False,
        }